import os


def load_env_variable(name: str) -> str:
    value: str | None = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable {name} not found")
    return value
