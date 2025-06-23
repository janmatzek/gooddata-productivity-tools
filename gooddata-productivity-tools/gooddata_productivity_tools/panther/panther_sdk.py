from typing import Callable

from gooddata_api_client import ApiException  # type: ignore
from gooddata_productivity_tools.panther.exceptions import PantherException
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeWorkspacePermissions,
)
from gooddata_sdk.catalog.user.entity_model.user import CatalogUser
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
    CatalogDeclarativeWorkspaceDataFilters,
)
from gooddata_sdk.catalog.workspace.entity_model.user_data_filter import (
    CatalogUserDataFilter,
)
from gooddata_sdk.catalog.workspace.entity_model.workspace import CatalogWorkspace
from gooddata_sdk.sdk import GoodDataSdk


def raise_with_context(**context_kwargs):
    def decorator(fn: Callable):
        def wrapper(*method_args, **method_kwargs):
            try:
                return fn(*method_args, **method_kwargs)
            except Exception as e:
                # Process known exceptions
                if isinstance(e, ApiException):
                    context_kwargs["http_status"] = f"{e.status} {e.reason}"
                    exception_content = e.body
                else:
                    exception_content = str(e)

                # Format the exception message: "{exception_type}: {exception_content}"
                message = f"{type(e).__name__}: {exception_content}"

                raise PantherException(message, **context_kwargs, **method_kwargs)

        return wrapper

    return decorator


class MethodsSDK:
    sdk: GoodDataSdk

    def check_workspace_exists(self, workspace_id: str) -> bool:
        try:
            self.sdk.catalog_workspace.get_workspace(workspace_id)
            return True
        except Exception:
            return False

    @raise_with_context(
        api_endpoint="sdk.catalog_workspace.get_workspace",
        http_method="GET",
    )
    def get_workspace(self, workspace_id: str, **_) -> CatalogWorkspace:
        """
        Gets a CatalogWorkspace object. Raises exception if the workspace
        does not exist or if there is an API error.
        """
        return self.sdk.catalog_workspace.get_workspace(workspace_id)

    @raise_with_context(
        api_endpoint="sdk.catalog_workspace.delete_workspace",
        http_method="DELETE",
    )
    def delete_panther_workspace(self, workspace_id: str) -> None:
        self.sdk.catalog_workspace.delete_workspace(workspace_id)

    @raise_with_context(
        api_endpoint="sdk.catalog_workspace.create_or_update",
    )
    def create_or_update_panther_workspace(
        self, workspace_id: str, workspace_name: str, parent_id: str | None, **_
    ) -> None:
        return self.sdk.catalog_workspace.create_or_update(
            CatalogWorkspace(
                workspace_id=workspace_id,
                name=workspace_name,
                parent_id=parent_id,
            )
        )

    def get_panther_children_workspaces(
        self, parent_workspace_ids: set[str]
    ) -> list[CatalogWorkspace]:
        """Calls GoodData Python SDK to retrieve all workspaces in domain and filters the
        result by the set of parent workspace IDs.
        Returns:
            list[CatalogWorkspace]: List of child workspaces in the parent workspace.
        """
        all_workspaces: list[CatalogWorkspace] = self.list_workspaces()
        children: list[CatalogWorkspace] = []

        for workspace in all_workspaces:
            if workspace.parent_id in parent_workspace_ids:
                children.append(workspace)

        return children

    def list_workspaces(self) -> list[CatalogWorkspace]:
        return self.sdk.catalog_workspace.list_workspaces()

    @raise_with_context(
        api_endpoint="sdk.catalog_permission.get_declarative_permissions",
        http_method="GET",
    )
    def get_declarative_permissions(
        self, workspace_id: str
    ) -> CatalogDeclarativeWorkspacePermissions:
        return self.sdk.catalog_permission.get_declarative_permissions(workspace_id)

    @raise_with_context(
        api_endpoint="sdk.catalog_permission.put_declarative_permissions",
        http_method="PUT",
    )
    def put_declarative_permissions(
        self, workspace_id: str, ws_permissions: CatalogDeclarativeWorkspacePermissions
    ) -> None:
        return self.sdk.catalog_permission.put_declarative_permissions(
            workspace_id, ws_permissions
        )

    @raise_with_context(
        api_endpoint="sdk.catalog_user.get_user",
        http_method="GET",
    )
    def get_user(self, user_id: str, **_) -> CatalogUser:
        return self.sdk.catalog_user.get_user(user_id)

    @raise_with_context(
        api_endpoint="sdk.catalog_user.create_or_update_user",
    )
    def create_or_update_user(self, user: CatalogUser, **_) -> None:
        return self.sdk.catalog_user.create_or_update_user(user)

    @raise_with_context(
        api_endpoint="sdk.catalog_user.delete_user",
        http_method="DELETE",
    )
    def delete_user(self, user_id: str, **_) -> None:
        return self.sdk.catalog_user.delete_user(user_id)

    @raise_with_context(
        api_endpoint="sdk.catalog_user.get_user_group",
        http_method="GET",
    )
    def get_user_group(self, user_group_id: str, **_) -> CatalogUserGroup:
        return self.sdk.catalog_user.get_user_group(user_group_id)

    @raise_with_context(
        api_endpoint="sdk.catalog_user.list_user_groups",
        http_method="GET",
    )
    def list_user_groups(self) -> list[CatalogUserGroup]:
        return self.sdk.catalog_user.list_user_groups()

    @raise_with_context(
        api_endpoint="sdk.catalog_user.create_or_update_user_group",
    )
    def create_or_update_user_group(
        self, catalog_user_group: CatalogUserGroup, **_
    ) -> None:
        return self.sdk.catalog_user.create_or_update_user_group(catalog_user_group)

    @raise_with_context(
        api_endpoint="sdk.catalog_user.delete_user_group",
        http_method="DELETE",
    )
    def delete_user_group(self, user_group_id: str) -> None:
        return self.sdk.catalog_user.delete_user_group(user_group_id)

    @raise_with_context()
    def get_declarative_workspace_data_filters(
        self,
    ) -> CatalogDeclarativeWorkspaceDataFilters:
        return self.sdk.catalog_workspace.get_declarative_workspace_data_filters()

    @raise_with_context()
    def list_user_data_filters(self, workspace_id: str) -> list[CatalogUserDataFilter]:
        return self.sdk.catalog_workspace.list_user_data_filters(workspace_id)

    @raise_with_context()
    def delete_user_data_filter(
        self, workspace_id: str, user_data_filter_id: str
    ) -> None:
        self.sdk.catalog_workspace.delete_user_data_filter(
            workspace_id, user_data_filter_id
        )

    @raise_with_context()
    def create_or_update_user_data_filter(
        self, workspace_id: str, user_data_filter: CatalogUserDataFilter
    ) -> None:
        self.sdk.catalog_workspace.create_or_update_user_data_filter(
            workspace_id, user_data_filter
        )
