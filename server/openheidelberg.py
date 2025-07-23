import json
import logging
import os
import sys
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from mcp.server.elicitation import (
    AcceptedElicitation,
    CancelledElicitation,
    DeclinedElicitation,
)
from pydantic import BaseModel, Field
try:
    from events import EventParser
except ImportError:
    from server.events import EventParser

try:
    from workpackages import WorkPackageParser
except ImportError:
    from server.workpackages import WorkPackageParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("openheidelberg")

mcp = FastMCP("Openheidelberg", log_level="INFO")

@mcp.tool()
async def onboard_user(
                username: str,
                full_name: str,
                email: str,
                service_name: str = "Openheidelberg"
                ) -> str:
    """
    Collect necessary data to onboard a new user for the specified service.

    Args:
        service_name: The name of the service to create an account for
        username: The account username
        full_name: firstname lasstname of user
        email: a valid email address

    Returns:
        Status message about the account creation
    """
    # This tool triggers the elicitation form
    logger.info(f"Creating account for service: {service_name}")

    class AccountSignup(BaseModel):
        username: str = Field(description="Choose a username", min_length=3, max_length=20)
        email: str = Field(description="Your email address", json_schema_extra={"format": "email"})
        full_name: str = Field(description="Your full name", max_length=30)

    result = await mcp.get_context().elicit(
        f"Write Your {service_name} Account data", schema=AccountSignup
    )

    match result:
        case AcceptedElicitation(data=data):
            try:
                # Create accounts directory if it doesn't exist
                os.makedirs("accounts", exist_ok=True)
                    
                # Prepare account data
                account_data = {
                    "username": data.username,
                    "email": data.email,
                    "full_name": data.full_name,
                    "created_at": datetime.now().isoformat(),
                    "service_name": service_name
                }
                    
                # Write to file
                filename = f"accounts/{data.username}_{service_name}.json"
                with open(filename, 'w') as f:
                    json.dump(account_data, f, indent=2)
                    
                logger.info(f"Account data written to file: {filename}")
                return f"✅ Account created successfully for {service_name}!\nUsername: {data.username}\nEmail: {data.email}\nAccount data saved to: {filename}"
                    
            except Exception as e:
                logger.error(f"Failed to write account data to file: {e}")
                return f"✅ Account created successfully for {service_name}!\nUsername: {data.username}\nEmail: {data.email}\n⚠️ Warning: Could not save account data to file: {e}"
        case DeclinedElicitation():
            return f"❌ Account creation for {service_name} was declined by user"
        case CancelledElicitation():
            return f"❌ Account creation for {service_name} was cancelled by user"

@mcp.tool()
def show_events(category: str = None)  -> str:
    """Get Events for Openheidelberg.

    Args:
        category: category of event
    """
    ep = EventParser()
    return ep.get_events()

#@mcp.prompt(name="events", title="Events", description="Show upcomming Events")
#def show_events_prompt() -> str:
#    return "Please Show me the upcomming events for Openheidelberg."

#@mcp.prompt(title="tasks")
#def show_tasks_prompt(skill: str) -> str:
#    return f"Please show me tasks that have been categorized as requiring this skill:\n\n{skill}"

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
