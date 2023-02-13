"""
Interact with wemportal via api
"""
import json
from typing import Dict, List, Optional
import requests
from requests import Session
from wemportal.constants import LOGGER, wem_url
from wemportal.exceptions import WemPortalConnectionError
from wemportal.model.wem_device import WemDevice, WemDeviceParser
from wemportal.model.wem_parameter import WemParameterParser
from wemportal.model.wem_value import WemValueParser


class WemPortalAPI:
    """
    Class to interact with wemportal via api
    """

    def __init__(self, username: str, password: str):
        self.devices: List[WemDevice] = []
        self.headers: Dict = {
            "User-Agent": "WeishauptWEMApp",
            "X-Api-Version": "2.0.0.0",
            "Accept": "*/*",
        }
        self.session: Optional[Session] = None
        self.username: str = username
        self.password: str = password

    def login(self):
        """Login to api"""
        self.session = requests.Session()
        self.session.cookies.clear()
        payload = {
            "Name": self.username,
            "PasswordUTF8": self.password,
            "AppID": "com.weishaupt.wemapp",
            "AppVersion": "2.0.2",
            "ClientOS": "Android",
        }
        self.session.headers.update(self.headers)
        response = self.session.post(
            f"{wem_url}/app/Account/Login",
            data=payload,
        )
        if response.status_code != 200:
            raise WemPortalConnectionError(
                f"Authentication Error: "
                f"Check if your login credentials are correct. "
                f"Receive response code: {response.status_code}, response: {response.content}"
            )

    def fetch(self):
        """Get data from the mobile API"""
        if self.session is None:
            self.login()

        if not self.devices:
            self.get_devices()

        self.get_values()

        return self.devices

    def get_devices(self):
        """Fetching api device data"""
        LOGGER.debug("Fetching api device data")
        response = self.session.get(
            f"{wem_url}/app/device/Read"
        )
        data = response.json()
        self.devices = []
        for device in data["Devices"]:
            device_object = WemDeviceParser.load(device)
            for module in device_object.modules:
                LOGGER.debug("Fetching api parameters data")

                data = {
                    "DeviceID": device_object.id,
                    "ModuleIndex": module.index,
                    "ModuleType": int(module.type)
                }
                response = self.session.post(
                    f"{wem_url}/app/EventType/Read",
                    data=data,
                )
                module.parameters = [WemParameterParser.load(param) for param in response.json()["Parameters"]]

            self.devices.append(device_object)

    def get_values(self):
        """Refresh and retrieve new values"""
        LOGGER.debug("Refreshing and retrieving new values")

        for device in self.devices:
            data = device.get_parameter_query()
            headers = {"Content-Type": "application/json"}

            # Refresh
            self.session.post(
                f"{wem_url}/app/DataAccess/Refresh",
                headers=headers,
                data=json.dumps(data),
            )

            # Read
            values = self.session.post(
                f"{wem_url}/app/DataAccess/Read",
                headers=headers,
                data=json.dumps(data),
            ).json()

            for module in values['Modules']:
                module_object = next((mod for mod in device.modules
                                      if mod.index == module['ModuleIndex'] and int(mod.type) == module['ModuleType']),
                                     None)

                for value in module['Values']:
                    value_object = WemValueParser.load(value)
                    parameter = next((param for param in module_object.parameters
                                      if param.parameter_id == value_object.parameter_id), None)
                    parameter.value = value_object

    def logout(self):
        """Delete session"""
        self.session.close()
