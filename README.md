# Python wemportal module
[![Tests](https://github.com/floek/wemportal/actions/workflows/test.yml/badge.svg)](https://github.com/floek/wemportal/actions/workflows/test.yml)
[![PyPi](https://github.com/floek/wemportal/actions/workflows/publish-release.yml/badge.svg)](https://github.com/floek/wemportal/actions/workflows/publish-release.yml)

I wanted to scrape the Weishaupt WEM Portal without using [Home Assistant](https://home-assistant.io/).
@erikkastelec created a nice project [hass-WEM-Portal](https://github.com/erikkastelec/hass-WEM-Portal), so
I used his code to create this python module for standalone scraping of WEM Portal.

It utilizes the mobile api for the most of the data. The statistics are collected via web api.

## Installation
```
pip install wemportal
```

## Example usage
```python
from wemportal.wem_portal import WemPortal

# Create API object
api = WemPortal(
    username="<WEM Portal Username>",
    password="<WEM Portal Password>"
)

# Fetch data
api.login()
devices = api.fetch_devices()
api.logout()

# Print values
for device in devices:
    print(f"== Device {device.name} ==\n")

    print("Values:")
    for data in device.get_parameter_values():
        print(f"\t{data['ParameterId']}: {data['ValueNumericValue']} {data['ValueUnit']}")

    print("\nHot Water Statistics:")
    for data in device.hot_water_statistic.values:
        print(f"\t{data.datetime.date()}: {data.value:.2f} {device.hot_water_statistic.unit}")

    print("\nHeating Statistics:")
    for data in device.heating_statistic.values:
        print(f"\t{data.datetime.date()}: {data.value:.2f} {device.heating_statistic.unit}")
```

## Reporting bugs or incorrect results

If you find a bug, please create an issue in the
[repo issues tracker](https://github.com/floek/wemportal/issues/).

## Please contribute
It was created for myself, but if you find it useful: Please contribute.
