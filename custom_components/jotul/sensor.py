"""Platform for sensor integration."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry

from homeassistant.const import TEMP_CELSIUS
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant

from . import Jotul
from .const import DOMAIN, STATUS_CODES


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_devices):
    """Add sensors for passed entry in HA."""
    jotul: Jotul = hass.data[DOMAIN][entry.entry_id]

    async_add_devices([
        JotulTemperatureSensor(jotul),
        JotulTargetTemperatureSensor(jotul),
        JotulPowerSensor(jotul),
        JotulStatusSensor(jotul)
    ])


class JotulTemperatureSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, jotul: Jotul):
        """Initialize the sensor."""
        self._state = None
        self._attr_name = f"{jotul.name}_temperature"
        self.jotul = jotul

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f'{self.jotul.name} Temperature'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return "mdi:thermometer"

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.jotul.get_temperature()


class JotulTargetTemperatureSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, jotul: Jotul):
        """Initialize the sensor."""
        self._state = None
        self._attr_name = f"{jotul.name}_target_temperature"
        self.jotul = jotul

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f'{self.jotul.name} Target Temperature'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return "mdi:thermometer"

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.jotul.get_target_temperature()


class JotulPowerSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, jotul: Jotul):
        """Initialize the sensor."""
        self._state = None
        self._attr_name = f"{jotul.name}_power"
        self.jotul = jotul

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f'{self.jotul.name} Power'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return "mdi:fire"

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.jotul.get_power()


class JotulStatusSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, jotul: Jotul):
        """Initialize the sensor."""
        self._state = None
        self._attr_name = f"{jotul.name}_status"
        self.jotul = jotul

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f'{self.jotul.name} Status'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return "mdi:power"

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = STATUS_CODES.get(self.jotul.get_status(), 'OFF')
