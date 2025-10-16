# (C) 2025 GoodData Corporation

from gooddata_pipelines import (
    EntityType,
    PermissionIncrementalLoad,
    PermissionProvisioner,
)
from utils.args.parser import Parser
from utils.args.schemas import PermissionArgs
from utils.logger import get_logger, setup_logging
from utils.utils import (
    create_client,
    read_csv_file_to_dict,
)

setup_logging()
logger = get_logger(__name__)


def read_permissions_from_csv(
    args: PermissionArgs,
) -> list[PermissionIncrementalLoad]:
    """Reads permissions from the input csv file."""
    validated_permissions: list[PermissionIncrementalLoad] = []
    raw_permissions = read_csv_file_to_dict(
        args.perm_csv, args.delimiter, args.quotechar
    )

    for raw_permission in raw_permissions:
        try:
            if raw_permission["user_id"] and raw_permission["ug_id"]:
                raise RuntimeError(
                    "UserID and UserGroupID are mutually exclusive per csv row. "
                    f'Skipping following row: "{raw_permission}".'
                )

            entity_id = raw_permission["user_id"] or raw_permission["ug_id"]
            if not entity_id:
                raise RuntimeError(
                    "Either UserID or UserGroupID have to be defined per csv row. "
                    f'Skipping following row: "{raw_permission}".'
                )

            if raw_permission["user_id"]:
                entity_type = EntityType.user
            else:
                entity_type = EntityType.user_group

            validated_permission = PermissionIncrementalLoad(
                permission=raw_permission["ws_permissions"],
                workspace_id=raw_permission["ws_id"],
                entity_id=entity_id,
                entity_type=entity_type,
                is_active=raw_permission["is_active"],
            )
            validated_permissions.append(validated_permission)
        except KeyError as e:
            logger.error(f"Missing key in following row: {raw_permission}. Error: {e}")
            continue
        except Exception as e:
            logger.error(
                f'Unable to load following row: "{raw_permission}". Error: "{e}"'
            )
            continue

    return validated_permissions


def permission_mgmt():
    args = Parser.parse_permission_args()

    permissions = read_permissions_from_csv(args)

    permission_manager = create_client(
        PermissionProvisioner, args.profile_config, args.profile
    )

    permission_manager.logger.subscribe(logger)

    permission_manager.incremental_load(permissions)


if __name__ == "__main__":
    permission_mgmt()
