# Storage Configuration Reference

This document provides detailed information about configuring storage backends for backup and restore operations.

## Overview

The backup and restore tools support multiple storage backends for saving and retrieving workspace backups. Currently supported storage types are:

- **AWS S3** - Store backups in Amazon S3 buckets
- **Local** - Store backups in the local filesystem

The storage configuration is defined in a YAML configuration file that you pass to the backup or restore tool.

---

## Configuration File Format

The basic structure of a storage configuration file is:

```yaml
storage_type: <storage_type>
storage:
  # Storage-specific configuration options
```

Additional optional parameters may be available depending on the tool (e.g., `api_page_size`, `batch_size` for backup operations).

---

## AWS S3 Configuration

### Basic Configuration

```yaml
storage_type: s3
storage:
  bucket: your-backup-bucket
  backup_path: path/to/backups/
```

### Full Configuration with Optional Parameters

```yaml
storage_type: s3
storage:
  bucket: your-backup-bucket
  backup_path: path/to/backups/
  profile: services
  aws_access_key_id: your-access-key-id
  aws_secret_access_key: your-secret-access-key
  aws_default_region: us-east-1
```

### Field Descriptions

| Field                   | Required | Description                                                         |
| ----------------------- | -------- | ------------------------------------------------------------------- |
| `bucket`                | Yes      | S3 bucket name containing the backups                               |
| `backup_path`           | Yes      | Absolute path within the S3 bucket to the root directory of backups |
| `profile`               | No       | AWS profile name to use (from `~/.aws/credentials`)                 |
| `aws_access_key_id`     | No       | AWS access key ID for authentication                                |
| `aws_secret_access_key` | No       | AWS secret access key for authentication                            |
| `aws_default_region`    | No       | AWS region where the bucket is located                              |

### AWS Authentication

The tools follow the standard [boto3 credential resolution](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) process. You can provide credentials through:

1. Configuration file (as shown above)
2. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
3. AWS credentials file (`~/.aws/credentials`)
4. IAM roles (when running on AWS infrastructure)

For detailed AWS authentication setup, see the main [README AWS section](../README.md#aws).

### Example: Backup to S3

**Configuration file (s3_config.yaml):**

```yaml
storage_type: s3
storage:
  bucket: my-gooddata-backups
  backup_path: production/backups/
  profile: production-aws
```

**Usage:**

```sh
python scripts/backup.py workspaces.csv s3_config.yaml
```

---

## Local Storage Configuration

### Configuration

```yaml
storage_type: local
storage:
```

### Behavior

- **Backup operations:** Backups are saved to `./local_backups/` directory relative to where the script is executed
- **Restore operations:** Backups are read from `./local_backups/` directory relative to where the script is executed

**Note:** For backup operations, the number of existing backups in the `./local_backups/` folder may affect script performance.

### Example: Backup to Local Storage

**Configuration file (local_config.yaml):**

```yaml
storage_type: local
storage:
```

**Usage:**

```sh
python scripts/backup.py workspaces.csv local_config.yaml
```

This will create backups in `./local_backups/` in your current working directory.

---

## Backup-Specific Configuration Options

When using the backup tool, additional configuration options are available:

### API Page Size

Controls the batch size when fetching workspace IDs from the GoodData API (used with `list-of-parents` or `entire-organization` input types).

**Default:** `100`

```yaml
storage_type: s3
storage:
  bucket: my-bucket
  backup_path: backups/
api_page_size: 200
```

### Batch Size

Determines how many workspaces are processed before saving the backups to storage.

**Default:** `100`

```yaml
storage_type: s3
storage:
  bucket: my-bucket
  backup_path: backups/
batch_size: 50
```

### Complete Example

```yaml
storage_type: s3
storage:
  bucket: gooddata-prod-backups
  backup_path: org_123/backups/
  profile: production
  aws_default_region: eu-west-1
api_page_size: 150
batch_size: 25
```

---

## Configuration File Examples

Example configuration files can be found in:

- [examples/backup_and_restore/configuration_s3.yaml](../examples/backup_and_restore/configuration_s3.yaml)
- [examples/backup_and_restore/configuration_local.yaml](../examples/backup_and_restore/configuration_local.yaml)

---

## Troubleshooting

### S3 Access Issues

If you encounter permission errors when accessing S3:

1. Verify your AWS credentials are correctly configured
2. Ensure the IAM user/role has appropriate S3 permissions:
   - `s3:GetObject` (for restore)
   - `s3:PutObject` (for backup)
   - `s3:ListBucket` (for both)
3. Check that the bucket name and region are correct
4. Verify the `backup_path` exists and is accessible

### Local Storage Issues

If backups fail with local storage:

1. Ensure you have write permissions in the current directory
2. Check available disk space
3. Verify the `./local_backups/` directory can be created

For additional help, check the tool-specific documentation:

- [Backup Tool Documentation](../tools/BACKUP.md)
- [Restore Tool Documentation](../tools/RESTORE.md)
