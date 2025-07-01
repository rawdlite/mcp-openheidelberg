from server.config import Config

def test_config():
    """Test creating an instance of Config."""
    assert Config

def test_get_config_key():
    """Test retrieving a configuration key."""
    config = Config()
    assert type(config.get('calendar')) == dict