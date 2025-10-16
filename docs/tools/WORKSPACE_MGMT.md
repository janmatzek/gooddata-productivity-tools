# GD Workspace Management

Tool which helps manage child workspace entities in a GoodData organization.

Workspaces can be created, updated, and deleted. This includes applying Workspace Data Filter values, when provided in input.

## Usage

The tool requires the following argument on input:

- `filepath` - a path to a CSV file defining workspace entities, their relevant attributes, workspace data filter configuration, and isActive state

### Optional arguments

The following optional arguments are available:

- `-d, --delimiter` - Column delimiter for the CSV files. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-d---delimiter) for details.
- `-i, --inner-delimiter` - Workspace Data Filter values column delimiter. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-i---inner-delimiter) for details.
- `-q, --quotechar` - Quotation character for escaping special characters. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-q---quotechar) for details.
- `-p, --profile-config` - Path to GoodData profile configuration file. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-p---profile-config) for details.
- `--profile` - Name of GoodData profile to use. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#--profile) for details.

Use the tool like so:

```sh
python scripts/workspace_mgmt.py path/to/workspace_definitions.csv
```

If you would like to define custom delimiters, use the tool like so:

```sh
python scripts/workspace_mgmt.py path/to/workspace_definitions.csv -d "," -i "|"
```

To use a custom GoodData profile, use:

```sh
python scripts/workspace_mgmt.py path/to/workspace_definitions.csv -p path/to/profiles.yaml --profile customer
```

To show the help for using arguments, call:

```sh
python scripts/workspace_mgmt.py -h
```

## Input CSV file

The input CSV file defines the workspace entities which you might want to manage. Note that GD organization workspaces that are not defined in the input will not be modified in any way.

The following CSV format is expected:

| parent_id           | workspace_id                 | workspace_name               | workspace_data_filter_id | workspace_data_filter_values | is_active |
| ------------------- | ---------------------------- | ---------------------------- | ------------------------ | ---------------------------- | --------- |
| parent_workspace_id | workspace_with_wdf_values    | Workspace With WDF Values    | wdf_id                   | 1&#124;2&#124;3              | true      |
| parent_workspace_id | workspace_without_wdf_values | Workspace Without WDF Values |                          |                              | true      |

Here, each `workspace_id` is the ID of the workspace to manage.

The `parent_id` specifies the parent workspace under which the workspace should be placed.

The `workspace_name` field specifies the display name of the workspace.

The `workspace_data_filter_id` and `workspace_data_filter_values` fields specify Workspace Data Filter configuration. Leave `workspace_data_filter_values` empty if no values should be set.

Lastly, the `is_active` field holds boolean values containing information about whether the workspace should or should not exist in the organization.
