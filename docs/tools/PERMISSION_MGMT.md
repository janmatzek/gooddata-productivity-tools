# GD Workspace Permission Management

Tool which helps manage user/userGroup bound workspace permissions within GoodData organization.

Goal of the tool is to help manage state of the user-workspace or userGroup-workspace permission pairs in a granular fashion (one input row per each permission - e.g. `user_1 - ws_id_1 - "ANALYZE"`).

## Usage

The tool requires the following argument on input:

- `perm_csv` - a path to a CSV file defining workspace permissions bound to specific ws_id-user or ws_id-userGroup pairs and the permissions isActive state

### Optional arguments

The following optional arguments are available:

- `-d, --delimiter` - Column delimiter for the CSV files. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-d---delimiter) for details.
- `-q, --quotechar` - Quotation character for escaping special characters. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-q---quotechar) for details.
- `-p, --profile-config` - Path to GoodData profile configuration file. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-p---profile-config) for details.
- `--profile` - Name of GoodData profile to use. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#--profile) for details.

Use the tool like so:

```sh
python scripts/permission_mgmt.py perm_csv
```

Where `perm_csv` refers to the input CSV file.

If you would like to define custom delimiter, use the tool like so:

```sh
python scripts/permission_mgmt.py perm_csv -d ","
```

To use a custom GoodData profile, use:

```sh
python scripts/permission_mgmt.py perm_csv -p path/to/profiles.yaml --profile customer
```

To show the help for using arguments, call:

```sh
python scripts/permission_mgmt.py -h
```

## Input CSV file (perm_csv)

The input CSV file defines the workspace permissions which you might want to manage.

[Example input CSV.](../examples/permission_mgmt/input.csv)

The following CSV format is expected:

| user_id | ug_id | ws_id   | ws_permissions | is_active |
| ------- | ----- | ------- | -------------- | --------- |
| user_1  |       | ws_id_1 | ANALYZE        | True      |
| user_1  |       | ws_id_1 | VIEW           | False     |
| user_1  |       | ws_id_2 | MANAGE         | True      |
| user_2  |       | ws_id_1 | ANALYZE        | True      |
| user_2  |       | ws_id_2 | MANAGE         | True      |
|         | ug_1  | ws_id_1 | ANALYZE        | True      |
|         | ug_1  | ws_id_1 | VIEW           | True      |
|         | ug_1  | ws_id_1 | MANAGE         | False     |
|         | ug_2  | ws_id_1 | ANALYZE        | True      |
|         | ug_2  | ws_id_2 | MANAGE         | True      |

Here, each `user_id` is the ID of the user to manage, and `ug_id` is the ID of the user group to manage. Note that these fields are mutually exclusive and you should provide only one of the two values per each row.

The `ws_id` is the workspace ID that the permission is bound to.

Lastly, the `is_active` field holds boolean values containing information about whether the permission should or should not exist in the organization.
