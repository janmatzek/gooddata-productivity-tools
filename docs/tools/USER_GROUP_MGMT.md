# GD User Group Management

This tool facilitates the management of user groups within a GoodData organization. It supports the creation, updating, and deletion of user groups, including the assignment of parent user groups as defined in the input details.

## Usage

The tool requires the following argument:

- `user_group_csv` - a path to a CSV file that defines the user groups, their names, parent user groups, and active status.

### Optional arguments

The following optional arguments are available:

- `-d, --delimiter` - Column delimiter for the CSV files. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-d---delimiter) for details.
- `-i, --inner-delimiter` - Delimiter for parent user groups within a column. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-i---inner-delimiter) for details.
- `-q, --quotechar` - Quotation character for escaping special characters. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-q---quotechar) for details.
- `-p, --profile-config` - Path to GoodData profile configuration file. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-p---profile-config) for details.
- `--profile` - Name of GoodData profile to use. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#--profile) for details.

Use the tool like so:

```sh
python scripts/user_group_mgmt.py user_group_csv
```

Where `user_group_csv` refers to the input CSV file.

For custom delimiters, use the command:

```sh
python scripts/user_group_mgmt.py user_group_csv -d "," -i "|"
```

To use a custom GoodData profile, use:

```sh
python scripts/user_group_mgmt.py user_group_csv -p path/to/profiles.yaml --profile customer
```

To display help for using arguments, run:

```sh
python scripts/user_group_mgmt.py -h
```

## Input CSV File (`user_group_csv`)

The input CSV file defines the user groups to be managed. User groups not defined in the input file will not be modified.

[Example input CSV.](../examples/user_group_mgmt/input.csv)

The following CSV format is expected:

| user_group_id | user_group_name | parent_user_groups | is_active |
| ------------- | --------------- | ------------------ | --------- |
| ug_1          | Admins          |                    | True      |
| ug_2          | Developers      | ug_1               | True      |
| ug_3          | Testers         | ug_1, ug_2         | True      |
| ug_4          | TemporaryAccess | ug_2               | False     |

Here, each `user_group_id` is the unique identifier for the user group.

The `user_group_name` field is an optional name for the user group, defaulting to the ID if not provided.

The `parent_user_groups` field specifies the parent user groups, defining hierarchical relationships.

The `is_active` field holds boolean values containing information about whether the user group should exist or be deleted from the organization.
