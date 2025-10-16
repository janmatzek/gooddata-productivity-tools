# GD User Management

Tool which helps manage user entities in a GoodData organization.

Users can be created, updated, and deleted. This includes creation of any new userGroups which would be provided in user details.

## Usage

The tool requires the following argument on input:

- `user_csv` - a path to a CSV file defining user entities, their relevant attributes, userGroup memberships, and isActive state

### Optional arguments

The following optional arguments are available:

- `-d, --delimiter` - Column delimiter for the CSV files. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-d---delimiter) for details.
- `-i, --inner-delimiter` - UserGroups column value delimiter. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-i---inner-delimiter) for details.
- `-q, --quotechar` - Quotation character for escaping special characters. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-q---quotechar) for details.
- `-p, --profile-config` - Path to GoodData profile configuration file. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-p---profile-config) for details.
- `--profile` - Name of GoodData profile to use. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#--profile) for details.

Use the tool like so:

```sh
python scripts/user_mgmt.py user_csv
```

Where `user_csv` refers to the input CSV file.

If you would like to define custom delimiters, use the tool like so:

```sh
python scripts/user_mgmt.py user_csv -d "," -i "|"
```

To use a custom GoodData profile, use:

```sh
python scripts/user_mgmt.py user_csv -p path/to/profiles.yaml --profile customer
```

To show the help for using arguments, call:

```sh
python scripts/user_mgmt.py -h
```

## Input CSV file (user_csv)

The input CSV file defines the user entities which you might want to manage. Note that GD organization users that are not defined in the input will not be modified in any way.

[Example input CSV.](../examples/user_mgmt/input.csv)

The following CSV format is expected:

| user_id              | firstname | lastname | email                   | auth_id   | user_groups | is_active |
| -------------------- | --------- | -------- | ----------------------- | --------- | ----------- | --------- |
| jozef.mrkva          | jozef     | mrkva    | jozef.mrkva@test.com    | auth_id_1 |             | True      |
| bartolomej.brokolica |           |          |                         |           |             | False     |
| peter.pertzlen       | peter     | pertzlen | peter.pertzlen@test.com | auth_id_3 | ug_1, ug_2  | True      |
| zoltan.zeler         | zoltan    | zeler    | zoltan.zeler@test.com   | auth_id_4 | ug_1        | True      |
| kristian.kalerab     | kristian  | kalerab  |                         | auth_id_5 |             | True      |
| richard.cvikla       |           |          | richard.cvikla@test.com | auth_id_6 | ug_1, ug_2  | False     |
| adam.avokado         |           |          |                         | auth_id_7 |             | False     |

Here, each `user_id` is the ID of the user to manage.

The `firstname`, `lastname`, `email`, and `auth_id` fields are optional attributes of the user.

The `user_groups` field specifies user group memberships of the user.

Lastly, the `is_active` field holds boolean values containing information about whether the user should or should not exist in the organization.
