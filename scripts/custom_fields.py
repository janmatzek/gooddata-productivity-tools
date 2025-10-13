# (C) 2025 GoodData Corporation
"""Top level script to manage custom datasets and fields in GoodData Cloud.

This script allows you to extend the Logical Data Model (LDM) of a child workspace.
Documentation and usage instructions are located in `docs/CUSTOM_FIELDS.md` file.
"""

from gooddata_pipelines import (
    CustomDatasetDefinition,
    CustomFieldDefinition,
    LdmExtensionManager,
)
from utils.args.parser import Parser
from utils.args.schemas import CustomFieldsArgs
from utils.logger import get_logger, setup_logging
from utils.utils import (
    create_client,
    read_csv_file_to_dict,
)

setup_logging()
logger = get_logger(__name__)


def custom_fields() -> None:
    """Main function to run the custom fields script."""

    args: CustomFieldsArgs = Parser.parse_custom_fields_args()

    # Load input data from csv files
    raw_custom_datasets: list[dict[str, str]] = read_csv_file_to_dict(
        args.path_to_custom_datasets_csv, args.delimiter, args.quotechar
    )

    custom_datasets = [
        CustomDatasetDefinition.model_validate(raw_custom_dataset)
        for raw_custom_dataset in raw_custom_datasets
    ]

    raw_custom_fields: list[dict[str, str]] = read_csv_file_to_dict(
        args.path_to_custom_fields_csv, args.delimiter, args.quotechar
    )

    custom_fields = [
        CustomFieldDefinition.model_validate(raw_custom_field)
        for raw_custom_field in raw_custom_fields
    ]

    # Create instance of CustomFieldManager with host and token
    manager = create_client(LdmExtensionManager, args.profile_config, args.profile)

    # Subscribe to logs
    manager.logger.subscribe(logger)

    # Process the custom datasets and fields
    manager.process(custom_datasets, custom_fields, args.check_relations)


if __name__ == "__main__":
    custom_fields()
