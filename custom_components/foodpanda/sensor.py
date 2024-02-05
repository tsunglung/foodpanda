"""Support for the foodpanda."""
import logging
from typing import Callable
from http import HTTPStatus

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_USERNAME
)

from .const import (
    ATTRIBUTION,
    ATTR_ETA,
    ATTR_RESTAURANT_NAME,
    ATTR_COURIER_NAME,
    ATTR_COURIER_PHONE,
    ATTR_COURIER_DESCRIPTION,
    ATTR_TITLE_SUMMARY,
    ATTR_SUBTITLE_SUMMARY,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_HTTPS_RESULT,
    ATTR_LIST,
    BASE_URL,
    DEFAULT_NAME,
    DOMAIN,
    FOODPANDA_DATA,
    FOODPANDA_COORDINATOR,
    FOODPANDA_ORDERS,
    MANUFACTURER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config: ConfigEntry, async_add_devices: Callable
) -> None:
    """Set up the foodpanda Sensor from config."""

    if config.data.get(CONF_USERNAME, None):
        username = config.data[CONF_USERNAME]
    else:
        username = config.options[CONF_USERNAME]

    data = hass.data[DOMAIN][config.entry_id][FOODPANDA_DATA]
    data.expired = False
    data.ordered = False
    coordinator = hass.data[DOMAIN][config.entry_id][FOODPANDA_COORDINATOR]
    device = foodpandaSensor(username, data, coordinator)

    async_add_devices([device], update_before_add=True)


class foodpandaSensor(SensorEntity):
    """Implementation of a foodpanda sensor."""

    def __init__(self, username, data, coordinator):
        """Initialize the sensor."""
        self._state = None
        self._data = data
        self._coordinator = coordinator
        self._attributes = {}
        self._attr_value = {}
        self._name = "{} {}".format(DEFAULT_NAME, username)
        self._username = username

        self.uri = BASE_URL

    @property
    def unique_id(self):
        """Return an unique ID."""
        uid = self._name.replace(" ", "_")
        return f"{uid}_orders"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} Orders"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:food-variant"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return None

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""
        self._attributes[ATTR_ATTRIBUTION] = ATTRIBUTION
        for i in ATTR_LIST:
            self._attributes[i] = self._attr_value[i]
        return self._attributes

    @property
    def device_info(self):
        return {
            'identifiers': {(DOMAIN, self._username)},
            'manufacturer': MANUFACTURER,
            'name': self._name
        }

    async def async_added_to_hass(self) -> None:
        """Set up a listener and load data."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self._update_callback)
        )
        self._update_callback()

    @callback
    def _update_callback(self) -> None:
        """Load data from integration."""
        self.async_write_ha_state()

    async def async_update(self):
        """Schedule a custom update via the common entity update service."""
        await self._coordinator.async_request_refresh()

        for i in ATTR_LIST:
            self._attr_value[i] = ''
        try:
            if self._username in self._data.orders:
                orders = self._data.orders[self._username].get(FOODPANDA_ORDERS, [])
                self._state = len(orders)
                if len(orders) >= 1:
                    orders = self._data.orders[self._username][FOODPANDA_ORDERS]
                    for order in orders:
                        self._attr_value[ATTR_ETA] = self._attr_value[ATTR_ETA] + "; " + order['eta']
                        self._attr_value[ATTR_TITLE_SUMMARY] = self._attr_value[ATTR_TITLE_SUMMARY] + "; " + data['current_status']['message']
                        ss = "{} {} {}".format(
                            data['delivery_time_range']['label'], data['delivery_time_range']['suffix'], data['delivery_time_range']['range'])
                        self._attr_value[ATTR_SUBTITLE_SUMMARY] = self._attr_value[ATTR_SUBTITLE_SUMMARY] + "; " + ss
                        self._attr_value[ATTR_COURIER_DESCRIPTION] = self._attr_value[ATTR_COURIER_DESCRIPTION] + "; " + data['courier']['vehicle_type']
                        self._attr_value[ATTR_RESTAURANT_NAME] = self._attr_value[ATTR_RESTAURANT_NAME] + "; " + data['vendor']['name']
                        name = "{} {}".format(
                            data['courier']['name'], data['courier']['id']
                        )
                        self._attr_value[ATTR_COURIER_NAME] = self._attr_value[ATTR_COURIER_NAME] + "; " + name
                        self._attr_value[ATTR_COURIER_PHONE] = self._attr_value[ATTR_COURIER_PHONE] + "; " + data['courier']['phone']
                        self._attr_value[ATTR_LATITUDE] = self._attr_value[ATTR_LATITUDE] + "; " + data['courier']['latitude']
                        self._attr_value[ATTR_LONGITUDE] = self._attr_value[ATTR_LONGITUDE] + "; " + data['courier']['longitude']

        except:
            self._state = 0

        for i in ATTR_LIST:
            self._attr_value[i] = self._attr_value[i].lstrip(';').lstrip()

        self._attr_value[ATTR_HTTPS_RESULT] = self._data.orders[self._username].get(
            ATTR_HTTPS_RESULT, 'Unknown')
        if self._attr_value[ATTR_HTTPS_RESULT] == HTTPStatus.FORBIDDEN:
            self._state = None

        return