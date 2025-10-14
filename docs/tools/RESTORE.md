# GD Workspace Restore

Tool which restores one or more workspace analytical models (AM), logical data models (LDM), user data filters (UDF), filter views and automations from source backup archives in an incremental manner.

The backups contain declarative definitions of AM, LDM and UDFs which are unarchived, loaded into memory and finally put into the target GD workspace.

The restores are workspace-agnostic, which means that if you need to, you can import a backed-up of one workspace into a different workspace.

## Usage

The tool requires the following arguments on input:

- `ws_csv` - a path to a CSV file defining target workspace IDs to restore to, and backup source paths
- `conf` - a path to a configuration file containing information required for accessing the backup source storage

Use the tool like so:

```sh
python scripts/restore.py ws_csv conf
```

Where `ws_csv` refers to the input CSV file and `conf` to the configuration file in YAML format.

For example, if you have a CSV file named "example_input.csv" in the folder from which you are executing the Python command and a configuration file named "example_conf.yaml" in a subfolder named "subfolder", the execution could look like this:

```sh
python scripts/restore.py example_input.csv subfolder/example_conf.yaml
```

To show the help for using arguments, call:

```sh
python scripts/restore.py -h
```

### Optional arguments

The following optional arguments are available:

- `-p, --profile-config` - Path to GoodData profile configuration file. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#-p---profile-config) for details.
- `--profile` - Name of GoodData profile to use. See [Common Arguments](../reference/COMMON_ARGUMENTS.md#--profile) for details.

Example with optional arguments:

```sh
python scripts/restore.py input.csv conf.yaml -p path/to/profiles.yaml --profile customer
```

## Configuration file (conf)

The configuration file defines which type of storage the restore tool will source the backups from, and any additional storage-specific information that might be required. Currently AWS S3 and local storage are supported.

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

| workspace_id | path             |
| ------------ | ---------------- |
| ws_id_1      | path/to/backup_1 |
| ws_id_2      | path/to/backup_2 |
| ws_id_3      | path/to/backup_1 |

Here, each `workspace_id` is the workspace ID of the workspace to perform the restore to. The `path` is the path (e.g. in S3) to a directory which contains the target backup archive (`gooddata_layouts.zip`).

The `path` is then prefixed with a additional information (e.g. S3 bucket and backup_path to backups root dir).

You can find an example of the input file ([restore_input.csv](../examples/backup_and_restore/restore_input.csv)) in _docs/../examples/backup_and_restore_.

If something fails, please read over all ERROR log messages for information where the issue lies.
