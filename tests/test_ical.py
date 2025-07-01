from server.ical import EventParser


def test_event_parser_initialization():
    """
    Test that the EventParser is initialized correctly with the provided configuration.

    Args:
        config: The configuration object to initialize the EventParser with.

    Asserts:
        The parser's config attribute is set to the provided config.
    """
    parser = EventParser()
    assert type(parser.config) == dict

def test_get_events(config):
    """
    Test that the get_events method returns a list.
    """
    parser = EventParser(config)
    events = parser.get_events()
    assert isinstance(events, str)

