import json
import os
import shutil
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import requests
import yaml

from gooddata_productivity_tools.backup_and_restore.input_loader import InputLoader
from gooddata_productivity_tools.backup_and_restore.storage import (
    BackupRestoreConfig,
    BackupStorage,
)
from gooddata_productivity_tools.panther.panther_wrapper import PantherWrapper
from gooddata_productivity_tools.utils.constants import BackupSettings, DirNames
from gooddata_productivity_tools.utils.models.batch import BackupBatch, Size


class BackupManager:
    panther: PantherWrapper
    storage: BackupStorage

    def __init__(self, path_to_config_yaml: str) -> None:
        self.config: BackupRestoreConfig = BackupRestoreConfig(path_to_config_yaml)
        self.loader = InputLoader(self.panther, self.config.api_page_size)

        self.organization_id: str = (
            self.panther.sdk.catalog_organization.organization_id
        )

    def backup_organization(self) -> None:
        """Backs up each workspace in the organization."""
        workspaces_to_backup: list[str] = self.loader.get_all_workspaces()

        self._backup(workspaces_to_backup)

    def backup_hierarchies(self, list_of_parent_workspaces: list[str]) -> None:
        """Backs up the selected hierarchies
        Args:
            list_of_parent_workspaces: List of parent workspace IDs to backup.
            For each parent workspace, all direct and indirect children will be
            backed up.
        """

        workspaces_to_backup: list[str] = self.loader.get_hierarchies(
            list_of_parent_workspaces
        )

        self._backup(workspaces_to_backup)

    def backup_workspaces(self, list_of_workspaces: list[str]) -> None:
        """Backs up the selected workspaces.

        Args:
            list_of_workspaces: List of workspace IDs to backup.
        """
        self._backup(list_of_workspaces)

    def _backup(self, workspaces_to_backup: list[str]) -> None:
        """Performs the actual backup of the workspaces."""
        batches = self.split_to_batches(workspaces_to_backup, self.config.batch_size)

        # logger.info(
        #     f"Exporting {len(workspaces_to_export)} workspaces in {len(batches)} batches."
        # ) # TODO: log observer

        self.process_batches_in_parallel(self.organization_id, self.storage, batches)

    @staticmethod
    def split_to_batches(
        workspaces_to_export: list[str], batch_size: Size
    ) -> list[BackupBatch]:
        """Splits the list of workspaces to into batches of the specified size.
        The batch is respresented as a list of workspace IDs.
        Returns a list of batches (i.e. list of lists of IDs)
        """
        list_of_batches = []
        while workspaces_to_export:
            batch = BackupBatch(workspaces_to_export[: batch_size.size])
            workspaces_to_export = workspaces_to_export[batch_size.size :]
            list_of_batches.append(batch)

        return list_of_batches

    def process_batches_in_parallel(
        self,
        organization_id: str,
        storage: BackupStorage,
        batches: list[BackupBatch],
    ) -> None:
        with ThreadPoolExecutor(max_workers=BackupSettings.MAX_WORKERS) as executor:
            futures = []
            for batch in batches:
                futures.append(
                    executor.submit(
                        self.process_batch,
                        organization_id,
                        storage,
                        batch,
                    )
                )

            for future in futures:
                future.result()

    def process_batch(
        self,
        organization_id: str,
        storage: BackupStorage,
        batch: BackupBatch,
        retry_count: int = 0,
    ) -> None:
        """Processes a single batch of workspaces for backup.
        If the batch processing fails, the function will wait
        and retry with exponential backoff up to BackupSettings.MAX_RETRIES.
        The base wait time is defined by BackupSettings.RETRY_DELAY.
        """
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                self.get_workspace_export(tmpdir, organization_id, batch.list_of_ids)

                self.archive_gooddata_layouts_to_zip(str(Path(tmpdir, organization_id)))

                storage.export(tmpdir, organization_id)

        except Exception as e:
            # Retry with exponential backoff until MAX_RETRIES, then raise the error
            if retry_count < BackupSettings.MAX_RETRIES:
                next_retry = retry_count + 1
                # logger.info(
                #     f"Unexpected error while processing a batch. Retrying {next_retry}/{BackupSettings.MAX_RETRIES}..."
                # ) # TODO: log via a singleton observer
                time.sleep(BackupSettings.RETRY_DELAY**next_retry)
                self.process_batch(organization_id, storage, batch, next_retry)
            else:
                # logger.error(f"Error processing batch: {e}") # TODO: log via a singleton observer
                raise e

    def get_workspace_export(
        self,
        local_target_path: str,
        organization_id: str,
        workspaces_to_export: list[str],
    ) -> None:
        """
        Iterate over all workspaces in the workspaces_to_export list and store
        their declarative_workspace and their respective user data filters.
        """
        exported = False
        for ws_id in workspaces_to_export:
            export_path = Path(
                local_target_path,
                organization_id,
                ws_id,
                BackupSettings.TIMESTAMP_SDK_FOLDER,
            )

            try:
                user_data_filters = self.get_user_data_filters(ws_id)
            except Exception:
                # logger.error(f"Skipping backup of {ws_id} - check if workspace exists.") # TODO: log via a singleton observer
                continue

            try:
                self.panther.sdk.catalog_workspace.store_declarative_workspace(
                    ws_id, export_path
                )
                self.store_declarative_filter_views(export_path, organization_id, ws_id)
                self.store_automations(export_path, organization_id, ws_id)

                self.store_user_data_filters(
                    user_data_filters, export_path, organization_id, ws_id
                )
                # logger.info(f"Stored export for {ws_id}") # TODO: log observer
                exported = True
            except Exception as e:
                # logger.error(f"Skipping {ws_id}. Error encountered: {e}") # TODO: log observer
                continue

        if not exported:
            raise RuntimeError(
                "None of the workspaces were exported. Check source file and their existence."
            )

    def archive_gooddata_layouts_to_zip(self, folder: str) -> None:
        """Archives the gooddata_layouts directory to a zip file."""
        target_subdir = ""
        for subdir, dirs, files in os.walk(folder):
            if DirNames.LAYOUTS in dirs:
                target_subdir = os.path.join(subdir, dirs[0])
            if DirNames.LDM in dirs:
                inner_layouts_dir = subdir + "/gooddata_layouts"
                os.mkdir(inner_layouts_dir)
                for dir in dirs:
                    shutil.move(
                        os.path.join(subdir, dir), os.path.join(inner_layouts_dir)
                    )
                shutil.make_archive(target_subdir, "zip", subdir)
                shutil.rmtree(target_subdir)

    def get_user_data_filters(self, workspace_id: str) -> dict:
        """Returns the user data filters for the specified workspace."""

        response = self.panther.get_user_data_filters(workspace_id)
        if response.ok:
            return response.json()
        else:
            raise RuntimeError(
                f"Failed to fetch user data filters for workspace {workspace_id}"
            )

    def store_automations(self, export_path: Path, org_id: str, ws_id: str) -> None:
        """Stores the automations in the specified export path."""
        # Get the automations from the API
        automations: Any = self.get_automations_from_api(ws_id)

        automations_folder_path: Path = Path(
            export_path, "gooddata_layouts", org_id, "workspaces", ws_id, "automations"
        )

        automations_file_path: Path = Path(automations_folder_path, "automations.json")

        os.mkdir(automations_folder_path)

        # Store the automations in a JSON file
        if len(automations["data"]) > 0:
            with open(automations_file_path, "w") as f:
                json.dump(automations, f)

    def get_automations_from_api(self, workspace_id: str) -> Any:
        """Returns automations for the workspace as JSON."""
        response: requests.Response = self.panther.get_automations(workspace_id)
        if response.ok:
            return response.json()
        else:
            raise RuntimeError(
                f"Failed to fetch automations for workspace {workspace_id}"
            )

    def store_declarative_filter_views(
        self, export_path: Path, org_id: str, ws_id: str
    ) -> None:
        """Stores the filter views in the specified export path."""
        # Get the filter views YAML files from the API
        self.panther.sdk.catalog_workspace.store_declarative_filter_views(
            ws_id, export_path
        )

        # Move filter views to the subfolder containing analytics model
        self.move_folder(
            Path(export_path, "gooddata_layouts", org_id, "filter_views"),
            Path(
                export_path,
                "gooddata_layouts",
                org_id,
                "workspaces",
                ws_id,
                "filter_views",
            ),
        )

    @staticmethod
    def move_folder(source: Path, destination: Path) -> None:
        """Moves the source folder to the destination."""
        shutil.move(source, destination)

    def store_user_data_filters(
        self, user_data_filters: dict, export_path: Path, org_id: str, ws_id: str
    ):
        """Stores the user data filters in the specified export path."""
        os.mkdir(
            os.path.join(
                export_path,
                "gooddata_layouts",
                org_id,
                "workspaces",
                ws_id,
                "user_data_filters",
            )
        )

        for filter in user_data_filters["userDataFilters"]:
            udf_file_path = os.path.join(
                export_path,
                "gooddata_layouts",
                org_id,
                "workspaces",
                ws_id,
                "user_data_filters",
                filter["id"] + ".yaml",
            )
            self.write_to_yaml(udf_file_path, filter)

    @staticmethod
    def write_to_yaml(folder, source):
        """Writes the source to a YAML file."""
        with open(folder, "w") as outfile:
            yaml.dump(source, outfile)
