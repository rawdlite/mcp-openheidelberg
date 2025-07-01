from ics import Calendar
from datetime import date, datetime, timedelta
import requests
import json
import arrow
from mcp.server.fastmcp import FastMCP
from typing import Optional

try:
    from config import Config
except ImportError:
    from server.config import Config


class EventParser:
    """
    A class designed to parse and manage events from a calendar.

    This class retrieves events from a specified calendar URL provided in its configuration.
    It processes and converts calendar events into standardized dictionary representations,
    enabling easier manipulation, inspection, or export.

    :ivar config: The configuration details for the parser, containing calendar settings such as the URL.
    :type config: dict
    :ivar cal: The calendar object fetched from the provided URL in the configuration.
    :type cal: Calendar
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        """Initialize the EventParser with a configuration."""
        if config is None:
            config = Config().get('calendar')
        self.config = config
        url = config['url']
        self.cal = Calendar(requests.get(url).text)
        #self.categories = config['categories']

    def event2dict(self,ev) -> dict:
        if ev.organizer:
            organizer = {
                'name': ev.organizer.common_name,
                'email': ev.organizer.email
        }
        else:
            organizer = 'none'
        evdict = {
            'name': ev.name,
            'organizer': organizer,
            'begin': ev.begin.format('DD-MM-YYYY HH:mm:ss ZZ'),
            'end': ev.end.format('DD-MM-YYYY HH:mm:ss ZZ'),
            'location': ev.location,
            'categories': list(ev.categories),
            'description': ev.description,
            'url': ev.url,
            'uid': ev.uid,
            'status': ev.status,
        }
        return evdict

    def get_events(self):
        """Get events from the calendar."""
        events = []
        cutoff = arrow.get(datetime.now())
        for event in self.cal.timeline.start_after(cutoff):
            events.append(self.event2dict(event))
            #print(dir(event))
        return json.dumps(events)
