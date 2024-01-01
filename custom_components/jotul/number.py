"""Platform for switch integration."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry

from homeassistant.components.number import NumberEntity
from homeassistant.core import HomeAssistant
from homeassistant.const import TEMP_CELSIUS

from . import Jotul
from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_devices):
    """Add switch for passed entry in HA."""
    jotul: Jotul = hass.data[DOMAIN][entry.entry_id]

    async_add_devices([
        JotulTargetTemperatureNumber(jotul),
        JotulPowerNumber(jotul)
    ])


class JotulTargetTemperatureNumber(NumberEntity):
    """Representation of a Number."""

    def __init__(self, jotul: Jotul):
        """Initialize the number."""
        self._attr_native_max_value = 30
        self._attr_native_min_value = 20
        self._attr_native_value = None
        self._attr_native_step = 1
        self._attr_name = f"{jotul.name}_target_temperature"
        self.jotul = jotul

    @property
    def name(self) -> str:
        """Return the name of the number."""
        return f'{self.jotul.name} Target Temperature'

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return "mdi:thermometer"

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the number.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = self.jotul.get_target_temperature()
    
    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = self.jotul.set_target_temperature(value)


class JotulPowerNumber(NumberEntity):
    """Representation of a Number."""

    def __init__(self, jotul: Jotul):
        """Initialize the number."""
        self._attr_native_max_value = 5
        self._attr_native_min_value = 1
        self._attr_native_value = None
        self._attr_native_step = 1
        self._attr_name = f"{jotul.name}_power"
        self.jotul = jotul

    @property
    def name(self) -> str:
        """Return the name of the number."""
        return f'{self.jotul.name} Power'

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return "mdi:fire"

    def update(self) -> None:
        """Fetch new state data for the number.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = self.jotul.get_power()
    
    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = self.jotul.set_power(int(value))

