"""Platform for switch integration."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant

from . import Jotul
from .const import DOMAIN, STATUS_CODES


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_devices):
    """Add switch for passed entry in HA."""
    jotul: Jotul = hass.data[DOMAIN][entry.entry_id]

    async_add_devices([
        JotulStatusSwitch(jotul)
    ])


class JotulStatusSwitch(SwitchEntity):
    """Representation of a Switch."""

    def __init__(self, jotul: Jotul):
        """Initialize the switch."""
        self._state = None
        self._attr_is_on = False
        self._attr_name = f"{jotul.name}_status"
        self.jotul = jotul

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return f'{self.jotul.name} Status'

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return "mdi:power"

    def update(self) -> None:
        """Fetch new state data for the switch.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_is_on = self.jotul.get_status() > 1

    def turn_on(self) -> None:
        """Turn on the device.
        """
        self.jotul.set_status('ON')

    def turn_off(self) -> None:
        """Turn off the device.
        """
        self.jotul.set_status('OFF')
