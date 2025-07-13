from client import ChatClient
import asyncio
import pytest

def test_chatclient():
    assert ChatClient

def test_init_chatclient():
    config = {'library': 'mcp_use','provider': 'anthropic','model': 'claude-3-sonnet-20240229'}
    client = ChatClient(config)
    assert client

@pytest.mark.asyncio
async def test_connect_chatclient():
    config = {'library': 'mcp_use','provider': 'anthropic','model': 'claude-3-7-sonnet-20250219'}
    client = ChatClient(config).client
    res = await client.connect_to_server()
    assert type(res) == str

@pytest.mark.asyncio
async def test_run_chatclient():
    config = {'library': 'mcp_use','provider': 'anthropic','model': 'claude-3-7-sonnet-20250219'}
    # claude-3-7-sonnet-20250219 claude-opus-4-20250514 claude-3-5-sonnet-20241022 claude-3-5-haiku-20241022
    # claude-3-haiku-20240307
    client = ChatClient(config).client
    res = await client.connect_to_server()
    print(res)
    res = await client.process_query("Wer ist Mitglied?")
    print(res)
    assert type(res) == str

