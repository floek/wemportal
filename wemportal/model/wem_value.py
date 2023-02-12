"""
Manage WEM Values
"""
from dataclasses import dataclass
import datetime
from typing import Dict


@dataclass
class WemValue():
    """Class for WEM Values"""
    unit: str
    time: datetime.datetime
    numeric_value: float
    string_value: str
    dynamisation: bool
    parameter_id: str


class WemValueParser:
    # pylint: disable=too-few-public-methods
    """
    Parser for WEM Values
    """
    @staticmethod
    def load(value: Dict) -> WemValue:
        """Load WEM Value from Dict"""
        return WemValue(
            unit = value["Unit"],
            time = datetime.datetime.fromtimestamp(int(value["Timestamp"])),
            numeric_value = value["NumericValue"],
            string_value = value["StringValue"],
            dynamisation = value["Dynamisation"],
            parameter_id = value["ParameterID"]
        )
