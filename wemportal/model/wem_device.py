"""
Main data structures for WEM Devices
"""
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Dict, Optional

from wemportal.model.wem_module import WemModule, WemModuleParser
from wemportal.model.wem_statistic import WemHeatingStatistic, WemHotWaterStatistic, WemSummaryStatistic, WemDefrostStatistic, WemCoolingStatistic

class DeviceType(IntEnum):
    """
    Types of devices
    """
    combi_boiler = 1 # NOTE: just guessing
    heating_pump = 2


class ConnectionStatus(IntEnum):
    """
    Type for Connection status
    """
    online = 0
    offline = 50
    busy = 8
    wrong_secret = 7


@dataclass
class WemDevice():
    # pylint: disable=too-many-instance-attributes
    """
    Main class for WEM Devices
    """
    id: int
    name: str
    device_type: DeviceType
    modules: List[WemModule]
    connection_status: ConnectionStatus
    has_errors: bool
    heating_statistic: Optional[WemHeatingStatistic]
    hot_water_statistic: Optional[WemHotWaterStatistic]
    summary_statistic: Optional[WemSummaryStatistic]
    defrost_statistic: Optional[WemDefrostStatistic]
    cooling_statistic: Optional[WemCoolingStatistic]

    def get_parameter_query(self):
        """Build query for parameters"""
        data = {
            "DeviceID": self.id,
            "Modules": []
        }

        for module in self.modules:
            if module.parameters:
                data["Modules"].append({
                    "ModuleIndex": module.index,
                    "ModuleType": int(module.type),
                    "Parameters": [
                        {"ParameterID": parameter.parameter_id}
                        for parameter in module.parameters
                    ],
                })

        return data

    def get_parameter_values(self):
        """Get flat list of parameters and values"""
        result = []
        for module in self.modules:
            for parameter in module.parameters:
                value_dict = {
                    "DeviceId": self.id,
                    "DeviceName": self.name,
                    "DeviceType": int(self.device_type),
                    "ModuleIndex": module.index,
                    "ModuleName": module.name,
                    "ModuleType": int(module.type),
                    "ParameterName": parameter.name,
                    "ParameterId": parameter.parameter_id,
                    "ParameterDataType": int(parameter.data_type),
                    "ParameterMaxValue": parameter.max_value,
                    "ParameterMinValue": parameter.min_value
                }

                if parameter.value:
                    value_dict["ValueStringValue"]=parameter.value.string_value
                    value_dict["ValueNumericValue"]=parameter.value.numeric_value
                    value_dict["ValueTime"]=parameter.value.time
                    value_dict["ValueUnit"]=parameter.value.unit
                    result.append(value_dict)

        return result


class WemDeviceParser:
    # pylint: disable=too-few-public-methods
    """Parser for WEM Devices"""
    @staticmethod
    def load(device: Dict) -> WemDevice:
        """Load WEM Device from dict"""
        return WemDevice(
            id = device["ID"],
            name = device["Name"],
            device_type = DeviceType(device["DeviceType"]),
            modules = [ WemModuleParser.load(module) for module in device["Modules"]],
            connection_status = ConnectionStatus(device["ConnectionStatus"]),
            has_errors = device["HasErrors"],
            heating_statistic=None,
            hot_water_statistic=None,
            summary_statistic=None,
            defrost_statistic=None,
            cooling_statistic=None
        )
