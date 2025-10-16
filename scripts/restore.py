# (C) 2025 GoodData Corporation

import logging

from gooddata_pipelines import RestoreManager, WorkspaceToRestore
from utils.args.parser import Parser
from utils.args.schemas import RestoreArgs
from utils.backup_restore_config import load_config_from_yaml
from utils.logger import setup_logging
from utils.utils import create_client, read_csv_file_to_dict

setup_logging()
logger = logging.getLogger(__name__)


def restore():
    """Main entry point of the script."""

    args: RestoreArgs = Parser.parse_restore_args()

    backup_restore_config = load_config_from_yaml(args.conf)

    restore_manager = create_client(
        RestoreManager,
        args.profile_config,
        args.profile,
        config=backup_restore_config,
    )

    # Subscribe to logs
    restore_manager.logger.subscribe(logger)

    # Load workspaces from CSV
    workspaces = read_csv_file_to_dict(args.ws_csv)

    # Validate data from CSV input
    workspaces_to_restore = [
        WorkspaceToRestore(
            id=workspace["workspace_id"],
            path=workspace["path"],
        )
        for workspace in workspaces
    ]

    # Restore workspaces
    restore_manager.restore(workspaces_to_restore)


if __name__ == "__main__":
    restore()
