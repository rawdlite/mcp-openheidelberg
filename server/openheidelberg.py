import json
from mcp.server.fastmcp import FastMCP
try:
    from ical import EventParser
except ImportError:
    from server.ical import EventParser

try:
    from workpackages import WorkPackageParser
except ImportError:
    from server.workpackages import WorkPackageParser

mcp = FastMCP("Openheidelberg")

@mcp.tool()
def show_events(category: str = None)  -> str:
    """Get Events for Openheidelberg.

    Args:
        category: category of event
    """
    ep = EventParser()
    return ep.get_events()

@mcp.tool()
def show_members() -> str:
    """
    Get Memnbers of the Openheidelberg project.
    """
    wp = WorkPackageParser()
    return json.dumps(wp.get_members())

@mcp.tool()
def show_tasks() -> str:
    """
    Get open tasks of the Openheidelberg project.
    """
    wp = WorkPackageParser()
    return json.dumps(wp.get_workpackages())

if __name__ == "__main__":
    mcp.run(transport="stdio")