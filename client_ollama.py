import asyncio
import os
from dotenv import load_dotenv
#from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from langchain_ollama import ChatOllama



load_dotenv()  # 🔑 Load API keys

# 1️⃣ Describe which MCP servers you want.  Here we spin up Playwright in a headless browser.
CONFIG = {
    "mcpServers": {
        "playwright": {
            "command": "python",
            "args": ["server/openheidelberg.py"],
            "env": None  # required if you run inside Xvfb / CI
        }
    }
}

async def main():
    client = MCPClient.from_dict(CONFIG)
    #llm = ChatOpenAI(model="gpt-4o")

    llm = ChatOllama(
        model="llama3.2:latest",
        request_timeout=120.0,
        # Manually set the context window to limit memory usage
        context_window=8000,
    )

    # 2️⃣ Wire the LLM to the client
    agent = MCPAgent(llm=llm, client=client, max_steps=20)

    # 3️⃣ Ask something that requires real web browsing
    result = await agent.run("Wer ist Mitglied bei Openheidelberg")
    print("\n🔥 Result:", result)

    # 4️⃣ Always clean up running MCP sessions
    await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
