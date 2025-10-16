# (C) 2025 GoodData Corporation

from typing import Any

from gooddata_pipelines import WorkspaceIncrementalLoad, WorkspaceProvisioner
from utils.args.parser import Parser
from utils.logger import get_logger, setup_logging
from utils.utils import (
    create_client,
    read_csv_file_to_dict,
)

# Setup logging
setup_logging()
logger = get_logger(__name__)


def validate_workspace_data(
    raw_workspaces: list[dict[str, Any]],
    wdf_delimiter: str,
) -> list[WorkspaceIncrementalLoad]:
    """Validate workspace against input model."""

    validated_workspaces: list[WorkspaceIncrementalLoad] = []

    for raw_workspace in raw_workspaces:
        try:
            if raw_workspace["workspace_data_filter_values"]:
                workspace_data_filter_values = raw_workspace[
                    "workspace_data_filter_values"
                ].split(wdf_delimiter)
            else:
                workspace_data_filter_values = None
            validated_workspace = WorkspaceIncrementalLoad(
                parent_id=raw_workspace["parent_id"],
                workspace_id=raw_workspace["workspace_id"],
                workspace_name=raw_workspace["workspace_name"],
                workspace_data_filter_id=raw_workspace["workspace_data_filter_id"],
                workspace_data_filter_values=workspace_data_filter_values,
                is_active=raw_workspace["is_active"],
            )

            validated_workspaces.append(validated_workspace)
        except Exception as e:
            logger.error(
                f'Unable to load following row: "{raw_workspace}". Error: "{e}"'
            )
            continue

    return validated_workspaces


def workspace_mgmt():
    """Main function for workspace management."""

    # Create parser and parse arguments
    args = Parser.parse_workspace_args()

    # Read CSV input
    raw_workspaces = read_csv_file_to_dict(
        args.filepath, args.delimiter, args.quotechar
    )

    # Validate workspace data
    validated_workspaces = validate_workspace_data(raw_workspaces, args.inner_delimiter)

    # Create provisioner and subscribe to logger
    provisioner = create_client(WorkspaceProvisioner, args.profile_config, args.profile)

    provisioner.logger.subscribe(logger)

    # Incremental load workspaces
    provisioner.incremental_load(validated_workspaces)


if __name__ == "__main__":
    # Main function
    workspace_mgmt()
