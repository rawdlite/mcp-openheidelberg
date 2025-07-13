from importlib import import_module
from server.config import Config
import asyncio
import argparse 


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
    parser = argparse.ArgumentParser(description="Openheidelberg Chat Client")
    parser.add_argument("--model", type=str, help="Model to use")
    parser.add_argument("--library", type=str, help="Library backend to use")
    parser.add_argument("--provider", type=str, help="Provider to use")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()
    
    if args.model:
        config['model'] = args.model
    if args.library:
        config['library'] = args.library
    if args.provider:
        config['provider'] = args.provider
    if args.verbose:
        print(f"library: {config['library']}\n"
              f"model: {config['model']}\n"
              f"provider: {config['provider']}")
    try:
        await client.connect_to_server()
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys

    asyncio.run(main())
