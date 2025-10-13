# (C) 2025 GoodData Corporation

import re
from pathlib import Path

UG_REGEX = r"^(?!\.)[.A-Za-z0-9_-]{1,255}$"


def path_must_exist(value: Path) -> None:
    """Validate that a provided filesystem path exists."""
    if not value.exists():
        raise ValueError(f"Invalid path to input csv given: {value}")


def delimiters_must_be_different(delimiter: str, inner_delimiter: str) -> None:
    """Validate that a provided delimiter is different from the inner delimiter."""
    if delimiter == inner_delimiter:
        raise ValueError("Delimiter and Inner Delimiter cannot be the same.")


def inner_delimiter_must_be_valid(inner_delimiter: str) -> None:
    """Validate that a provided inner delimiter is valid."""
    if inner_delimiter == "." or re.match(UG_REGEX, inner_delimiter):
        raise RuntimeError(
            'Inner delimiter cannot be dot (".") '
            f'or match the following regex: "{UG_REGEX}".'
        )


def quotechar_must_be_valid(quotechar: str) -> None:
    """Validate that a provided quotechar is valid."""
    if len(quotechar) != 1:
        raise RuntimeError("The quotechar argument must be exactly one character long.")
