from importlib import import_module
from server.config import Config
import asyncio


class ChatClient:
    def __init__(self, config: dict):
        _cm = import_module(f"clients.client_{config['library']}")
        self.client = _cm.LLMClient(config)

    def connect(self):
        self.client.connect()

    def disconnect(self):
        print(f"Disconnecting {self.name}...")

async def main():
    config = Config().get('client')
    client = ChatClient(config).client
    try:
        await client.connect_to_server()
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys

    asyncio.run(main())
