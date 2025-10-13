# BSD License
#
# Copyright (c) 2024, GoodData Corporation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted, provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from typing import Any

from gooddata_pipelines import (
    UserGroupIncrementalLoad,
    UserGroupProvisioner,
)
from utils.args.parser import Parser
from utils.args.schemas import UserGroupArgs
from utils.logger import get_logger, setup_logging
from utils.utils import create_client, read_csv_file_to_dict

setup_logging()
logger = get_logger(__name__)


def read_users_groups_from_csv(
    args: UserGroupArgs,
) -> list[UserGroupIncrementalLoad]:
    """Reads users from csv file."""
    user_groups: list[UserGroupIncrementalLoad] = []
    raw_user_groups = read_csv_file_to_dict(
        args.user_group_csv, args.delimiter, args.quotechar
    )
    for raw_user_group in raw_user_groups:
        processed_user_group: dict[str, Any] = dict(raw_user_group)
        parent_user_groups = raw_user_group["parent_user_groups"]

        if parent_user_groups:
            processed_user_group["parent_user_groups"] = parent_user_groups.split(
                args.inner_delimiter
            )
        else:
            processed_user_group["parent_user_groups"] = []

        try:
            user_group = UserGroupIncrementalLoad.model_validate(processed_user_group)
            user_groups.append(user_group)
        except Exception as e:
            logger.error(
                f'Unable to load following row: "{raw_user_group}". Error: "{e}"'
            )
            continue
    return user_groups


def user_group_mgmt():
    """Main function for user management."""

    args = Parser.parse_user_group_args()

    try:
        provisioner = create_client(
            UserGroupProvisioner, args.profile_config, args.profile
        )

        provisioner.logger.subscribe(logger)

        validated_user_groups = read_users_groups_from_csv(args)

        provisioner.incremental_load(validated_user_groups)

    except RuntimeError as e:
        logger.error(f"Runtime error has occurred: {e}")


if __name__ == "__main__":
    user_group_mgmt()
