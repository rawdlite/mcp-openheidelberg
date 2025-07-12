import asyncio
import os
from dotenv import load_dotenv
#from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from langchain_ollama import ChatOllama



load_dotenv()  # 🔑 Load API keys

# 1️⃣ Describe which MCP servers you want. .

class LLMClient():

    def __init__(self, config: dict):
        #self.client = MCPClient.from_dict(CONFIG)
        config_file = os.path.join(os.path.dirname(__file__), '../mcp_server_config.json')
        self.client = MCPClient.from_config_file(config_file)
        self.agent = None
        self.config = config

    async def connect_to_server(self):
        """Connect to the MCP server
        """
        llm = ChatOllama(
            model=self.config["model"],
            request_timeout=120.0,
            temperature=0.7,
            # Manually set the context window to limit memory usage
            context_window=8000,
        )
        self.agent = MCPAgent(llm=llm, client=self.client, max_steps=20)
        return f"Connected to server with tools: "

    async def process_query(self, query: str) -> str:
        result = await self.agent.run(query)
        return result

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.client.close_all_sessions()





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
