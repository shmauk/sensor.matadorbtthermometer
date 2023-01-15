"""Platform for bluetooth thermometer integration"""
from __future__ import annotations

import logging
import voluptuous as vol

from .matador import MatadorInstance

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity

from homeassistant.const import (
    ATTR_BATTERY_LEVEL,
    CONF_DEVICES,
    CONF_NAME,
    CONF_TEMPERATURE_UNIT,
    CONF_UNIQUE_ID,
    CONF_MAC,
    DEVICE_CLASS_TEMPERATURE,
    UnitOfTemperature
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from pprint import pformat

_LOGGER = logging.getLogger("matador")

#Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_MAC): cv.string,
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:

    """Set up the Matador Bluetooth Thermometer Platform"""
    # Add Devices
    _LOGGER.info(pformat(config))

    sensor = {
        "name": config[CONF_NAME],
        "mac": config[CONF_MAC]
    }

    add_entities([MatadorSensor(sensor)])

class MatadorSensor(SensorEntity):

    def __init__(self, sensor) -> None:
        """Initialise a Matador Bluetooth Thermometer"""
        _LOGGER.info(pformat(sensor))
        self._sensor = MatadorInstance(sensor['mac'])
        self._name = sensor['name']
        self._type = 'temperature'
        self._state = None
        self._unit = UnitOfTemperature.CELSIUS
        self._device_class = DEVICE_CLASS_TEMPERATURE

    @property
    def name(self) -> str:
        """Return the name of this sensor"""
        return self._name

    @property
    def state(self) -> bool | None:
        """Return whether the device is available or not."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity"""
        return self._unit

    @property
    def device_class(self):
        """Return the Home Assistant device class."""
        return self._device_class

    async def update(self) -> None:
        """Fetch new data for the thermometer"""
        data = await self._sensor.get_data(self._mac)
        self._temperature = data.get('temperature')
        self._battery = data.get('battery')

