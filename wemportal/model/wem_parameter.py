# pylint: disable=too-few-public-methods
"""
Manage WEM Parameters
"""
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Dict, Optional

from wemportal.model.wem_value import WemValue


class DataType(IntEnum):
    """Data Types for parameters"""
    function = 1
    time = 2
    value = 3
    program = 6
    decimal_value = -1


@dataclass()
class EnumValue:
    """Class for values of parameters"""
    value: int
    name: str


class EnumValueParser:
    """Parser for Enum Values"""
    @staticmethod
    def load(enum_value: Dict) -> EnumValue:
        """Load Enum Values from Dict"""
        return EnumValue(
            value = enum_value["Value"],
            name = enum_value["Name"]
        )


@dataclass
class WemParameter:
    # pylint: disable=too-many-instance-attributes
    """Wem Parameter class"""
    parameter_id: str
    name: str
    data_type: DataType
    min_value: Optional[float]
    max_value: Optional[float]
    default_value: Optional[float]
    is_readable: bool
    is_writeable: bool
    enum_values: List[EnumValue]
    value: Optional[WemValue]


class WemParameterParser:
    """Parser for WEM Parameters"""
    @staticmethod
    def load(parameter: Dict) -> WemParameter:
        """Load Enum Values from Dict"""
        enum_values = parameter["EnumValues"]
        if not enum_values:
            enum_values = []

        return WemParameter(
            parameter_id = parameter["ParameterID"],
            name = parameter["Name"],
            data_type = DataType(parameter["DataType"]),
            min_value = parameter["MinValue"],
            max_value = parameter["MaxValue"],
            default_value = parameter["DefaultValue"],
            is_readable=parameter["IsReadable"],
            is_writeable=parameter["IsWriteable"],
            enum_values=[EnumValueParser.load(enum_value) for enum_value in enum_values],
            value=None
        )
