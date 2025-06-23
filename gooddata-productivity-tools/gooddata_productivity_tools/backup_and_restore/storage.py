import abc
import os
import shutil
from pathlib import Path
from typing import Type

import boto3
import yaml

from gooddata_productivity_tools.utils.constants import BackupSettings
from gooddata_productivity_tools.utils.models.batch import Size


class BackupRestoreConfig:
    def __init__(self, path_to_config_yaml: str):
        with open(path_to_config_yaml, "r") as stream:
            conf: dict = yaml.safe_load(stream)

        self.storage_type: str = conf["storage_type"]
        self.storage: dict[str, str] = conf["storage"]

        page_size = conf.get("api_page_size", BackupSettings.DEFAULT_PAGE_SIZE)
        self.api_page_size: Size = Size(size=page_size)

        batch_size = conf.get("batch_size", BackupSettings.DEFAULT_BATCH_SIZE)
        self.batch_size: Size = Size(size=batch_size)


class BackupStorage(abc.ABC):
    def __init__(self, conf: BackupRestoreConfig):
        return

    @abc.abstractmethod
    def export(self, folder, org_id):
        """Exports the content of the folder to the storage."""
        raise NotImplementedError

    @classmethod
    def get_storage(cls, storage_type: str) -> Type["BackupStorage"]:
        """Returns the storage class based on the storage type."""
        match storage_type:
            case "s3":
                return S3Storage
            case "local":
                return LocalStorage
            case _:
                raise RuntimeError(f'Unsupported storage type "{storage_type}".')


class S3Storage(BackupStorage):
    def __init__(self, conf: BackupRestoreConfig):
        self._config = conf.storage
        self._profile = self._config.get("profile", "default")
        self._session = self._create_boto_session(self._profile)
        self._resource = self._session.resource("s3")
        self._bucket = self._resource.Bucket(self._config["bucket"])  # type: ignore [missing library stubs]
        suffix = "/" if not self._config["backup_path"].endswith("/") else ""
        self._backup_path = self._config["backup_path"] + suffix

        self._verify_connection()

    @staticmethod
    def _create_boto_session(profile: str) -> boto3.Session:
        try:
            return boto3.Session(profile_name=profile)
        except Exception:
            # logger.warning(
            #     'AWS profile "[default]" not found. Trying other fallback methods...'
            # )
            pass  # TODO: logging via a singleton observer

        return boto3.Session()

    def _verify_connection(self) -> None:
        """
        Pings the S3 bucket to verify that the connection is working.
        """
        try:
            self._resource.meta.client.head_bucket(Bucket=self._config["bucket"])
        except Exception as e:
            raise RuntimeError(
                f"Failed to connect to S3 bucket {self._config['bucket']}: {e}"
            )

    def export(self, folder, org_id) -> None:
        """Uploads the content of the folder to S3 as backup."""
        # logger.info(
        #     f"Uploading {org_id} to {self._config['bucket']}" / "{self._backup_path}"
        # )  # TODO: logging via a singleton observer
        folder = folder + "/" + org_id
        for subdir, dirs, files in os.walk(folder):
            full_path = os.path.join(subdir)
            export_path = (
                self._backup_path + org_id + "/" + full_path[len(folder) + 1 :] + "/"
            )
            self._bucket.put_object(Key=export_path)

            for file in files:
                full_path = os.path.join(subdir, file)
                with open(full_path, "rb") as data:
                    export_path = (
                        self._backup_path + org_id + "/" + full_path[len(folder) + 1 :]
                    )
                    self._bucket.put_object(Key=export_path, Body=data)


class LocalStorage(BackupStorage):
    def __init__(self, conf: BackupRestoreConfig):
        return

    def export(self, folder, org_id, export_folder="local_backups"):
        """Copies the content of the folder to local storage as backup."""
        # logger.info(f"Saving {org_id} to local storage") # TODO: logging via a singleton observer
        shutil.copytree(
            Path(folder), Path(Path.cwd(), export_folder), dirs_exist_ok=True
        )
