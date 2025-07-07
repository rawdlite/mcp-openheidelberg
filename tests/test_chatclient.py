from client import ChatClient

def test_chatclient():
    assert ChatClient

def test_init_chatclient():
    config = {'client': 'anthropic'}
    client = ChatClient(config)
    assert client