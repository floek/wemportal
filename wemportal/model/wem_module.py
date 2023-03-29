"""
Manage WEM Modules
"""
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, List

from wemportal.model.wem_parameter import WemParameter


class ModuleType(IntEnum):
    """
    Types of WEM Modules
    """
    system = 1
    heater_circuit = 2
    hot_water_circuit = 3
    solar = 4
    terminal = 5
    gateway = 6
    we = 7
    device = 9
    ground_module = 10
    test = 240
    sensor = 241
    external = 255


@dataclass
class WemModule:
    """
    Class for WEM Modules
    """
    index: int
    custom_numbering: int
    name: str
    type: ModuleType
    dynamisation: bool
    fwu_version: str
    parameters: List[WemParameter]


class WemModuleParser:
    # pylint: disable=too-few-public-methods
    """
    Parser for WEM Modules
    """
    @staticmethod
    def load(module: Dict) -> WemModule:
        """Load WEM Module from Dict"""
        return WemModule(
            index = module["Index"],
            custom_numbering = module["CustomNumbering"],
            name = module["Name"],
            type = ModuleType(module["Type"]),
            dynamisation = module["Dynamisation"],
            fwu_version = module["FWUVersion"],
            parameters = []
        )
