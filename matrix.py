import niobot
import asyncio
import aiocouchdb
from typing import List, Dict, Any
from client import ChatClient
from server.config import Config


import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/matrix.log'),  # Log to file
        logging.StreamHandler()  # Optionally log to console
    ]
)


config = Config().get('matrix')
if isinstance(config, str):
    config = json.loads(config)
cbd_config = Config().get('couchdb')
if isinstance(cbd_config, str):
    cbd_config = json.loads(cbd_config)

client = niobot.NioBot(
    # Note that all of these options other than the following are optional:
    # * homeserver
    # * user_id
    # * command_prefix
    homeserver=config.get("homeserver") or "https://matrix.org",  # it is important that you use the matrix server, not the delegation URL
    user_id=config.get("user_id") or "@oh-bot:matrix.org",
    device_id=config.get("device_id") or "oh-bot",
    command_prefix=config.get("command_prefix") or "!",
    case_insensitive=config.get("case_insensitive") or True,
    owner_id=config.get("owner_id") or "@oh-bot:matrix.org",
    ignore_self=True  # default is True, set to false to not ignore the bot's own messages
)

async def write_to_couchdb(data: List[Dict[str, Any]]):
    """Write data to CouchDB."""
    server = aiocouchdb.Server(
        cbd_config.get('couchdb_url'), 
        username=cbd_config.get('couchdb_username'), 
        password=cbd_config.get('couchdb_password')
    )
    if not await server.exists():
        logging.error("CouchDB server does not exist or is unreachable.")
        return None
    database_name = cbd_config.get('couchdb_db')
    try:
        db = await server[database_name]
    except aiocouchdb.exceptions.ResourceNotFound:
        # Database doesn't exist, create it
        db = await server.create(database_name)
        logging.info(f"Created database {database_name}")
    except Exception as e:
        logging.error(f"Error accessing database {database_name}: {e}")
        return None
    # Write data to database
    for i, doc in enumerate(data):
        # Add _id if not present
        if '_id' not in doc:
            doc['_id'] = f"user_{i}"
        # Insert document
        try:
            await db.save(doc)
        except Exception as e:
            print(f"Error inserting document {i}: {str(e)}")
            logging.error(f"Error inserting document {i}: {str(e)}") 
    logging.info(f"Data written to CouchDB: {data}")
    return data

@client.on_event("ready")
async def on_ready(sync_result: niobot.SyncResponse):
    """Event handler for when the bot is ready."""
    logging.info(f"Bot is ready!")


# A simple command
@client.command()
async def ping(ctx: niobot.Context):
    latency = ctx.latency
    await ctx.respond(f"Pong! {latency:.2f}ms")
    logging.info(f"Received ping command from {ctx.sender}")


# A command with arguments
@client.command()
async def onboard(ctx: niobot.Context, *, message: str):
    sender = ctx.sender
    input = message.split('')
    if len(input) < 3:
        await ctx.respond("Please provide your first name, last name, and email in the format: firstname:<firstname> lastname:<lastname> email:<email>")
        return
    onboarding_user = {}
    for item in input:
        if not item.startswith(('firstname:', 'lastname:', 'email:')):
            await ctx.respond(f"Invalid input format: {item}. Please use the format: firstname:<firstname> lastname:<lastname> email:<email>")
            return
        key, value = item.split(':', 1)
        onboarding_user[key] = value
    await ctx.respond(f"Onboarding user: {onboarding_user}")
    result = await write_to_couchdb([onboarding_user])
    if result:
        await ctx.respond(f"User onboarded successfully: {onboarding_user}")
    else:
        await ctx.respond("Failed to onboard user due to CouchDB error.")
    
async def execute_chat_command(ctx, query_message, response_prefix):
    """Helper function to execute chat commands with consistent flow"""
    client_config = Config().get('client')
    if isinstance(client_config, str):
        import json
        client_config = json.loads(client_config)
    chat_client = ChatClient(client_config).client
    response = await chat_client.connect_to_server()
    #await ctx.respond(response)
    response = await chat_client.process_query(query_message)
    await ctx.respond(f"{response_prefix}: {response}")
    await chat_client.cleanup()

@client.command()
async def chat(ctx: niobot.Context, *, message: str):
    await execute_chat_command(ctx, message, "My Answer")


@client.command()
async def events(ctx: niobot.Context):
    await execute_chat_command(
        ctx, 
        "Zeige mir die nächsten Termine bei Openheidelberg", 
        "Answer"
        )

@client.command()
async def tasks(ctx: niobot.Context):
    await execute_chat_command(
        ctx,
        "Welche Aufgaben gibt es bei Openheidelberg?", 
        "Answer"
        )


@client.command()
async def members(ctx: niobot.Context, *, message: str):
    await execute_chat_command(
        ctx, 
        "Wer ist Mitglied bei Openheidelberg", 
        "My Answer"
        )


client.run(access_token=config.get('token'))
