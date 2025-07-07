from importlib import import_module
import asyncio


class ChatClient:
    def __init__(self, config: dict):
        _cm = import_module(f"clients.client_{config['client']}")
        self.client = _cm.LLMClient()

    def connect(self):
        self.client.connect()

    def disconnect(self):
        print(f"Disconnecting {self.name}...")

async def main():
    client = ChatClient({'client': 'ollama'}).client
    try:
        await client.connect_to_server()
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys

    asyncio.run(main())
