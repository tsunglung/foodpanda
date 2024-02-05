"""Constants of the foodpanda component."""
from datetime import timedelta

DEFAULT_NAME = "foodpanda"
DOMAIN = "foodpanda"
PLATFORMS = [ "binary_sensor", "button", "sensor" ]
DATA_KEY = "data_foodpanda"

ATTR_ETA = "eta"
ATTR_RESTAURANT_NAME = "restaurant_name"
ATTR_COURIER_NAME = "courier_name"
ATTR_COURIER_PHONE = "courier_phone"
ATTR_COURIER_DESCRIPTION = "courier_description"
ATTR_TITLE_SUMMARY = "title_summary"
ATTR_SUBTITLE_SUMMARY = "subtitle_summary"
ATTR_LATITUDE = "latitude"
ATTR_LONGITUDE = "longitude"
ATTR_HTTPS_RESULT = "https_result"
ATTR_LIST = [
    ATTR_ETA,
    ATTR_RESTAURANT_NAME,
    ATTR_COURIER_NAME,
    ATTR_COURIER_DESCRIPTION,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_SUBTITLE_SUMMARY,
    ATTR_TITLE_SUMMARY,
    ATTR_HTTPS_RESULT
]

DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

CONF_LOCALCODE = "localcode"
CONF_TOKEN_TIMEOUT = "token_timeout"
CONF_DEVICE_TOKEN = "device_token"
CONF_REFRESH_TOKEN = "refresh_token"
CONF_REFRESH_TOKEN_TIMEOUT = "refresh_token_timeout"
CONF_CLIENTID = "clientid"
CONF_SESSIONID = "sessionid"
CONF_USERSOURCE = "usersouce"
CONF_X_DEVICE = "x_device"
ATTRIBUTION = "Powered by foodpanda Data"
MANUFACTURER = "foodpanda"
DEFAULT_LOCALCODE = "tw"
FOODPANDA_COORDINATOR = "foodpanda_coordinator"
FOODPANDA_DATA = "foodpanda_data"
FOODPANDA_NAME = "foodpanda_name"
FOODPANDA_ORDERS = "orders"
UPDATE_LISTENER = "update_listener"
DEFAULT_LOCALCODE = "tw"

DEFAULT_X_DEVICE = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImtleW1ha2VyLXZvbG8tZGV2aWNlLWZwLXR3IiwidHlwIjoiSldUIn0.eyJpZCI6IjEzNTI4MjhjLWM0MTAtNDgyZi05ZjZkLTk2MGE4NDdiNzRkMCIsImNsaWVudF9pZCI6InZvbG8iLCJ1c2VyX2lkIjoidHdrMGNzcjMiLCJleHBpcmVzIjo0ODYwNDUyODYzLCJ0b2tlbl90eXBlIjoiYmVhcmVyIiwic2NvcGUiOiJERVZJQ0VfVE9LRU4ifQ.bNa-xs2e7LQcX9HkBNHQcwrc9m5JhV-34qXAaBvCT1yOV8fPT9udzXsRTXa1nt7Wx4l-oe58SKx-BGH5j75bJxgQRoZNl6oktaV_3M_GrjPLp4v1aqTQQCLVBhHbVfSn2Tm115M6WrfkG-paKgaBvwjqxKD2u3P7FniP5SnW8bchaph8t4hwlJOMbSC8vgIlyN0nCFUdjgWVEcil8MTkAndXE4OClx5_ebUo4mt5EiLeR8qiKTWgH0_aHmzu_kc9KX_lrHtQbyzDgsMjZiqSx8XdL4bOgNbKgUPqh3uaP6hvMtHdOepf3aCfrW7rMMQOLydXI5Kw2_dfasgoX-GDww"

HA_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
BASE_URL = 'https://www.foodpanda.com.tw/login/new/api'
BASE_TW_URL = 'https://tw.fd-api.com/api/v5'

REQUEST_TIMEOUT = 10  # seconds

LOCALCODES = {
    "en": "America/Los_Angeles",
    "tw": "Asia/Taipei"
}
