# GD Workspace Backup

Tool which exports / creates a backup of one or more workspaces - their logical data model (LDM), analytical model (AM), user data filters (UDF), filter views and automations. Backups are stored either locally or can be uploaded to an S3 bucket.

## Usage

The tool requires the following arguments on input:

- `ws_csv` - a path to a CSV file defining workspace IDs to back up (required unless using `entire-organization` input type)
- `conf` - a path to a configuration file containing information required for accessing the backup storage

### Input type

The `input-type` argument is optional and has three options:

`list-of-workspaces` is the default option. The data in the input file is treated as an exhaustive list of workspaces to back up. This is also what will happen if the argument is omitted entirely

Use `list-of-parents` when the input file contains a list of parent workspaces and you wish to back up the entire hierarchy. For each workspace ID in the input, all of its direct and indirect children are included in the backup, as well as the parent workspaces themselves.

If the `entire-organization` option is selected, the script will back up all the workspaces within the organization. If this option is selected, you do not need to provide the `ws_csv` argument as it will be ignored. If a `ws_csv` value is provided, the script will log a warning message, but will proceed to back up the organization.

### Usage examples

If you want to back up a list of specific workspaces, run:

```sh
python scripts/backup.py ws_csv conf
```

Where `ws_csv` refers to the input CSV file and `conf` to the configuration file in YAML format. This would be equivalent to running:

```sh
python scripts/backup.py ws_csv conf -t list-of-workspaces
```

For example, if you have a CSV file named "example_input.csv" in the folder from which you are executing the Python command and a configuration file named "example_conf.yaml" in a subfolder named "subfolder", the execution could look like this:

```sh
python scripts/backup.py example_input.csv subfolder/example_conf.yaml
```

If you want to back up a specific hierarchy under a parent workspace, prepare the list of parents, store it in a CSV file (named for example `parents.csv`) and run:

```sh
python scripts/backup.py parents.csv conf.yaml -t list-of-parents
```

If you want to back up all the workspaces in the organization, run:

```sh
python scripts/backup.py conf.yaml -t entire-organization
```

Note that in this case, you do not need to provide the `ws_csv` argument as no list is required.

To show the help for using arguments, call:

```sh
python scripts/backup.py -h
```

### Optional arguments

The following optional arguments are available:

- `-t, --input-type` - Specification of how the input file is handled. Options: `list-of-workspaces` (default), `list-of-parents`, `entire-organization`. See the Input Type section above for details.
- `-p, --profile-config` - Path to GoodData profile configuration file. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-p---profile-config) for details.
- `--profile` - Name of GoodData profile to use. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#--profile) for details.

Example with optional arguments:

```sh
python scripts/backup.py input.csv conf.yaml -t list-of-parents -p path/to/profiles.yaml --profile customer
```

## Configuration file (conf)

The configuration file defines which type of storage the export tool will save the backups to, and any additional storage-specific information that might be required. Currently AWS S3 and local storage are supported.

### Backup-Specific Options

If you run the script with `list-of-parents` or `entire-organization`, the script will fetch the IDs of workspaces to process in batches. You can configure:

- `api_page_size` - Batch size for fetching workspace IDs from the GoodData API. Default: `100`
- `batch_size` - Number of workspaces to process before saving backups to storage. Default: `100`

### Configuration Format

```yaml
storage_type: s3 # or 'local'
storage:
  # Storage-specific configuration (see Storage Config documentation)
api_page_size: 1000 # optional
batch_size: 20 # optional
```

### Storage Configuration

For detailed information on configuring AWS S3 or local storage, including all available options and examples, see the [Storage Configuration Reference](../reference/STORAGE_CONFIG.md).

**Quick examples:**

**S3 Storage:**

```yaml
storage_type: s3
storage:
  bucket: my-backup-bucket
  backup_path: backups/
```

**Local Storage:**

```yaml
storage_type: local
storage:
```

See [../examples/backup_and_restore](../examples/backup_and_restore/) for complete configuration file examples.

## Input CSV file (ws_csv)

The input CSV file defines the targets and sources for backup restores (imports).

The following CSV format is expected:

| workspace_id |
| ------------ |
| ws_id_1      |
| ws_id_2      |
| ws_id_3      |

Here, each `workspace_id` is the workspace ID of the workspace to perform the export on.
If the defined workspace does not exit in the target organization, this information will be present as ERROR log. If something fails, please read over all ERROR log messages for information where the issue lies.

You can find an example of the input file ([backup_input.csv](../examples/backup_and_restore/backup_input.csv)) in _docs/../examples/backup_and_restore_.
