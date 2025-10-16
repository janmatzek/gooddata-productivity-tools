import argparse
from pathlib import Path

from gooddata_sdk.utils import PROFILES_FILE_PATH
from utils.args.schemas import (
    BackupArgs,
    CustomFieldsArgs,
    PermissionArgs,
    RestoreArgs,
    UserArgs,
    UserDataFilterArgs,
    UserGroupArgs,
    WorkspaceArgs,
)


class Parser:
    """Interface to handle common command line arguments.

    Use `parse_*` class methods to parse command line arguments for each script.
    """

    parser: argparse.ArgumentParser

    DEFAULT_DELIMITER = ","
    DEFAULT_INNER_DELIMITER = "|"
    DEFAULT_QUOTECHAR = '"'

    def __init__(self, description: str) -> None:
        self.parser = argparse.ArgumentParser(description=description)

    @classmethod
    def parse_workspace_args(cls) -> WorkspaceArgs:
        """Parses workspace management command line arguments."""
        parser = cls("Management of workspaces.")

        parser._add_file_path("filepath", "Path to CSV file with input data.")
        parser._add_common_args()

        namespace = parser.parser.parse_args()

        return WorkspaceArgs(
            filepath=namespace.filepath,
            delimiter=namespace.delimiter,
            inner_delimiter=namespace.inner_delimiter,
            quotechar=namespace.quotechar,
            profile_config=namespace.profile_config,
            profile=namespace.profile,
        )

    @classmethod
    def parse_user_args(cls) -> UserArgs:
        """Parses user management command line arguments."""
        parser = cls("Management of users and userGroups.")

        parser._add_file_path("user_csv", "Path to csv with user definitions.")
        parser._add_common_args()

        namespace = parser.parser.parse_args()

        return UserArgs(
            user_csv=namespace.user_csv,
            delimiter=namespace.delimiter,
            inner_delimiter=namespace.inner_delimiter,
            quotechar=namespace.quotechar,
            profile_config=namespace.profile_config,
            profile=namespace.profile,
        )

    @classmethod
    def parse_user_group_args(cls) -> UserGroupArgs:
        """Parses user group management command line arguments."""
        parser = cls("Management of users and userGroups.")

        parser._add_file_path(
            "user_group_csv", "Path to csv with user groups definitions."
        )
        parser._add_common_args()

        namespace = parser.parser.parse_args()

        return UserGroupArgs(
            user_group_csv=namespace.user_group_csv,
            delimiter=namespace.delimiter,
            inner_delimiter=namespace.inner_delimiter,
            quotechar=namespace.quotechar,
            profile_config=namespace.profile_config,
            profile=namespace.profile,
        )

    @classmethod
    def parse_permission_args(cls) -> PermissionArgs:
        """Parses permission management command line arguments."""
        parser = cls("Management of workspace permissions.")
        parser._add_file_path("perm_csv", "Path to csv with permission definitions.")

        parser._add_csv_args()
        parser._add_profile_args()

        namespace = parser.parser.parse_args()

        return PermissionArgs(
            perm_csv=namespace.perm_csv,
            delimiter=namespace.delimiter,
            quotechar=namespace.quotechar,
            profile_config=namespace.profile_config,
            profile=namespace.profile,
        )

    @classmethod
    def parse_user_data_filter_args(cls) -> UserDataFilterArgs:
        """Parses user data filter management command line arguments."""
        parser = cls("Management of user data filters.")

        parser._add_file_path("filepath", "Path to csv with input data.")

        parser._add_ldm_column_name()
        parser._add_maql_column_name()

        parser._add_csv_args()
        parser._add_profile_args()

        namespace = parser.parser.parse_args()

        return UserDataFilterArgs(
            filepath=namespace.filepath,
            ldm_column_name=namespace.ldm_column_name,
            maql_column_name=namespace.maql_column_name,
            delimiter=namespace.delimiter,
            quotechar=namespace.quotechar,
            profile_config=namespace.profile_config,
            profile=namespace.profile,
        )

    @classmethod
    def parse_custom_fields_args(cls) -> CustomFieldsArgs:
        """Parses custom fields management command line arguments."""
        parser = cls("Management of custom fields.")
        parser._add_file_path(
            "path_to_custom_datasets_csv",
            "Path to csv with custom datasets definitions.",
        )
        parser._add_file_path(
            "path_to_custom_fields_csv", "Path to csv with custom fields definitions."
        )

        parser._add_csv_args()
        parser._add_profile_args()

        parser._add_check_relations()

        namespace = parser.parser.parse_args()

        return CustomFieldsArgs(
            path_to_custom_datasets_csv=namespace.path_to_custom_datasets_csv,
            path_to_custom_fields_csv=namespace.path_to_custom_fields_csv,
            delimiter=namespace.delimiter,
            quotechar=namespace.quotechar,
            check_relations=namespace.check_relations,
            profile_config=namespace.profile_config,
            profile=namespace.profile,
        )

    @classmethod
    def parse_backup_args(cls) -> BackupArgs:
        """Parses backup management command line arguments."""
        parser = cls("Backup of workspaces.")
        parser._add_file_path("ws_csv", "Path to csv with input data.")
        parser._add_file_path("conf", "Path to backup storage configuration file.")
        parser._add_profile_args()
        parser._add_input_type()

        namespace = parser.parser.parse_args()

        return BackupArgs(
            ws_csv=namespace.ws_csv,
            conf=namespace.conf,
            profile_config=namespace.profile_config,
            profile=namespace.profile,
            input_type=namespace.input_type,
        )

    @classmethod
    def parse_restore_args(cls) -> RestoreArgs:
        """Parses restore management command line arguments."""
        parser = cls("Restore of workspaces.")
        parser._add_file_path("ws_csv", "Path to csv with input data.")
        parser._add_file_path("conf", "Path to backup storage configuration file.")
        parser._add_profile_args()

        namespace = parser.parser.parse_args()

        return RestoreArgs(
            ws_csv=namespace.ws_csv,
            conf=namespace.conf,
            profile_config=namespace.profile_config,
            profile=namespace.profile,
        )

    def _add_common_args(self) -> None:
        self._add_csv_args()
        self._add_inner_delimiter()

        self._add_profile_args()

    def _add_profile_args(self) -> None:
        self._add_profile_config()
        self._add_profile()

    def _add_csv_args(self) -> None:
        self._add_quotechar()
        self._add_delimiter()

    def _add_file_path(self, name: str, help: str) -> None:
        self.parser.add_argument(
            name,
            type=Path,
            help=help,
        )

    def _add_delimiter(self) -> None:
        self.parser.add_argument(
            "-d",
            "--delimiter",
            type=str,
            default=self.DEFAULT_DELIMITER,
            help="Delimiter used to separate different columns in the input csv.",
        )

    def _add_inner_delimiter(self) -> None:
        self.parser.add_argument(
            "-i",
            "--inner-delimiter",
            type=str,
            default=self.DEFAULT_INNER_DELIMITER,
            help=(
                "Delimiter used to separate different inner values within "
                "the columns in the input csv which contain inner-delimiter "
                "separated values. This must differ from the 'delimiter' argument."
            ),
        )

    def _add_quotechar(self) -> None:
        self.parser.add_argument(
            "-q",
            "--quotechar",
            type=str,
            default=self.DEFAULT_QUOTECHAR,
            help="Character used for quoting (escaping) values which contain "
            "delimiters or quotechars.",
        )

    def _add_profile_config(self) -> None:
        self.parser.add_argument(
            "-p",
            "--profile-config",
            type=Path,
            default=PROFILES_FILE_PATH,
            help="Optional path to GoodData profile config. If no path is "
            "provided, the default profiles file is used.",
        )

    def _add_profile(self) -> None:
        self.parser.add_argument(
            "--profile",
            type=str,
            default="default",
            help="GoodData profile to use. If no profile is provided, 'default' "
            "is used.",
        )

    def _add_check_relations(self) -> None:
        self.parser.add_argument(
            "--no-relations-check",
            action="store_false",
            dest="check_relations",
            help="Check relations after updating LLM. "
            + "If new invalid relations are found, the update is rolled back. "
            + "Boolean, defaults to True.",
        )

    def _add_ldm_column_name(self) -> None:
        self.parser.add_argument(
            "ldm_column_name",
            type=str,
            help="LDM column name.",
        )

    def _add_maql_column_name(self) -> None:
        self.parser.add_argument(
            "maql_column_name",
            type=str,
            help="MAQL column name: {attribute/dataset.field}",
        )

    def _add_input_type(self) -> None:
        self.parser.add_argument(
            "-t",
            "--input-type",
            type=str,
            choices=["list-of-workspaces", "list-of-parents", "entire-organization"],
            default="list-of-workspaces",
            help="Type of input to use as the base of the backup. If not provided, `list-of-workspaces` is used as default.",
        )
