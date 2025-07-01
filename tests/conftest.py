import pytest
import os
import tomllib


@pytest.fixture
def config():
    config_path = os.path.expanduser("~/.config/mcp/config.toml")
    with open(config_path, "rb") as f:
        return tomllib.load(f)

