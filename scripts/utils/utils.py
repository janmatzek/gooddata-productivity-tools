# (C) 2025 GoodData Corporation
"""This module contains general utility functions."""

import csv
import logging
import os
from pathlib import Path
from typing import Any, Generic, Protocol, Type, TypeVar, overload

logger = logging.getLogger(__name__)

TOKEN_ENV_VAR_NAME = "GDC_AUTH_TOKEN"
HOSTNAME_ENV_VAR_NAME = "GDC_HOSTNAME"


def read_csv_file_to_dict(
    file_path: Path, delimiter: str = ",", quotechar: str = '"'
) -> list[dict[str, Any]]:
    """Read a CSV file and return its content as a list of dictionaries.

    Args:
        file_path (Path): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file.
        quotechar (str): The quote character used in the CSV file.
    Returns:
        list[dict[str, Any]]: A list of dictionaries where each dictionary represents
        a row in the CSV file, with keys as column headers and values as row values.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file, delimiter=delimiter, quotechar=quotechar))


class SimpleClient(Protocol):
    """Protocol for GoodData Pipelines clients (Provisioners, Managers...)."""

    @classmethod
    def create(cls, host: str, token: str) -> "SimpleClient":
        pass

    @classmethod
    def create_from_profile(cls, profile: str, profiles_path: Path) -> "SimpleClient":
        pass


ConfigType = TypeVar("ConfigType")


class ConfiguredClient(Protocol, Generic[ConfigType]):
    """Protocol for clients requiring a configuration object."""

    @classmethod
    def create(
        cls, config: ConfigType, host: str, token: str
    ) -> "ConfiguredClient[ConfigType]":
        pass

    @classmethod
    def create_from_profile(
        cls, config: ConfigType, profile: str, profiles_path: Path
    ) -> "ConfiguredClient[ConfigType]":
        pass


SimpleT = TypeVar("SimpleT", bound="SimpleClient")
ConfiguredT = TypeVar("ConfiguredT", bound="ConfiguredClient[Any]")


@overload
def create_client(
    client_type: Type[SimpleT], profile_config: Path, profile: str
) -> SimpleT: ...


@overload
def create_client(
    client_type: Type[ConfiguredT],
    profile_config: Path,
    profile: str,
    config: ConfigType,
) -> ConfiguredT: ...


def create_client(
    client_type: Type[Any],
    profile_config: Path,
    profile: str,
    config: Any | None = None,
) -> Any:
    """Creates a GoodData Pipelines client.

    Depending on whether "config" is provided, the function will call the
    appropriate classmethod on the provided client type.
    """
    gdc_auth_token = os.environ.get(TOKEN_ENV_VAR_NAME)
    gdc_hostname = os.environ.get(HOSTNAME_ENV_VAR_NAME)

    if gdc_hostname and gdc_auth_token:
        if not gdc_hostname.strip() or not gdc_auth_token.strip():
            raise ValueError(
                f"Environment variables {HOSTNAME_ENV_VAR_NAME} and "
                f"{TOKEN_ENV_VAR_NAME} cannot be empty strings."
            )
        logger.info(f"Using {HOSTNAME_ENV_VAR_NAME} and {TOKEN_ENV_VAR_NAME} envvars.")
        if config is None:
            return client_type.create(host=gdc_hostname, token=gdc_auth_token)
        return client_type.create(
            config=config, host=gdc_hostname, token=gdc_auth_token
        )

    if os.path.exists(profile_config):
        logger.info(f"Using GoodData profile {profile} sourced from {profile_config}.")
        if config is None:
            return client_type.create_from_profile(
                profile=profile, profiles_path=profile_config
            )
        return client_type.create_from_profile(
            config=config, profile=profile, profiles_path=profile_config
        )

    raise RuntimeError(
        "No GoodData credentials provided. Please export required ENVVARS "
        f"({HOSTNAME_ENV_VAR_NAME}, {TOKEN_ENV_VAR_NAME}) or provide path to GD profile config."
    )
