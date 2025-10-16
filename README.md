# gooddata-productivity-tools

This repository contains tools that help with GoodData Cloud/CN workspace management, user and user group management, and backup/restore of workspaces.

This section of the documentation contains information on how to set up the environment and relevant authentication files. At the end of the Tools section, there is more specific documentation for each tool. The steps mentioned here are shared between them.

## Requirements

Python 3.11

Depending on your environment, the statements can start either as

```sh
pip
pip3
```

```sh
python
python3
```

please use the one that works for you and refers to Python 3.11.

The version can be checked by running

```sh
python -V
```

## Install

In order to install tooling requirements to the target environment, run the following:

```sh
pip install -r requirements.txt
```

## Authentication

The scripts follow standard credential/authentication conventions for GoodData and storage providers (e.g., AWS).

### Quick Overview

**GoodData Authentication:**

- Environment variables: `GDC_AUTH_TOKEN` and `GDC_HOSTNAME`
- Profile file: `~/.gooddata/profiles.yaml` (supports multiple profiles)
- Tools use the `default` profile by default
- Environment variables take precedence over profile files

**AWS Authentication:**

- Follows [boto3 credential resolution](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)
- Common method: AWS credentials file at `~/.aws/credentials`
- See tool-specific docs for profile selection

### Detailed Setup

For step-by-step instructions on creating and configuring authentication files, including file formats and examples, see the [Authentication Setup Guide](docs/guides/SETUPAUTHENTICATION.md).

## Tools

- [Backup workspace](docs/tools/BACKUP.md)
- [Restore workspace](docs/tools/RESTORE.md)
- [Workspace management](docs/tools/WORKSPACE_MGMT.md)
- [Workspace permission management](docs/tools/PERMISSION_MGMT.md)
- [User management](docs/tools/USER_MGMT.md)
- [User group management](docs/tools/USER_GROUP_MGMT.md)
- [User data filter management](docs/tools/USER_DATA_FILTER_MGMT.md)
- [Custom fields management](docs/tools/CUSTOM_FIELDS.md)

### Reference Documentation

- [Common Arguments Reference](docs/reference/COMMON_ARGUMENTS.md) - Detailed explanations of shared CLI arguments
- [Storage Configuration Reference](docs/reference/STORAGE_CONFIG.md) - Guide to configuring S3 and local storage backends

## Known MacOS issue SSL: CERTIFICATE_VERIFY_FAILED

If you are getting the following message:

`Caused by SSLError(SSLCertVerificationError(1, ‘[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1129)'))`

it is likely caused by Python and it occurs if you have installed Python directly from python.org.

To mitigate, please install your SSL certificates in HD -> Applications -> Python -> Install Certificates.command.

---

## Development

This section is aimed towards developers wanting to adjust / test the code. If you are regular user you can ignore following parts.

### Setup

To set up local development environment do the following:

1. (optional) Set up a local python virtual environment:

```sh
    python -m venv venv
    source venv/bin/activate
```

2. Install tool, dev, and test requirements:

```sh
pip install -r requirements.txt -r requirements-test.txt -r requirements-dev.txt
```

### Style checking, linting, and typing

The codebase (both, scripts and tests) is style, lint, and type checked when the CI/CD pipeline runs.

Linting and style-checking is done with help of `black` and `ruff`.

Type checking is done using `mypy`.

To run either of the mentioned tools locally, just call the tool with a target directory.

```sh
<black|ruff|mypy> <target_path>
```

For example, in order to check the typing in the scripts, call the following from the repository's root directory:

```sh
mypy scripts
```

To check that the code styling will pass pre-merge checks when creating a pull request, run:

```sh
tox -e lint
```

### Testing

The tooling test suite makes use of some third party tools, such as `pytest`, `tox`, and `moto`.

To run the test suite locally, ensure you have test and script requirements installed (see Setup step above) change working directory to repository's root and then call:

```sh
pytest .
```

### Tox

The pre-merge checks run via GitHub actions use tox to verify the code style and test cases.

To run the test suite, linters and type checks locally you can also use `tox`.

To check everything at once, ensure youre in the repository's root directory and simply call:

```sh
tox
```

## Contributing

If you want to contribute to the project, please read the [contributing guide](CONTRIBUTING.md).
