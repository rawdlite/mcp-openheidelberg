import requests
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from dateutil import parser

try:
    from config import Config
except ImportError:
    from server.config import Config

class WorkpackageParser:
    """
    This class is used to parse the workpackage data from the API.
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        """
        Initialize the WorkpackageParser class.

        :param config:
        """
        if config is None:
            config = Config().get('workpackages')
        self.config = config
        self.apikey = config['apikey']

    def get_workpackages(self) -> List[Dict[str, Any]]:
        """
        Get the workpackages from the API.
        :return:
        """
        url = f"https://apikey:{self.apikey}@plan.openheidelberg.de/api/v3/work_packages"
        workpackages = requests.get(url)

        total = workpackages.json()['total']
        count = workpackages.json()['count']
        return workpackages.json()
