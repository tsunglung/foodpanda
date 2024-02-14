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
    CONF_LOCALCODE,
    DEFAULT_NAME,
    DOMAIN,
    FOODPANDA_DATA,
    FOODPANDA_COORDINATOR,
    FOODPANDA_ORDERS,
    LANGUAGE_TRANSLATIONS,
    MANUFACTURER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config: ConfigEntry, async_add_devices: Callable
) -> None:
    """Set up the foodpanda Sensor from config."""

    if config.data.get(CONF_USERNAME, None):
        username = config.data[CONF_USERNAME]
        localcode = config.data[CONF_LOCALCODE]
    else:
        username = config.options[CONF_USERNAME]
        localcode = config.options[CONF_LOCALCODE]

    data = hass.data[DOMAIN][config.entry_id][FOODPANDA_DATA]
    data.expired = False
    data.ordered = False
    coordinator = hass.data[DOMAIN][config.entry_id][FOODPANDA_COORDINATOR]
    device = foodpandaSensor(username, localcode, data, coordinator)

    async_add_devices([device], update_before_add=True)


class foodpandaSensor(SensorEntity):
    """Implementation of a foodpanda sensor."""

    def __init__(self, username, localcode, data, coordinator):
        """Initialize the sensor."""
        self._state = None
        self._data = data
        self._coordinator = coordinator
        self._attributes = {}
        self._attr_value = {}
        self._name = "{} {}".format(DEFAULT_NAME, username)
        self._username = username

        self._localcode = localcode

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
        self._attributes = {}
        self._attributes[ATTR_ATTRIBUTION] = ATTRIBUTION
        for k, _ in self._attr_value.items():
            self._attributes[k] = self._attr_value[k]
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

        self._attr_value = {}
        for i in ATTR_LIST:
            self._attr_value[i] = ''
        try:
            if self._username in self._data.orders:
                orders = self._data.orders[self._username].get(FOODPANDA_ORDERS, [])
                self._state = len(orders)
                index = 0
                if len(orders) >= 1:
                    if self._localcode in LANGUAGE_TRANSLATIONS:
                        translations = LANGUAGE_TRANSLATIONS[self._localcode]
                    else:
                        translations = LANGUAGE_TRANSLATIONS["en"]

                    for order in orders:
                        if index == 0:
                            if "eta" in order:
                                self._attr_value[ATTR_ETA] = order['eta']
                            if "current_status" in order:
                                msg = order['current_status']['message']
                                self._attr_value[ATTR_TITLE_SUMMARY] = translations.get(msg, msg)
                            if "delivery_time_range" in order:
                                ss = "{} {} {}".format(
                                    order['delivery_time_range']['label'], order['delivery_time_range']['range'], order['delivery_time_range']['suffix'])
                                self._attr_value[ATTR_SUBTITLE_SUMMARY] = ss
                            if "vendor" in order:
                                self._attr_value[ATTR_RESTAURANT_NAME] = order['vendor']['name']
                            if order.get('courier', {}) != None:
                                self._attr_value[ATTR_COURIER_DESCRIPTION] = order['courier']['vehicle_type']
                                name = "{} ({})".format(
                                    order['courier']['name'], order['courier']['id']
                                )
                                self._attr_value[ATTR_COURIER_NAME] = name
                                self._attr_value[ATTR_COURIER_PHONE] = order['courier']['phone']
                                self._attr_value[ATTR_LATITUDE] = str(order['courier']['latitude'])
                                self._attr_value[ATTR_LONGITUDE] = str(order['courier']['longitude'])
                        if index >= 1:
                            if "eta" in order:
                                self._attr_value[f"{ATTR_ETA}_{index + 1}"] = order['eta']
                            if "current_status" in order:
                                msg = order['current_status']['message']
                                self._attr_value[f"ATTR_TITLE_SUMMARY}_{index + 1}"] = translations.get(msg, msg)
                            if "delivery_time_range" in order:
                                ss = "{} {} {}".format(
                                    order['delivery_time_range']['label'], order['delivery_time_range']['range'], order['delivery_time_range']['suffix'])
                                self._attr_value[f"{ATTR_SUBTITLE_SUMMARY}_{index + 1}"] = ss
                            if "vendor" in order:
                                self._attr_value[f"{ATTR_RESTAURANT_NAME}_{index + 1}"] = order['vendor']['name']
                            if order.get('courier', {}) != None:
                                self._attr_value[f"{ATTR_COURIER_DESCRIPTION}_{index + 1}"] = order['courier']['vehicle_type']
                                name = "{} ({})".format(
                                    order['courier']['name'], order['courier']['id']
                                )
                                self._attr_value[f"{ATTR_COURIER_NAME}_{index + 1}"] =  name
                                self._attr_value[f"{ATTR_COURIER_PHONE}_{index + 1}"] = order['courier']['phone']
                                self._attr_value[f"{ATTR_LATITUDE}_{index + 1}"] = str(order['courier']['latitude'])
                                self._attr_value[f"{ATTR_LONGITUDE}_{index + 1}"] = str(order['courier']['longitude'])
                        index = index + 1

        except Exception as e:
            _LOGGER.error(f"paring orders occured exception {e}")
            self._state = 0

        self._attr_value[ATTR_HTTPS_RESULT] = self._data.orders[self._username].get(
            ATTR_HTTPS_RESULT, 'Unknown')
        if self._attr_value[ATTR_HTTPS_RESULT] == HTTPStatus.FORBIDDEN:
            self._state = None

        return
