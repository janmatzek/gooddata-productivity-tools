import re

from gooddata_sdk.catalog.workspace.entity_model.user_data_filter import (
    CatalogEntityIdentifier,
    CatalogUserDataFilter,
    CatalogUserDataFilterAttributes,
    CatalogUserDataFilterRelationships,
)
from gooddata_sdk.sdk import GoodDataSdk
from utils.logger import logger  # type: ignore[import]
from utils.models.user_data_filters import (  # type: ignore[import]
    UserDataFilter,
    UserDataFilterGroup,
    WorkspaceUserDataFilters,
)


class UserDataFilterProvisioner:
    def __init__(
        self,
        panther_domain: str,
        panther_token: str,
        ldm_column_name: str,
        maql_column_name: str,
    ) -> None:
        self.sdk = GoodDataSdk.create(
            host_=panther_domain,
            token_=panther_token,
        )
        self.logger = logger
        self.ldm_column_name = ldm_column_name
        self.maql_column_name = maql_column_name

    @staticmethod
    def _group_db_user_data_filters_by_ws_id(
        user_data_filters: list[UserDataFilter],
    ) -> list[WorkspaceUserDataFilters]:
        ws_map: dict[str, dict[str, set[str]]] = {}

        for udf in user_data_filters:
            ws_map.setdefault(udf.workspace_id, {}).setdefault(udf.udf_id, set()).add(
                str(udf.udf_value)
            )

        result: list[WorkspaceUserDataFilters] = []

        for ws_id, udf_dict in ws_map.items():
            udf_groups = [
                UserDataFilterGroup(udf_id=udf_id, udf_values=list(values))
                for udf_id, values in udf_dict.items()
            ]
            result.append(
                WorkspaceUserDataFilters(
                    workspace_id=ws_id, user_data_filters=udf_groups
                )
            )
        return result

    @staticmethod
    def _extract_numbers_from_maql(maql: str) -> list[str]:
        numbers = re.findall(r'"\d+"', maql)
        return [number.strip('"') for number in numbers]

    def _skip_user_data_filter_update(
        self, existing_udf: list[CatalogUserDataFilter], udf_value: list[str]
    ) -> bool:
        if not existing_udf:
            return False
        existing_udfs = self._extract_numbers_from_maql(existing_udf[0].attributes.maql)
        return set(udf_value) == set(existing_udfs)

    def _create_user_data_filters(
        self, user_data_filter_ids_to_create: list[WorkspaceUserDataFilters]
    ) -> None:
        for workspace_user_data_filter in user_data_filter_ids_to_create:
            workspace_id = workspace_user_data_filter.workspace_id
            user_data_filters = workspace_user_data_filter.user_data_filters

            gd_user_data_filters: list[CatalogUserDataFilter] = (
                self.sdk.catalog_workspace.list_user_data_filters(workspace_id)
            )

            gd_udf_ids = {
                user.relationships.user["data"].id
                for user in gd_user_data_filters
                if user.relationships and user.relationships.user
            }

            db_udf_ids = {udf.udf_id for udf in user_data_filters}

            udf_ids_to_delete = gd_udf_ids.difference(db_udf_ids)
            self._delete_user_data_filters(workspace_id, udf_ids_to_delete)

            udf_group: UserDataFilterGroup
            for udf_group in user_data_filters:
                udf_id: str = udf_group.udf_id
                udf_values: list[str] = udf_group.udf_values

                existing_udf: list[CatalogUserDataFilter] = [
                    udf for udf in gd_user_data_filters if udf.id == udf_id
                ]
                if self._skip_user_data_filter_update(existing_udf, udf_values):
                    continue

                formatted_udf_values = '", "'.join(str(value) for value in udf_values)
                maql = f'{self.maql_column_name} IN ("{formatted_udf_values}")'

                attributes = CatalogUserDataFilterAttributes(maql=maql)
                relationships = CatalogUserDataFilterRelationships(
                    labels={
                        "data": [
                            CatalogEntityIdentifier(
                                id=self.ldm_column_name, type="label"
                            )
                        ]
                    },
                    user={"data": CatalogEntityIdentifier(id=udf_id, type="user")},
                )
                user_data_filter = CatalogUserDataFilter(
                    id=udf_id,
                    attributes=attributes,
                    relationships=relationships,
                )

                try:
                    self._create_or_update_user_data_filter(
                        user_data_filter, workspace_id
                    )
                    self.logger.info(
                        f"Created or updated user data filters for user with id {udf_id} for client with id {workspace_id}"
                    )
                except Exception as e:
                    raise RuntimeError(f"Failed to create user data filters: {e}")

    def _delete_user_data_filters(self, workspace_id, udf_ids_to_delete):
        for udf_id in udf_ids_to_delete:
            try:
                self.sdk.catalog_workspace.delete_user_data_filter(workspace_id, udf_id)
                self.logger.info(f"Deleted user data filters for user with id {udf_id}")
            except Exception as e:
                raise RuntimeError(f"Failed to delete user data filters: {e}")

    def _create_or_update_user_data_filter(
        self, user_data_filter: CatalogUserDataFilter, workspace_id: str
    ) -> None:
        self.sdk.catalog_workspace.create_or_update_user_data_filter(
            workspace_id, user_data_filter
        )

    def provision(self, source_user_data_filters: list[UserDataFilter]) -> None:
        self.source_user_data_filters: list[UserDataFilter] = source_user_data_filters

        grouped_db_user_data_filters = self._group_db_user_data_filters_by_ws_id(
            self.source_user_data_filters
        )

        self._create_user_data_filters(grouped_db_user_data_filters)

        self.logger.info("User data filters provisioning completed")
