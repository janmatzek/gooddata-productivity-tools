# (C) 2025 GoodData Corporation

import csv
from pathlib import Path

from gooddata_pipelines import UserIncrementalLoad, UserProvisioner
from utils.args.parser import Parser
from utils.logger import get_logger, setup_logging
from utils.utils import create_client

setup_logging()
logger = get_logger(__name__)


def read_users_from_csv(
    path_to_csv: Path, row_delimiter: str, quotechar: str, user_group_delimiter: str
) -> list[UserIncrementalLoad]:
    """Reads users from csv file."""

    users: list[UserIncrementalLoad] = []

    with open(path_to_csv, "r") as f:
        reader = csv.DictReader(
            f, delimiter=row_delimiter, quotechar=quotechar, skipinitialspace=True
        )
        for row in reader:
            try:
                user_id = row["user_id"]
                firstname = row["firstname"]
                lastname = row["lastname"]
                email = row["email"]
                auth_id = row["auth_id"]
                user_groups = row["user_groups"].split(user_group_delimiter)
                is_active = row["is_active"] == "True"

                user = UserIncrementalLoad(
                    user_id=user_id,
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    auth_id=auth_id,
                    user_groups=user_groups,
                    is_active=is_active,
                )

            except Exception as e:
                logger.error(f'Unable to load following row: "{row}". Error: "{e}"')
                continue

            users.append(user)

    return users


def user_mgmt() -> None:
    """Main function for user management."""

    args = Parser.parse_user_args()

    users = read_users_from_csv(
        args.user_csv, args.delimiter, args.quotechar, args.inner_delimiter
    )

    provisioner = create_client(UserProvisioner, args.profile_config, args.profile)

    provisioner.logger.subscribe(logger)

    provisioner.incremental_load(users)


if __name__ == "__main__":
    user_mgmt()
