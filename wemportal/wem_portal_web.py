"""
Interact with wemportal via webgui
"""
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from requests import Session
from wemportal.constants import wem_url, LOGGER
from wemportal.exceptions import WemPortalConnectionError
from wemportal.model.wem_device import WemDevice
from wemportal.model.wem_statistic import GraphType, StatisticType, \
    WemHeatingStatisticParser, WemHotWaterStatisticParser, WemSummaryStatisticParser, \
    WemDefrostStatisticParser, WemCoolingStatisticParser

class WemPortalWeb:
    """
    Class to interact with wemportal via webgui
    """

    def __init__(self, username: str, password: str):
        self.session: Session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0"'})
        self.session.cookies.clear()
        self.username: str = username
        self.password: str = password

    def login(self):
        """
        Login to wemportal webgui
        """

        LOGGER.debug("Login to wemportal")
        # Request login page to scrape hidden inputs
        response = self.session.get(f'{wem_url}/Web/Login.aspx')
        data = _get_hidden_input(response.content)

        # Fill form
        data['ctl00$content$tbxUserName'] = self.username
        data['ctl00$content$tbxPassword'] = self.password
        data['ctl00$content$btnLogin'] = 'Anmelden'

        # login
        web_response = self.session.post(f'{wem_url}/Web/Login.aspx', data=data)
        if web_response.status_code != 200:
            raise WemPortalConnectionError(
                f"Authentication Error: "
                f"Check if your login credentials are correct. "
                f"Receive response code: {web_response.status_code}, response: {web_response.content}"
            )

    def __get_raw_statistic(self, device: WemDevice,
                            statistics_type: StatisticType,
                            graph_type: GraphType = GraphType.daily):
        """
        Retrieve data from wemportal webgui
        """

        # Get device structure
        response = self.session.get(f"{wem_url}/Web/Api/DeviceStatistics/GetStructure?deviceId={device.id}")
        device_structure = response.json()
        modules = []
        for group in device_structure:
            for module in group["Modules"]:
                modules.append(module)
        system_table_ids = [module["SystemTableID"] for module in modules]
        data = {
            'SystemTableIDs[]': system_table_ids,
            'StatisticsType': int(statistics_type),
            'GraphType': int(graph_type),
            'MaxDisplayTime': datetime.now(),
            'MonthType': '0',
        }

        response = self.session.post(
            f'{wem_url}/Web/Api/DeviceStatistics/GetStatistics',
            data=data,
        )
        return response.json()

    def get_heating_statistic(self, device: WemDevice):
        """Retrieve statistics for heating system"""
        graph_type = GraphType.daily
        data = self.__get_raw_statistic(device=device, statistics_type=StatisticType.heating, graph_type = graph_type)
        heating_statistic = WemHeatingStatisticParser.load(statistic=data, graph_type=graph_type)
        device.heating_statistic = heating_statistic
        return device

    def get_hot_water_statistic(self, device: WemDevice):
        """Retrieve statistics for hot water system"""
        graph_type = GraphType.daily
        data = self.__get_raw_statistic(device=device, statistics_type=StatisticType.hot_water, graph_type = graph_type)
        hot_water_statistic = WemHotWaterStatisticParser.load(statistic=data, graph_type=graph_type)
        device.hot_water_statistic = hot_water_statistic
        return device

    def get_summary_statistic(self, device: WemDevice):
        """Retrieve statistics for hot water system"""
        graph_type = GraphType.daily
        data = self.__get_raw_statistic(device=device, statistics_type=StatisticType.summary, graph_type = graph_type)
        summary_statistic = WemSummaryStatisticParser.load(statistic=data, graph_type=graph_type)
        device.summary_statistic = summary_statistic
        return device

    def get_defrost_statistic(self, device: WemDevice):
        """Retrieve statistics for hot water system"""
        graph_type = GraphType.daily
        data = self.__get_raw_statistic(device=device, statistics_type=StatisticType.defrost, graph_type = graph_type)
        defrost_statistic = WemDefrostStatisticParser.load(statistic=data, graph_type=graph_type)
        device.defrost_statistic = defrost_statistic
        return device


    def get_cooling_statistic(self, device: WemDevice):
        """Retrieve statistics for hot water system"""
        graph_type = GraphType.daily
        data = self.__get_raw_statistic(device=device, statistics_type=StatisticType.cooling, graph_type = graph_type)
        cooling_statistic = WemCoolingStatisticParser.load(statistic=data, graph_type=graph_type)
        device.cooling_statistic = cooling_statistic
        return device

    def logout(self):
        """
        Logout from wemportal webgui
        """
        self.session.close()


def _get_hidden_input(content):
    """
    Return a dict containing hidden input from content
    """
    tags = {}
    soup = BeautifulSoup(content, 'html.parser')
    hidden_tags = soup.find_all('input', type='hidden')
    for tag in hidden_tags:
        tags[tag.get('name')] = tag.get('value')

    return tags
