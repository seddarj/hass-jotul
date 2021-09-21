"""The Jotul integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, STATUS_CODES

import logging, requests, json, time

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["number", "sensor", "switch"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Jotul from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = Jotul(
        entry.data.get("host"),
        entry.data.get("name")
    )

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class Jotul:
    def __init__(self, host, name):
        _LOGGER.info(f"Starting Jotul integration for {host} ({name})")
        self.name = name
        self.host = host
        self.endpoint = f'http://{host}/cgi-bin/sendmsg.lua'

    def get_status(self):
        resp = self._query_stove('GET STATUS')
        if resp:
            return resp.get("DATA", {}).get("STATUS", 0)
        return 0

    def get_temperature(self):
        resp = self._query_stove('GET TMPS')
        if resp:
            return resp.get("DATA", {}).get("T1", 0)
        return 0

    def get_target_temperature(self):
        resp = self._query_stove('GET SETP')
        if resp:
            return resp.get("DATA", {}).get("SETP", 0)
        return 0

    def set_target_temperature(self, value: float):
        resp = self._query_stove(f'SET SETP {str(value)}')
        if resp:
            return resp.get("DATA", {}).get("SETP", 0)
        return 0

    def set_power(self, value: int):
        resp = self._query_stove(f'SET POWR {str(value)}')
        if resp:
            return resp.get("DATA", {}).get("PWR", 1)
        return 1

    def get_power(self):
        return self._get('PWR')

    def _get(self, attr, default=0):
        resp = self._query_stove('GET ALLS')
        if resp:
            return resp.get("DATA", {}).get(attr, default)
        return 0

    def set_status(self, status):
        if status not in ["ON", "OFF"]:
            _LOGGER.error(f"Invalid status {status}")
            raise ValueError
        self._query_stove(f'CMD {status}')

    def _query_stove(self, op):
        _LOGGER.debug(f'Sending request to stove: {op}')

        if op is None:
            return False

        retry = 0
        success = False

        params = {"cmd": op}

        while not success :
            try:
                response = requests.get(self.endpoint, params=params, timeout=30)
            except requests.exceptions.ReadTimeout:
                _LOGGER.error(f'Timeout reached querying {self.endpoint}')
                _LOGGER.error(f'Please check if you can ping {self.host}')
                return False
            except requests.exceptions.ConnectTimeout:
                _LOGGER.error(f'Please check host {self.host}')
                return False

            if response == False:
                return False

            response_json = json.loads(response.text)
            success = response_json.get('SUCCESS', False)

            # cbox return error
            if not success:
                _LOGGER.error(f'Error returned by CBox - retrying in 2 seconds ({op})')
                time.sleep(2)
                retry = retry + 1

                if retry == 3 :
                     _LOGGER.error(f'Error returned by CBox - stop retry after 3 attempts ({op})')
                     break

        return response_json
