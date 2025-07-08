# mcp-openheidelberg

## Project Description

https://nx.openheidelberg.de/s/HJjR7FAtbmLYtLY

##Getting started

- clone repository
- cd mpc-openheidelberg
- uv venv
- uv sync


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

## Working on the Api

    uv run cli.py tasks

## Working on the client

    uv run client.py

## Working on the Web App

    uv run flet run

## Working on the Chat

    uv run matrix.py
