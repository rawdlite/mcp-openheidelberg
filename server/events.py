import icalendar
import recurring_ical_events
import json
from datetime import date, datetime, timedelta
import caldav
from config import Config
from typing import Optional


class EventParser:
    """
    A class designed to parse and manage events from a calendar.

    This class retrieves events from a specified calendar URL provided in its co
nfiguration.
    It processes and converts calendar events into standardized dictionary repre
sentations,
    enabling easier manipulation, inspection, or export.

    :ivar config: The configuration details for the parser, containing calendar 
settings such as the URL.
    :type config: dict
    :ivar cal: The calendar object fetched from the provided URL in the configur
ation.
    :type cal: Calendar
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        """Initialize the EventParser with a configuration."""
        if config is None:
            config = Config().get('calendar')
        self.config = config
        url = config['url']
        self.client = caldav.DAVClient(url)

    def event2dict(self, event) -> dict:
        evdict = {
            'name': event['SUMMARY'],
            'start': event["DTSTART"].dt.strftime("%Y-%m-%d %H:%M:%S"),
            'end': event['DTEND'].dt.strftime("%Y-%m-%d %H:%M:%S"),
            'description': event['DESCRIPTION'],
            'location': event['LOCATION'],
            'organizer': event.get('ORGANIZER','')
        }
        if event.get('categories'):
            evdict['categories'] = event.get('categories').to_ical().decode()
        return evdict


    def get_events(self):
        """
            get events from caldav
            todo: make timerange a parameter
        """
        event_arr = []
        principal = self.client.principal()
        for calendar in principal.calendars():
            for event in calendar.events():
                ical_text = event.data
                a_calendar = icalendar.Calendar.from_ical(ical_text)
                events = recurring_ical_events.of(a_calendar).between(
                             datetime.now(),
                             datetime.now() + timedelta(weeks=3)
                         )
                for event in events:
                    event_arr.append(self.event2dict(event))
        return json.dumps(event_arr)            
