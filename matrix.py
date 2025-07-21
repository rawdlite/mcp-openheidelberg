import niobot
import asyncio
from client import ChatClient
from server.config import Config


config = Config().get('matrix')

client = niobot.NioBot(
    # Note that all of these options other than the following are optional:
    # * homeserver
    # * user_id
    # * command_prefix
    homeserver=config["homeserver"],  # it is important that you use the matrix server, not the delegation URL
    user_id=config["user_id"],
    device_id=config.get("device_id"),
    command_prefix=config["command_prefix"],
    case_insensitive=config.get("case_insensitive"),
    owner_id=config.get("owner_id"),
    ignore_self=True  # default is True, set to false to not ignore the bot's own messages
)

@client.on_event("ready")
async def on_ready(sync_result: niobot.SyncResponse):
    print("Logged in!")


# A simple command
@client.command()
async def ping(ctx: niobot.Context):
    latency = ctx.latency
    await ctx.respond(f"Pong! {latency:.2f}ms")


# A command with arguments
@client.command()
async def echo(ctx: niobot.Context, *, message: str):
    await ctx.respond("You said: " + message)

@client.command()
async def chat(ctx: niobot.Context, *, message: str):
    client_config = Config().get('client')
    client = ChatClient(client_config).client
    response = await client.connect_to_server()
    await ctx.respond(response)
    response = await client.process_query(message)
    await ctx.respond(f"My Answer: {response}")
    await client.cleanup()

@client.command()
async def events(ctx: niobot.Context):
    client_config = Config().get('client')
    client = ChatClient(client_config).client
    response = await client.connect_to_server()
    #await ctx.respond(response)
    response = await client.process_query("Zeige mir die nächsten Termine bei Openheidelberg")
    await ctx.respond(f"Answer: {response}")
    await client.cleanup()

@client.command()
async def tasks(ctx: niobot.Context):
    client_config = Config().get('client')
    client = ChatClient(client_config).client
    response = await client.connect_to_server()
    #await ctx.respond(response)
    response = await client.process_query("Welche Aufgaben gibt es bei Openheidelberg?")
    await ctx.respond(f"Answer: {response}")
    await client.cleanup()

@client.command()
async def members(ctx: niobot.Context, *, message: str):
    client_config = Config().get('client')
    client = ChatClient(client_config).client
    response = await client.connect_to_server()
    #await ctx.respond(response)
    response = await client.process_query("Wer ist Mitglied bei Openheidelberg")
    await ctx.respond(f"My Answer: {response}")
    await client.cleanup()



client.run(access_token=config['token'])
