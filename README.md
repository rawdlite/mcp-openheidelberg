# mcp-openheidelberg

## Project Description

https://nx.openheidelberg.de/s/HJjR7FAtbmLYtLY

## Getting started

- clone repository
- cd mpc-openheidelberg
- uv venv
- uv sync

   cp config_sample.toml ~/.config/mpc/config.toml

fill in requiered values

create claude_desktop_config.json

{
  "mcpServers": {
    "Openheidelberg": {
      "command": "/Users/tom/.local/bin/uv",
      "args": [
        "run",
	"--directory",
        "/Users/tom/projects/python-dev/mcp-openheidelberg",
        "--with",
        "mcp",
        "server/openheidelberg.py"
      ]
    }
  }
}

obviously adapt the path.
