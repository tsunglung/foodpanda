"""Common foodpanda Data class used by both sensor and entity."""

import logging
from datetime import datetime, timezone
import json
from http import HTTPStatus
import requests
from aiohttp.hdrs import (
    ACCEPT,
    AUTHORIZATION,
    CONTENT_TYPE,
    METH_GET,
    METH_POST,
    USER_AGENT 
)
from dateutil import tz as timezone

from homeassistant.helpers.storage import Store
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_TOKEN,
    CONTENT_TYPE_JSON,
    EVENT_HOMEASSISTANT_STOP
)
from .const import (
    ATTR_HTTPS_RESULT,
    LOGIN_URLS,
    BASE_URLS,
    CONF_CLIENTID,
    CONF_LOCALCODE,
    CONF_DEVICE_TOKEN,
    CONF_TOKEN_TIMEOUT,
    CONF_REFRESH_TOKEN,
    CONF_REFRESH_TOKEN_TIMEOUT,
    CONF_SESSIONID,
    CONF_USERSOURCE,
    CONF_X_DEVICE,
    DEFAULT_X_DEVICE,
    DOMAIN,
    HA_USER_AGENT,
    REQUEST_TIMEOUT,
    FOODPANDA_ORDERS
)

_LOGGER = logging.getLogger(__name__)


