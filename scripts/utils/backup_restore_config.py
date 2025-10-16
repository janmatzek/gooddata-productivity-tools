from pathlib import Path

import yaml
from gooddata_pipelines import (
    BackupRestoreConfig,
    LocalStorageConfig,
    S3StorageConfig,
    StorageType,
)
from gooddata_pipelines.backup_and_restore.constants import BackupSettings


def load_config_from_yaml(path: Path) -> BackupRestoreConfig:
    """Loads the backup and restore configuration from a YAML file."""
    storage_config: LocalStorageConfig | S3StorageConfig

    with open(path, "r") as file:
        contents = yaml.safe_load(file)

    if "storage_type" not in contents:
        raise ValueError("storage_type is required in the configuration file")

    if contents["storage_type"] == "local":
        storage_type = StorageType.LOCAL
    else:
        storage_type = StorageType.S3

    if storage_type == StorageType.LOCAL:
        local_storage = contents.get("storage", {})
        if not local_storage:
            backup_path = "local_backups"
        else:
            backup_path = local_storage.get("backup_path", "local_backups")

        storage_config = LocalStorageConfig(backup_path=backup_path)
    else:
        storage_config = S3StorageConfig(
            backup_path=contents["storage"]["backup_path"],
            bucket=contents["storage"]["bucket"],
            profile=contents["storage"].get("profile"),
            aws_access_key_id=contents["storage"].get("aws_access_key_id"),
            aws_secret_access_key=contents["storage"].get("aws_secret_access_key"),
            aws_default_region=contents["storage"].get(
                "aws_default_region", "us-east-1"
            ),
        )

    config = BackupRestoreConfig(
        storage_type=storage_type,
        storage=storage_config,
        api_page_size=contents.get("api_page_size", BackupSettings.API.PAGE_SIZE),
        batch_size=contents.get("batch_size", BackupSettings.API.BATCH_SIZE),
        api_calls_per_second=contents.get(
            "api_calls_per_second", BackupSettings.API.CALLS_PER_SECOND
        ),
    )

    return config
