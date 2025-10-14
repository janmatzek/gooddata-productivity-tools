# Common Arguments Reference

This document provides detailed explanations for command-line arguments that are shared across multiple tools in this repository.

## CSV File Arguments

### `-d, --delimiter`

**Type:** String  
**Default:** `,` (comma)

Column delimiter for the CSV files. Use this to define how the CSV is parsed.

**Example:**

```sh
python scripts/user_mgmt.py input.csv -d ";"
```

This would parse a CSV file that uses semicolons as delimiters instead of commas.

---

### `-i, --inner-delimiter`

**Type:** String  
**Default:** `|` (pipe)  
**Available in:** User management, User group management, Workspace management

Delimiter used to separate multiple values within a single CSV column. This is used for columns that contain lists of items (e.g., multiple user groups, multiple parent groups, or multiple workspace data filter values).

**Important:** The `--inner-delimiter` must differ from the `--delimiter`.

**Example:**

If your CSV contains a column with multiple user groups like `admin|developer|tester`, you would use:

```sh
python scripts/user_mgmt.py input.csv -i "|"
```

---

### `-q, --quotechar`

**Type:** String  
**Default:** `"` (double quote)

Quotation character used to escape special characters (such as the delimiter) within the column field values. This is particularly useful when your data contains the delimiter character itself.

**Escaping the quotechar:** If you need to include the quotechar itself within a field value, you must embed it in quotechars and then double the quotation character.

**Example:**

- Input with escaped quote: `"some""string"`
- Result after parsing: `some"string`

**Usage:**

```sh
python scripts/user_mgmt.py input.csv -q "'"
```

This would use single quotes as the quotation character instead of double quotes.

---

## GoodData Profile Arguments

### `-p, --profile-config`

**Type:** Path  
**Default:** `~/.gooddata/profiles.yaml`

Path to the GoodData profile configuration file. The profile file contains authentication credentials for one or more GoodData instances.

If not specified, the tool will look for the profiles file in the default location.

**Example:**

```sh
python scripts/user_mgmt.py input.csv -p /path/to/custom/profiles.yaml
```

For profile file format and detailed authentication setup, see the [Authentication Setup Guide](../guides/SETUPAUTHENTICATION.md).

---

### `--profile`

**Type:** String  
**Default:** `default`

Name of the GoodData profile to use from the profiles configuration file. This allows you to switch between different GoodData instances or credentials.

**Example:**

```sh
python scripts/user_mgmt.py input.csv --profile customer
```

This would use the `customer` profile defined in your profiles.yaml file instead of the default profile.

**Combined Example:**

```sh
python scripts/user_mgmt.py input.csv -p /path/to/profiles.yaml --profile production
```

This command uses a custom profiles file and selects the `production` profile from it.

---

## Notes

- **Authentication Priority:** If both environment variables (`GDC_AUTH_TOKEN`, `GDC_HOSTNAME`) and profile configuration are provided, the environment variables take precedence.
- **Help Command:** All tools support the `-h` or `--help` flag to display available arguments and their descriptions.
