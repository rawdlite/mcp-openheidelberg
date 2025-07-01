# mcp-ical
Getting and merging ical entries

- clone repository
- cd mpc-openheidelberg
- uv venv
- uv sync


claude_desktop_config.json

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
        "server/ical.py"
      ]
    }
  }
}
