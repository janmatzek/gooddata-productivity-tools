# (C) 2025 GoodData Corporation

import logging

from gooddata_pipelines import BackupManager
from utils.args.parser import Parser
from utils.args.schemas import BackupArgs
from utils.backup_restore_config import load_config_from_yaml
from utils.logger import setup_logging
from utils.utils import create_client

setup_logging()
logger = logging.getLogger(__name__)


def backup():
    args: BackupArgs = Parser.parse_backup_args()

    backup_restore_config = load_config_from_yaml(args.conf)

    backup_manager = create_client(
        BackupManager,
        args.profile_config,
        args.profile,
        config=backup_restore_config,
    )

    backup_manager.logger.subscribe(logger)

    if args.input_type == "entire-organization":
        backup_manager.backup_entire_organization()
    elif args.input_type == "list-of-workspaces":
        backup_manager.backup_workspaces(str(args.ws_csv))
    elif args.input_type == "list-of-parents":
        backup_manager.backup_hierarchies(str(args.ws_csv))
    else:
        raise ValueError(f"Unsupported input type: {args.input_type}")


if __name__ == "__main__":
    backup()
