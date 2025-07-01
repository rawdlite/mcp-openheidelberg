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

# Create an MCP server
mcp = FastMCP("Openheidelberg")

class EventParser:
    """
       Class to get Events
       filter by category
        ... 
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

@mcp.resource("openheidelberg://{category}")
def provide_events(category: str) -> str:
    #todo: filter by categories
    "get events for openheidelberg"
    return get_events()

@mcp.tool()
def show_events(category: str) -> str:
    """Get Events for Openheidelberg.

    Args:
        category: category of event
    """
    return get_events()

@mcp.prompt()
def heidelberg_events_prompt() -> str:
    """Prompt for querying Heidelberg events in a user-friendly way"""
    return """Du hilfst Nutzern dabei, Termine und Veranstaltungen von Openheidelberg zu finden.

Wenn ein Nutzer nach Terminen fragt, verwende das show_events Tool um aktuelle Veranstaltungen abzurufen.

Formatiere die Antworten benutzerfreundlich auf Deutsch:
- Zeige Datum und Uhrzeit in lesbarem Format (z.B. "Dienstag, 1. Juli 2025, 17:00-18:00 Uhr")
- Hebe wichtige Informationen wie Ort, Organisator und Beschreibung hervor
- Verwende Markdown-Formatierung für bessere Lesbarkeit
- Wenn keine Termine gefunden werden, erkläre das freundlich

Häufige Anfragen:
- "Welche Termine gibt es?"
- "Was ist diese Woche los?"
- "Gibt es Veranstaltungen zu [Thema]?"
- "Wann ist der nächste Termin?"

Du kannst auch nach Kategorien filtern, auch wenn die Implementierung noch in Entwicklung ist."""




if __name__ == "__main__":
    mcp.run(transport="stdio")
