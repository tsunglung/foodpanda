"""Upload foodpanda Button instances."""
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_USERNAME

from .const import (
    DEFAULT_NAME,
    DOMAIN,
    FOODPANDA_DATA,
    FOODPANDA_COORDINATOR,
    MANUFACTURER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, async_add_devices):
    """Set up the binary sensors from a config entry."""

    cookie = None
    if config.data.get(CONF_USERNAME, None):
        username = config.data[CONF_USERNAME]
    else:
        username = config.options[CONF_USERNAME]

    data = hass.data[DOMAIN][config.entry_id][FOODPANDA_DATA]
    coordinator = hass.data[DOMAIN][config.entry_id][FOODPANDA_COORDINATOR]
    device = foodpandaButton(username, data, coordinator)

    async_add_devices([device], update_before_add=True)

class foodpandaButton(ButtonEntity):
    """Represent a binary sensor."""

    def __init__(self, username, data, coordinator):
        """Set initializing values."""
        super().__init__()
        self._name = "{} {}".format(DEFAULT_NAME, username)
        self._attributes = {}
        self._username = username
        self._data = data
        self._coordinator = coordinator

    @property
    def unique_id(self):
        """Return an unique ID."""
        uid = self._name.replace(" ", "_")
        return f"{uid}_order"

    @property
    def name(self):
        """Return the name of the button."""
        return f"{self._name} Order"

    @property
    def device_info(self):
        """Return Device Info."""
        return {
            'identifiers': {(DOMAIN, self._username)},
            'manufacturer': MANUFACTURER,
            'name': self._name
        }

    async def async_press(self) -> None:
        """Press the button."""
        self._data.ordered = True
        await self._coordinator.async_request_refresh()