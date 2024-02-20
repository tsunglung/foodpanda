"""Config flow to configure foodpanda component."""
import logging
from typing import Optional
import voluptuous as vol

from homeassistant import core, exceptions
from homeassistant.config_entries import (
    CONN_CLASS_CLOUD_POLL,
    ConfigFlow,
    OptionsFlow,
    ConfigEntry
    )
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_TOKEN
from homeassistant.core import callback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_DEVICE_TOKEN,
    CONF_REFRESH_TOKEN,
    CONF_LOCALCODE,
    CONF_X_DEVICE,
    DEFAULT_LOCALCODE,
    LOCALCODES
)
from .data import foodpandaData

ACTIONS = {"cloud": "Add foodpanda Account", "token": "Add foodpanda by Tokens"}

_LOGGER = logging.getLogger(__name__)

async def validate_input(hass: core.HomeAssistant, data):
    """Validate that the user input allows us to connect to DataPoint.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    session = async_get_clientsession(hass)
    login_info = {
        CONF_USERNAME: data[CONF_USERNAME],
        CONF_PASSWORD: data.get(CONF_PASSWORD, ""),
        CONF_TOKEN: data.get(CONF_TOKEN, ""),
        CONF_DEVICE_TOKEN: data.get(CONF_DEVICE_TOKEN, ""),
        CONF_REFRESH_TOKEN: data.get(CONF_REFRESH_TOKEN, ""),
        CONF_LOCALCODE: data[CONF_LOCALCODE],
        CONF_X_DEVICE: data[CONF_X_DEVICE]
    }

    foodpanda_data = foodpandaData(hass, session, login_info)
    foodpanda_data.expired = False
    foodpanda_data.ordered = True
    await foodpanda_data.async_update_data()
    if foodpanda_data.username is None:
        raise CannotConnect()

    return {CONF_USERNAME: foodpanda_data.username}

class foodpandaFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a foodpanda config flow."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._username: Optional[str] = None
        self._password: Optional[str] = None
        self._localcode: Optional[str] = None
        self._x_device: Optional[str] = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """ get option flow """
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            if user_input["action"] == CONF_TOKEN:
                return await self.async_step_token()
            return await self.async_step_cloud()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("action", default="cloud"): vol.In(ACTIONS)}
            ),
        )

    async def async_step_cloud(
        self,
        user_input: Optional[ConfigType] = None
    ):
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_USERNAME]}"
            )
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                user_input[CONF_USERNAME] = info[CONF_USERNAME]
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_LOCALCODE, default=DEFAULT_LOCALCODE): vol.In(
                    list(LOCALCODES.keys())
                ),
                vol.Required(CONF_X_DEVICE, default=''): str
            }
        )

        return self.async_show_form(
            step_id="cloud", data_schema=data_schema, errors=errors
        )

    async def async_step_token(self, user_input: dict = None, error=None):

        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_USERNAME]}"
            )
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                user_input[CONF_USERNAME] = info[CONF_USERNAME]
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_TOKEN): str,
                vol.Required(CONF_DEVICE_TOKEN): str,
                vol.Required(CONF_REFRESH_TOKEN): str,
                vol.Required(CONF_LOCALCODE, default=DEFAULT_LOCALCODE): vol.In(
                    list(LOCALCODES.keys())
                ),
                vol.Optional(CONF_X_DEVICE, default=''): str
            }
        )

        return self.async_show_form(
            step_id=CONF_TOKEN, data_schema=data_schema, errors=errors
        )

    @property
    def _name(self):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        return self.context.get(CONF_USERNAME)

    @_name.setter
    def _name(self, value):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        self.context[CONF_USERNAME] = value
        self.context["title_placeholders"] = {"name": self._username}


class OptionsFlowHandler(OptionsFlow):
    # pylint: disable=too-few-public-methods
    """Handle options flow changes."""
    _username = None
    _password = None
    _token = None
    _device_token = None
    _refresh_token = None
    _localcode = None
    _x_device = None

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if CONF_TOKEN in self.config_entry.options:
            return await self.async_step_token()
        return await self.async_step_cloud()

    async def async_step_cloud(self, user_input=None):
        """Manage the options."""
        errors = {}
        if user_input is not None:
            user_input[CONF_USERNAME] = self._username
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                user_input[CONF_USERNAME] = info[CONF_USERNAME]
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )

        self._username = self.config_entry.options.get(CONF_USERNAME, '')
        self._password = self.config_entry.options.get(CONF_PASSWORD, '')
        self._localcode = self.config_entry.options.get(CONF_LOCALCODE, '')
        self._x_device = self.config_entry.options.get(CONF_X_DEVICE, '')

        return self.async_show_form(
            step_id="cloud",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PASSWORD, default=self._password): str,
                    vol.Required(CONF_LOCALCODE, default=self._localcode): vol.In(
                        list(LOCALCODES.keys())
                    ),
                    vol.Required(CONF_X_DEVICE, default=self._x_device): str
                }
            ),
            errors=errors
        )

    async def async_step_token(self, user_input=None):
        """Manage the options."""
        errors = {}
        if user_input is not None:
            user_input[CONF_USERNAME] = self._username
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                user_input[CONF_USERNAME] = info[CONF_USERNAME]
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )

        self._username = self.config_entry.options.get(CONF_USERNAME, '')
        self._token = self.config_entry.options.get(CONF_TOKEN, '')
        self._device_token = self.config_entry.options.get(CONF_DEVICE_TOKEN, '')
        self._refresh_token = self.config_entry.options.get(CONF_REFRESH_TOKEN, '')
        self._localcode = self.config_entry.options.get(CONF_LOCALCODE, '')
        self._x_device = self.config_entry.options.get(CONF_X_DEVICE, '')

        return self.async_show_form(
            step_id=CONF_TOKEN,
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TOKEN, default=self._token): str,
                    vol.Required(CONF_DEVICE_TOKEN, default=self._device_token): str,
                    vol.Required(CONF_REFRESH_TOKEN, default=self._refresh_token): str,
                    vol.Required(CONF_LOCALCODE, default=self._localcode): vol.In(
                        list(LOCALCODES.keys())
                    ),
                    vol.Optional(CONF_X_DEVICE, default=self._x_device): str
                }
            ),
            errors=errors
        )

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
