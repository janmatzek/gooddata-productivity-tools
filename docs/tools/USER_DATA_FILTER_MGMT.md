# GD User Data Filter Management

Tool which helps manage User Data Filters in a GoodData organization.

User Data Filters can be created, updated, and deleted based on CSV input.

## Usage

The tool requires the following arguments on input:

- `filepath` - a path to a CSV file defining user data filters, their values, and target workspace
- `ldm_column_name` - LDM column name
- `maql_column_name` - MAQL column name in the form `{attribute/dataset.field}`

### Optional arguments

The following optional arguments are available:

- `-d, --delimiter` - Column delimiter for the CSV files. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-d---delimiter) for details.
- `-q, --quotechar` - Quotation character for escaping special characters. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-q---quotechar) for details.
- `-p, --profile-config` - Path to GoodData profile configuration file. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-p---profile-config) for details.
- `--profile` - Name of GoodData profile to use. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#--profile) for details.

Use the tool like so:

```sh
python scripts/user_data_filter_mgmt.py path/to/udfs.csv ldm_column_name maql_column_name
```

If you would like to define custom delimiters, use the tool like so:

```sh
python scripts/user_data_filter_mgmt.py path/to/udfs.csv ldm_column_name maql_column_name -d ","
```

To use a custom GoodData profile, use:

```sh
python scripts/user_data_filter_mgmt.py path/to/udfs.csv ldm_column_name maql_column_name -p path/to/profiles.yaml --profile customer
```

To show the help for using arguments, call:

```sh
python scripts/user_data_filter_mgmt.py -h
```

## Input CSV file

The input CSV file defines the user data filter values to be managed. All user data filters in all workspaces listed in the input will be overwritten based on the CSV content.

The following CSV format is expected:

| workspace_id              | udf_id    | udf_value |
| ------------------------- | --------- | --------- |
| workspace_with_wdf_values | user_id_1 | 1         |
| workspace_with_wdf_values | user_id_2 | 2         |

Here, each `workspace_id` is the ID of the workspace where the user data filter applies.

The `user_data_filter_id` identifies the specific User Data Filter you want to assign or update for the given workspace. Should be equal to the ID of the user the UDF is applied to.

The `udf_value` field specifies the value to be set for that User Data Filter.
