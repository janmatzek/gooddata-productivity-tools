# (C) 2025 GoodData Corporation

from typing import Any

from gooddata_pipelines import UserDataFilterFullLoad, UserDataFilterProvisioner
from utils.args.parser import Parser
from utils.logger import get_logger, setup_logging
from utils.utils import (
    create_client,
    read_csv_file_to_dict,
)

# Setup logging
setup_logging()
logger = get_logger(__name__)


def validate_user_data_filter_data(
    raw_user_data_filters: list[dict[str, Any]],
) -> list[UserDataFilterFullLoad]:
    """Validate workspace against input model."""
    validated_user_data_filters: list[UserDataFilterFullLoad] = []
    for raw_user_data_filter in raw_user_data_filters:
        validated_user_data_filter = UserDataFilterFullLoad(
            workspace_id=raw_user_data_filter["workspace_id"],
            udf_id=raw_user_data_filter["udf_id"],
            udf_value=raw_user_data_filter["udf_value"],
        )

        validated_user_data_filters.append(validated_user_data_filter)

    return validated_user_data_filters


def udf_mgmt():
    """Main function for workspace management."""

    # Create parser and parse arguments
    args = Parser.parse_user_data_filter_args()

    # Read CSV input
    raw_user_data_filters = read_csv_file_to_dict(
        args.filepath, args.delimiter, args.quotechar
    )

    # Validate user data filter data
    validated_user_data_filters = validate_user_data_filter_data(raw_user_data_filters)

    # Create provisioner and subscribe to logger
    provisioner: UserDataFilterProvisioner = create_client(
        UserDataFilterProvisioner, args.profile_config, args.profile
    )

    provisioner.set_ldm_column_name(args.ldm_column_name)
    provisioner.set_maql_column_name(args.maql_column_name)

    provisioner.logger.subscribe(logger)

    # Incremental load user data filters
    provisioner.full_load(validated_user_data_filters)


if __name__ == "__main__":
    # Main function
    udf_mgmt()
