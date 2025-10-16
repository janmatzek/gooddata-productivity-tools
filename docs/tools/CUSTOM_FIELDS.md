# Custom Field Management

The `scripts/custom_fields.py` script will allow you to extend the Logical Data Model (LDM) of a child workspace by adding extra datasets which are not present in the parent workspaces' LDM.

## Input files

The script works with input from two CSV files. These files should contain (a) custom dataset definitions and (b) custom field definitions.

The custom dataset defines the dataset entity, i.e., the box you would see in the GoodData Cloud UI. The custom fields, on the other hand, define the individual fields in that dataset. You can imagine it as first defining a table and then its columns.

Multiple datasets and fields can be defined in the files. However, the files need to be consistent with each other - you cannot define fields form datasets that are not defined in the datasets file.

### Custom dataset definitions

The first contains the definitions of the datasets you want to create. It should have following structure:

| workspace_id         | dataset_id        | dataset_name         | dataset_datasource_id | dataset_source_table | dataset_source_sql | parent_dataset_reference | parent_dataset_reference_attribute_id | dataset_reference_source_column | dataset_reference_source_column_data_type | wdf_id | wdf_column_name |
| -------------------- | ----------------- | -------------------- | --------------------- | -------------------- | ------------------ | ------------------------ | ------------------------------------- | ------------------------------- | ----------------------------------------- | ------ | --------------- |
| child_workspace_id_1 | custom_dataset_id | Custom Dataset Title | datasource_id         | dataset_source_table |                    | parent_dataset_id        | parent_dataset.reference_field        | custom_dataset.reference_field  | column data type                          | wdf_id | wdf_column_name |

#### Validity constraints

- The `dataset_source_table` and `dataset_source_sql` are mutually exclusive. Only one of those should be filled in, the other should be null (empty value). In case both values are present, the script will throw an error.

- `workspace_id` + `dataset_id` combination must be unique across all dataset definitions.

#### Description and Example Values

Below is a description of each field present in the custom dataset definition CSV. Use the table for guidance on what values to use in your file, and refer to the Example Value column for clarity. Each column must be filled in according to the requirements outlined.

| Field                                       | Example Value              | Description                                                                                                     |
| ------------------------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `workspace_id`                              | child_workspace_id_1       | Child workspace id                                                                                              |
| `dataset_id`                                | custom_dataset_id          | Custom dataset id                                                                                               |
| `dataset_name`                              | Custom Dataset Title       | Custom dataset name                                                                                             |
| `dataset_datasource_id`                     | datasource_id              | Data source id (can be found in UI under "manage files")                                                        |
| `dataset_source_table`                      | dataset_source_table       | Name of the table in the physical data model                                                                    |
| `dataset_source_sql`                        | _(leave empty or provide)_ | SQL query defining the dataset (should be empty if above is filled)                                             |
| `parent_dataset_reference`                  | products                   | ID of the parent dataset to which this custom dataset will be connected                                         |
| `parent_dataset_reference_attribute_id`     | products.product_id        | Parent dataset column name used for the "join"                                                                  |
| `dataset_reference_source_column`           | product_id                 | Custom dataset column name used for the "join"                                                                  |
| `dataset_reference_source_column_data_type` | STRING                     | See [ColumnDataType](https://www.gooddata.com/docs/python-sdk/latest/pipelines/ldm_extension/#customfieldtype). |
| `wdf_id`                                    | x\_\_client_id             | Workspace data filter id                                                                                        |
| `wdf_column_name`                           | client_id                  | Name of the column used for filtering                                                                           |

### Custom fields definition

The individual files of the custom dataset are defined thusly:

| workspace_id         | dataset_id        | cf_id           | cf_name           | cf_type   | cf_source_column           | cf_source_column_data_type |
| -------------------- | ----------------- | --------------- | ----------------- | --------- | -------------------------- | -------------------------- |
| child_workspace_id_1 | custom_dataset_id | custom_field_id | Custom Field Name | attribute | custom_field_source_column | INT                        |

#### Validity constraints

The custom field definitions must comply with these criteria:

- **attributes** and **facts**: unique `workspace_id` + `cf_id` combinations
- **dates**: unique `dataset_id` and `cf_id` combinations

#### Description and Example Values

Below is a description of each field present in the custom dataset definition CSV. Use the table for guidance on what values to use in your file, and refer to the Example Value column for clarity. Each column must be filled in according to the requirements outlined.

| Field                        | Example Value              | Description                                                                                                     |
| ---------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `workspace_id`               | child_workspace_id_1       | Child workspace ID                                                                                              |
| `dataset_id`                 | custom_dataset_id          | Custom dataset ID                                                                                               |
| `cf_id`                      | custom_field_id            | Custom field ID                                                                                                 |
| `cf_name`                    | Custom Field Name          | Custom field name                                                                                               |
| `cf_type`                    | attribute                  | See [CustomFieldType](https://www.gooddata.com/docs/python-sdk/latest/pipelines/ldm_extension/#customfieldtype) |
| `cf_source_column`           | custom_field_source_column | Name of the column in the physical data model                                                                   |
| `cf_source_column_data_type` | INT                        | See [ColumnDataType](https://www.gooddata.com/docs/python-sdk/latest/pipelines/ldm_extension/#customfieldtype)  |

## Usage

The script requires two positional arguments, which represent the paths to the input files discussed above:

```shell
python scripts/custom_fields.py custom_datasets.csv custom_fields.csv
```

### Optional arguments

The following optional arguments are available:

- `-d, --delimiter` - Column delimiter for the CSV files. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-d---delimiter) for details.
- `-q, --quotechar` - Quotation character for escaping special characters. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-q---quotechar) for details.
- `-p, --profile-config` - Path to GoodData profile configuration file. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-p---profile-config) for details.
- `--profile` - Name of GoodData profile to use. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#--profile) for details.
- `--no-relations-check` - Skip relations check after updating LDM. If used, the script will not verify object relations or perform rollback if issues are found.

Example with optional arguments:

```shell
python scripts/custom_fields.py custom_datasets.csv custom_fields.csv -p path/to/profiles.yaml --profile customer --no-relations-check
```

### Check valid relations

Regardless of whether the flag is used or not, the script will always start by loading and validating the data from the provided files. The script will then iterate through workspaces.

#### If unused

If `--no-relations-check` is not used, the script will:

1. Store current workspace layout (analytical objects and LDM).
1. Check whether relations of metrics, visualizations and dashboards are valid. A set of current objects with invalid relations is created.
1. Push the updated LDM to GoodData Cloud.
1. Check object relations again. New set of objects with invalid relations is created.
1. The sets are compared.
   - If there is more objects with invalid references in the new set, it means the objects were invalidated. Rollback is required.
   - If the sets are not equal, rollback might be required
   - If there is fewer invalid references or the sets are equal, rollback is not required
1. In case rollback is required, the initally stored workspace layout will be pushed to GoodData Cloud again, reverting changes to the workspace.

#### If used

If you decide to use the `--no-relations-check` flag, the script will simply validate the data and push the LDM extension to GoodData Cloud without any additional checks or rollbacks.

```shell
python scripts/custom_fields.py custom_datasets.csv custom_fields.csv --no-relations-check
```
