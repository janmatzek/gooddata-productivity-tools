# (C) 2025 GoodData Corporation

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
)


from pathlib import Path

from gooddata_pipelines import LocalStorageConfig, S3StorageConfig, StorageType
from utils.backup_restore_config import load_config_from_yaml  # type: ignore


def test_local_storage_config():
    config = load_config_from_yaml(Path("tests/data/backup/test_local_conf.yaml"))

    assert isinstance(config.storage, LocalStorageConfig)
    assert config.storage_type == StorageType.LOCAL
    assert config.storage.backup_path == "local_backups"


def test_s3_storage_config():
    config = load_config_from_yaml(Path("tests/data/backup/test_conf.yaml"))

    assert isinstance(config.storage, S3StorageConfig)
    assert config.storage_type == StorageType.S3
    assert config.storage.backup_path == "some/s3/backup/path/org_id/"
    assert config.storage.bucket == "some-s3-bucket"
