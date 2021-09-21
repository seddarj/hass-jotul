"""Config flow for Jotul integration."""
from __future__ import annotations

import logging, aiohttp, json
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Required("name"): str
    }
)


class JotulHub:
    """JotulHub
    """

    def __init__(self, host: str, name: str) -> None:
        """Initialize."""
        self.host = host
        self.name = name

    async def test_connection(self) -> bool:
        """Test if we can connect to the host."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{self.host}/cgi-bin/sendmsg.lua', params={'cmd': 'GET'}) as response:                    
                    if response.status != 200 : 
                        _LOGGER.error("Error during api request : http status returned is {}".format(response.status))
                        return False
                    else:
                        json.loads(await response.text())
        except aiohttp.ClientError as client_error:
            _LOGGER.error("Error during api request: {emsg}".format(emsg=client_error))
            return False
        except json.decoder.JSONDecodeError as err:
            _LOGGER.error("Error during json parsing: response unexpected from Cbox")
            return False
        return True


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    hub = JotulHub(data["host"], data["name"])

    if not await hub.test_connection():
        raise CannotConnect

    # Return info that you want to store in the config entry.
    return {"title": data["name"]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Jotul."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
