# (C) 2025 GoodData Corporation

from dataclasses import dataclass
from pathlib import Path

from utils.args.validators import (
    delimiters_must_be_different,
    inner_delimiter_must_be_valid,
    path_must_exist,
    quotechar_must_be_valid,
)


@dataclass
class UserArgs:
    """Schema for user management command line arguments."""

    user_csv: Path
    delimiter: str
    inner_delimiter: str
    quotechar: str
    profile_config: Path
    profile: str

    def __post_init__(self) -> None:
        path_must_exist(self.user_csv)
        delimiters_must_be_different(self.delimiter, self.inner_delimiter)
        inner_delimiter_must_be_valid(self.inner_delimiter)
        quotechar_must_be_valid(self.quotechar)


@dataclass
class WorkspaceArgs:
    """Schema for workspace management CLI arguments."""

    filepath: Path
    delimiter: str
    inner_delimiter: str
    quotechar: str
    profile_config: Path
    profile: str

    def __post_init__(self) -> None:
        path_must_exist(self.filepath)
        delimiters_must_be_different(self.delimiter, self.inner_delimiter)
        inner_delimiter_must_be_valid(self.inner_delimiter)
        quotechar_must_be_valid(self.quotechar)


@dataclass
class UserGroupArgs:
    """Schema for user group management command line arguments."""

    user_group_csv: Path
    delimiter: str
    inner_delimiter: str
    quotechar: str
    profile_config: Path
    profile: str

    def __post_init__(self) -> None:
        path_must_exist(self.user_group_csv)
        delimiters_must_be_different(self.delimiter, self.inner_delimiter)
        inner_delimiter_must_be_valid(self.inner_delimiter)
        quotechar_must_be_valid(self.quotechar)


@dataclass
class PermissionArgs:
    """Schema for permission management command line arguments."""

    perm_csv: Path
    delimiter: str
    quotechar: str
    profile_config: Path
    profile: str

    def __post_init__(self) -> None:
        path_must_exist(self.perm_csv)
        quotechar_must_be_valid(self.quotechar)


@dataclass
class UserDataFilterArgs:
    """Schema for user data filter management command line arguments."""

    filepath: Path
    ldm_column_name: str
    maql_column_name: str
    delimiter: str
    quotechar: str
    profile_config: Path
    profile: str

    def __post_init__(self) -> None:
        path_must_exist(self.filepath)
        quotechar_must_be_valid(self.quotechar)


@dataclass
class CustomFieldsArgs:
    """Schema for custom fields management command line arguments."""

    path_to_custom_datasets_csv: Path
    path_to_custom_fields_csv: Path
    delimiter: str
    quotechar: str
    check_relations: bool
    profile_config: Path
    profile: str

    def __post_init__(self) -> None:
        path_must_exist(self.path_to_custom_datasets_csv)
        path_must_exist(self.path_to_custom_fields_csv)
        quotechar_must_be_valid(self.quotechar)


@dataclass
class BackupArgs:
    """Schema for backup management command line arguments."""

    ws_csv: Path
    conf: Path
    profile_config: Path
    profile: str
    input_type: str

    def __post_init__(self) -> None:
        path_must_exist(self.conf)

        # If input type is not entire organization, ws_csv must be provided
        if self.input_type != "entire-organization":
            path_must_exist(self.ws_csv)


@dataclass
class RestoreArgs:
    """Schema for restore management command line arguments."""

    ws_csv: Path
    conf: Path
    profile_config: Path
    profile: str

    def __post_init__(self) -> None:
        path_must_exist(self.ws_csv)
        path_must_exist(self.conf)