class foodpandaData():
    """Class for handling the data retrieval."""

    def __init__(self, hass, session, login_info):
        """Initialize the data object."""
        self._hass = hass
        self._session = session
        self._username = login_info[CONF_USERNAME]
        self._password = login_info[CONF_PASSWORD]
        self._localcode = login_info[CONF_LOCALCODE]
        self.orders = {}
        self.username = None
        self.expired = False
        self.ordered = False
        self.new_order = False
        self.uri = BASE_URLS.get(self._localcode, BASE_URLS["tw"])
        self.orders[login_info[CONF_USERNAME]] = {}
        self._last_check = datetime.now().timestamp()
        self._token = login_info[CONF_TOKEN]
        self._device_token = login_info[CONF_DEVICE_TOKEN]
        self._refresh_token = login_info[CONF_REFRESH_TOKEN]
        self._token_timeout = 0
        self._refresh_token_timeout = 0
        self._x_device = login_info[CONF_X_DEVICE] if len(login_info[CONF_X_DEVICE]) >= 1 else DEFAULT_X_DEVICE
        self._clientid = None
        self._sessionid = None
        self._usersource = "volo"

    def _format_cookies(self, cookies: str):
        """ format cookies """
        cookies_dict = {}
        for line in cookies.splitlines():
            cookie = line.replace("Set-Cookie: ", "")
            item = 0
            cookie_dict = {}
            for data in cookie.split(";"):
                if "=" in data:
                    key = data.split("=")[0].lstrip()
                    value = data.split("=")[1].lstrip()
                    cookie_dict[key] = value
                    if item == 0:
                        cookies_dict[key] = cookie_dict
                item = item + 1

        return cookies_dict

    async def async_login(self):
        """ do login """

        headers = {
            USER_AGENT: HA_USER_AGENT,
            CONTENT_TYPE: CONTENT_TYPE_JSON,
            ACCEPT: 'application/json, text/plain, */*',
            'x-device': self._x_device,
            'x-otp-method': 'EMAIL',
        }
        payload={
            CONF_USERNAME: self._username,
            CONF_PASSWORD: self._password
        }

        try:
            response = await self._session.request(
                METH_POST,
                url=f"{LOGIN_URLS['tw']}/login",
                data=json.dumps(payload),
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )

        except requests.exceptions.RequestException:
            _LOGGER.error("Failed fetching data for %s", self._username)
            return

        if response.status == HTTPStatus.OK:
            cookies = self._format_cookies(str(response.cookies))
            self._token = cookies.get(CONF_TOKEN, {}).get(CONF_TOKEN, "")
            self._token_timeout = cookies.get(CONF_TOKEN, {}).get("expires", "")
            self._device_token = cookies.get(CONF_DEVICE_TOKEN, {}).get(CONF_DEVICE_TOKEN, "")
            self._refresh_token = cookies.get(CONF_REFRESH_TOKEN, {}).get(CONF_REFRESH_TOKEN, "")
            self._refresh_token_timeout = cookies.get(CONF_REFRESH_TOKEN, {}).get("expires", "")
            self._clientid = cookies.get("dhhPerseusGuestId", {}).get("dhhPerseusGuestId", "")
            self._sessionid = cookies.get("dhhPerseusSessionId", {}).get("dhhPerseusSessionId", "")
            self._usersource = cookies.get("userSource", {}).get("userSource", self._usersource)
            try:
                self._token_timeout = int(datetime.strptime(
                    self._token_timeout, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.gettz('Etc/GMT0')).timestamp())
                self._refresh_token_timeout = int(datetime.strptime(
                    self._refresh_token_timeout, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.gettz('Etc/GMT0')).timestamp())
            except:
                self._token_timeout = 1893459660
                self._refresh_token_timeout = 1893459660
        else:
            info = ""
            self.orders[self._username][ATTR_HTTPS_RESULT] = response.status
            if response.status == HTTPStatus.FORBIDDEN:
                info = " Token is expired"
            _LOGGER.error(
                "Failed fetching data for %s (HTTP Status Code = %d).%s",
                self._username,
                response.status,
                info
            )

    async def async_refresh_token(self):
        """ do refresh token """
        payload = {
            "country": self._localcode,
            "platform": "b2c",
            CONF_DEVICE_TOKEN: self._device_token,
            CONF_REFRESH_TOKEN: self._refresh_token
        }

        headers = {
            USER_AGENT: HA_USER_AGENT,
            CONTENT_TYPE: f"{CONTENT_TYPE_JSON};charset=UTF-8",
            ACCEPT: 'application/json, text/plain, */*',
            'x-device': self._x_device,
            'x-otp-method': 'EMAIL',
        }

        uri = LOGIN_URLS.get(self._localcode, LOGIN_URLS["tw"])
        try:
            response = await self._session.request(
                METH_POST,
                url=f"{uri}/refresh-token",
                data=json.dumps(payload),
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )

        except requests.exceptions.RequestException:
            _LOGGER.error("Failed fetching data for %s", self._username)
            return

        if response.status == HTTPStatus.OK:
            cookies = self._format_cookies(str(response.cookies))
            self._token = cookies.get(CONF_TOKEN, {}).get(CONF_TOKEN, self._token)
            self._device_token = cookies.get(CONF_DEVICE_TOKEN, {}).get(CONF_DEVICE_TOKEN, self._device_token)
            self._token_timeout = cookies.get(CONF_TOKEN, {}).get("expires", self._token_timeout)
            self._refresh_token_timeout = cookies.get(CONF_REFRESH_TOKEN, {}).get("expires", self._refresh_token_timeout)
            self._refresh_token = cookies.get(CONF_REFRESH_TOKEN, {}).get(CONF_REFRESH_TOKEN, self._refresh_token)
            self._clientid = cookies.get("dhhPerseusGuestId", {}).get("dhhPerseusGuestId", self._clientid)
            self._sessionid = cookies.get("dhhPerseusSessionId", {}).get("dhhPerseusSessionId", self._sessionid)
            self._usersource = cookies.get("userSource", {}).get("userSource", self._usersource)

            try:
                self._token_timeout = int(datetime.strptime(
                    self._token_timeout, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.gettz('Etc/GMT0')).timestamp())
                self._refresh_token_timeout = int(datetime.strptime(
                    self._refresh_token_timeout, "%a, %d %b %Y %H:%M:%S %Z").replace(
                        tzinfo=timezone.gettz('Etc/GMT0')).timestamp())
            except:
                pass
            return True
        else:
            info = ""
            self.orders[self._username][ATTR_HTTPS_RESULT] = response.status
            if response.status == HTTPStatus.FORBIDDEN:
                info = " Token is expired"
            _LOGGER.error(
                "Failed fetching data for %s (HTTP Status Code = %d).%s",
                self._username,
                response.status,
                info
            )
        return False

    async def async_load_tokens(self) -> dict:
        """
        Update tokens in .storage
        """
        if self._token is not None:
            return {
                CONF_TOKEN: self._token,
                CONF_DEVICE_TOKEN: self._device_token,
                CONF_TOKEN_TIMEOUT: self._token_timeout,
                CONF_REFRESH_TOKEN: self._refresh_token,
                CONF_REFRESH_TOKEN_TIMEOUT: self._refresh_token_timeout,
                CONF_CLIENTID: self._clientid,
                CONF_SESSIONID: self._sessionid,
                CONF_USERSOURCE: self._usersource,
                CONF_X_DEVICE: self._x_device,
                CONF_LOCALCODE: self._localcode
            }

        default = {
                CONF_TOKEN: "",
                CONF_TOKEN_TIMEOUT: "1577836800",
                CONF_REFRESH_TOKEN: "",
                CONF_REFRESH_TOKEN_TIMEOUT: "1577836800"
            }
        store = Store(self._hass, 1, f"{DOMAIN}/tokens.json")
        data = await store.async_load() or None
        if not data:
            # force login
            return default
        tokens = data.get(self._username, default)

        # noinspection PyUnusedLocal
        async def stop(*args):
            # save devices data to .storage
            tokens = {
                CONF_TOKEN: self._token,
                CONF_DEVICE_TOKEN: self._device_token,
                CONF_TOKEN_TIMEOUT: self._token_timeout,
                CONF_REFRESH_TOKEN: self._refresh_token,
                CONF_REFRESH_TOKEN_TIMEOUT: self._refresh_token_timeout,
                CONF_X_DEVICE: self._x_device,
                CONF_CLIENTID: self._clientid,
                CONF_SESSIONID: self._sessionid,
                CONF_USERSOURCE: self._usersource,
                CONF_LOCALCODE: self._localcode
            }
            data[self._username] = tokens

            await store.async_save(data)

        self._hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop)
        return tokens

    async def async_store_tokens(self, tokens: dict):
        """
        Update tokens in .storage
        """
        store = Store(self._hass, 1, f"{DOMAIN}/tokens.json")
        data = await store.async_load() or {}
        data[self._username] = tokens

        await store.async_save(data)

    async def async_check_tokens(self):
        """ check the tokens if valid """
        tokens = await self.async_load_tokens()

        self._token = tokens.get(CONF_TOKEN, "")
        self._device_token = tokens.get(CONF_DEVICE_TOKEN, "")
        token_timeout = str(tokens.get(CONF_TOKEN_TIMEOUT, 0))
        self._refresh_token = tokens.get(CONF_REFRESH_TOKEN, "")
        refresh_token_timeout = str(tokens.get(CONF_REFRESH_TOKEN_TIMEOUT, 0))
        self._clientid = tokens.get(CONF_CLIENTID, "")
        self._sessionid = tokens.get(CONF_SESSIONID, "")
        self._usersource = tokens.get(CONF_USERSOURCE, "volo")
        self._x_device = tokens.get(CONF_X_DEVICE, "")

        if not isinstance(token_timeout, str):
            token_timeout = "1577836800"
        if not isinstance(refresh_token_timeout, str):
            refresh_token_timeout = "1577836800"

        now = datetime.now().timestamp()
        # configure foodpanda by tokens, there is not timeout of tokens.
        # do not login
        if len(self._password) < 1 or refresh_token_timeout == 0:
            refresh_token_timeout = int(now) + 31440000
            self._clientid = "1707192686179.449358429208716900.iohek328rn"
            self._sessionid = "1707192686179.978673916504541700.vnuoeucgts"

        self._token_timeout = token_timeout = int(token_timeout)
        self._refresh_token_timeout = refresh_token_timeout = int(refresh_token_timeout)

        updated_refresh_token = False
        timeout = refresh_token_timeout

        if ((int(timeout - now) < 86400) and
                len(self._password) >= 1):
            if self._localcode in ["hk", "sg"]:
                return False
            await self.async_login()
            if len(self._token) < 1:
                return False
            updated_refresh_token = True
            await self.async_store_tokens({
                CONF_TOKEN: self._token,
                CONF_DEVICE_TOKEN: self._device_token,
                CONF_TOKEN_TIMEOUT: self._token_timeout,
                CONF_REFRESH_TOKEN: self._refresh_token,
                CONF_REFRESH_TOKEN_TIMEOUT: self._refresh_token_timeout,
                CONF_CLIENTID: self._clientid,
                CONF_SESSIONID: self._sessionid,
                CONF_USERSOURCE: self._usersource,
                CONF_X_DEVICE: self._x_device,
                CONF_LOCALCODE: self._localcode
            })

        timeout = token_timeout

        if ((int(timeout - now) < 600) and
                not updated_refresh_token):
            ret = await self.async_refresh_token()
            if not ret:
                return False
            await self.async_store_tokens({
                CONF_TOKEN: self._token,
                CONF_DEVICE_TOKEN: self._device_token,
                CONF_TOKEN_TIMEOUT: self._token_timeout,
                CONF_REFRESH_TOKEN: self._refresh_token,
                CONF_REFRESH_TOKEN_TIMEOUT: self._refresh_token_timeout,
                CONF_CLIENTID: self._clientid,
                CONF_SESSIONID: self._sessionid,
                CONF_USERSOURCE: self._usersource,
                CONF_X_DEVICE: self._x_device,
                CONF_LOCALCODE: self._localcode
            })

        self.username = self._username
        return True

    async def async_check_order_history(self):
        """ check the order history """
        """ https://tw.fd-api.com/api/v5/orders/order_history?include=order_products,order_details """
        payload = {}
        headers = {
            USER_AGENT: HA_USER_AGENT,
            AUTHORIZATION: f"Bearer {self._token}",
            CONTENT_TYPE: CONTENT_TYPE_JSON,
            ACCEPT: 'application/json, text/plain, */*',
            'Perseus-Client-Id': self._clientid,
            'Perseus-Session-Id': self._sessionid,
            'X-Fp-Api-Key': self._usersource
        }
        try:
            response = await self._session.request(
                METH_GET,
                url=f"{self.uri}/orders/order_history?include=order_products",
                data=json.dumps(payload),
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )

        except requests.exceptions.RequestException:
            _LOGGER.error("Failed fetching data for %s", self._username)
            return

        orders = []
        if response.status == HTTPStatus.OK:
            try:
                res = await response.json()
            except:
                res = {"data": response.text}

            data = res.get('data', {})
            self.orders[self._username] = {}
            if len(data) >= 1:
                for item in data['items']:
                    if (item['current_status']['code'] != 16 and item['current_status']['code'] != 13):
                        orders.append(item)
            self.orders[self._username][ATTR_HTTPS_RESULT] = response.status
        else:
            info = ""
            self.orders[self._username][ATTR_HTTPS_RESULT] = response.status
            if response.status == HTTPStatus.FORBIDDEN:
                info = " Token is expired"
            _LOGGER.error(
                "Failed fetching data for %s (HTTP Status Code = %d).%s",
                self._username,
                response.status,
                info
            )

        return orders


    async def async_order_tracking(self, order_code):
        """ check the order tracking """
        payload = {}
        headers = {
            USER_AGENT: HA_USER_AGENT,
            AUTHORIZATION: f"Bearer {self._token}",
            CONTENT_TYPE: CONTENT_TYPE_JSON,
            ACCEPT: 'application/json, text/plain, */*',
            'X-Fp-Api-Key': self._usersource
        }
        params = {
            "order_status_variation": "Control"
        }

        try:
            response = await self._session.request(
                METH_GET,
                url=f"{self.uri}/tracking/orders/{order_code}",
                data=json.dumps(payload),
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )

        except requests.exceptions.RequestException:
            _LOGGER.error("Failed fetching data for %s", self._username)
            return
        data = {}

        if response.status == HTTPStatus.OK:
            try:
                res = await response.json()
            except:
                res = {"data": response.text}
            data = res.get('data', {})
            if len(data) >= 1:
                self.orders[self._username][FOODPANDA_ORDERS].append(data)
            self.orders[self._username][ATTR_HTTPS_RESULT] = HTTPStatus.OK
            self.expired = False
        elif response.status == HTTPStatus.NOT_FOUND:
            self.orders[self._username][ATTR_HTTPS_RESULT] = HTTPStatus.NOT_FOUND
            self.expired = True
        else:
            info = ""
            self.orders[self._username][ATTR_HTTPS_RESULT] = response.status
            if response.status == HTTPStatus.FORBIDDEN:
                info = " Token is expired"
                _LOGGER.error(
                    "Failed fetching data for %s (HTTP Status Code = %d).%s",
                    self._username,
                    response.status,
                    info
                )
                self.expired = True
            elif self.expired:
                self.orders[self._username][ATTR_HTTPS_RESULT] = 'sessions_expired'
                _LOGGER.warning(
                    "Failed fetching data for %s (Sessions expired)",
                    self._username,
                )
        return data

    async def async_update_data(self):
        """Get the latest data for foodpanda from REST service."""

        force_update = False
        now = datetime.now().timestamp()

        if (int(now - self._last_check) > 300):
            force_update = True
            self._last_check = now

        if not self.expired and (self.ordered or force_update):

            ret = await self.async_check_tokens()
            if not ret:
                return self

            data = await self.async_check_order_history()
            if len(data) < 1:
                self.new_order = False
                self.ordered = False
                return self

            if len(data) >= 1:
                self.new_order = True
                self.ordered = True
                self.orders[self._username][FOODPANDA_ORDERS] = []
                for order in data:
                    await self.async_order_tracking(order['order_code'])
        return self
