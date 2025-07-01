import requests
from typing import Optional, List, Dict, Any



try:
    from config import Config
except ImportError:
    from server.config import Config

class WorkPackageParser:
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
        self.url = config['url']

    def get_members(self) -> List[Dict[str, Any]]:
        """
        Get the workpackages from the API.
        :return:
        """
        url = f"{self.url}/api/v3/projects/18/work_packages"
        response = requests.get(url, auth=('apikey', self.apikey))
        if response.status_code == 200:
            return self.build_result_dict(response)
        else:
            return None

    def build_result_dict(self, workpackages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Build the result dictionary.
        :param workpackages:
        :return:
        """
        result = {'total': workpackages.json()['total'],
                  'count': workpackages.json()['count'],
                  'workpackages': []}
        for workpackage in workpackages.json()['_embedded']['elements']:
            result['workpackages'].append(self.workpackage2dict(workpackage))
        return result

    def get_workpackages(self) -> Dict[str, Any]:
        """
        Get open workpackages from the API.
        :return:
        """
        url = f"{self.url}/api/v3/projects/3/work_packages/"
        params = {
            "filters": '[{"status":{"operator": "o","values": []}}]'
        }
        response = requests.get(url, params=params, auth=('apikey', self.apikey))
        if response.status_code == 200:
            return self.build_result_dict(response)
        else:
            return None

    def workpackage2dict(self, workpackage: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts a given work package dictionary into a processed dictionary format. This method takes
        a work package represented as a dictionary containing relevant details and returns a transformed
        dictionary suited to specific requirements.

        :param workpackage: A dictionary containing key-value pairs representing a work package.
        :type workpackage: Dict[str, Any]
        :return: A processed dictionary derived from the input work package.
        :rtype: Dict[str, Any]
        """
        wpdict = {
            'id': workpackage['id'],
            'subject': workpackage['subject'],
            'description': workpackage['description']['raw'],
            'status': workpackage['_links']['status']['title'],
            'priority': workpackage['_links']['priority']['title'],
        }
        return wpdict


