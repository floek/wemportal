"""
Abstraction for API and WEB classes
"""
from wemportal import WemPortalAPI
from wemportal.wem_portal_web import WemPortalWeb


class WemPortal:
    """
    Class to interact with wemportal via api and web
    """

    def __init__(self, username: str, password: str):
        self.username: str = username
        self.password: str = password
        self.__api: WemPortalAPI = WemPortalAPI(username=username, password=password)
        self.__web: WemPortalWeb = WemPortalWeb(username=username, password=password)

    def login(self):
        """Login to api and web"""
        self.__api.login()
        self.__web.login()

    def fetch_devices(self):
        """Fetch data"""
        devices = self.__api.fetch()
        for device in devices:
            self.__web.get_heating_statistic(device)
            self.__web.get_hot_water_statistic(device)
            self.__web.get_summary_statistic(device)
            self.__web.get_defrost_statistic(device)
            self.__web.get_cooling_statistic(device)

        return devices

    def logout(self):
        """Logout from api and web"""
        self.__api.logout()
        self.__web.logout()
