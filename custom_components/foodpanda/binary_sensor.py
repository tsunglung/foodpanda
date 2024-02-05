"""Upload foodpanda New Order binary sensor instances."""
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import CONF_USERNAME

from .const import (
    DEFAULT_NAME,
    DOMAIN,
    FOODPANDA_DATA,
    MANUFACTURER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, async_add_devices):
    """Set up the binary sensors from a config entry."""

    if config.data.get(CONF_USERNAME, None):
        username = config.data[CONF_USERNAME]
    else:
        username = config.options[CONF_USERNAME]

    data = hass.data[DOMAIN][config.entry_id][FOODPANDA_DATA]
    device = foodpandaBinarySensor(hass, data, username)

    async_add_devices([device], update_before_add=True)

class foodpandaBinarySensor(BinarySensorEntity):
    """Represent a binary sensor."""

    def __init__(self, hass, data, username):
        """Set initializing values."""
        super().__init__()
        self._name = "{} {}".format(DEFAULT_NAME, username)
        self._attributes = {}
        self._state = False
        self._username = username
        self._data = data
        self._https_result = None
        self.hass = hass

    @property
    def unique_id(self):
        """Return an unique ID."""
        uid = self._name.replace(" ", "_")
        return f"{uid}_new_order"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} New Order"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._data.new_order

    @property
    def device_info(self):
        """Return Device Info."""
        return {
            'identifiers': {(DOMAIN, self._username)},
            'manufacturer': MANUFACTURER,
            'name': self._name
        }
