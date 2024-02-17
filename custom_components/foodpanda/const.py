"""Constants of the foodpanda component."""
from datetime import timedelta

DEFAULT_NAME = "foodpanda"
DOMAIN = "foodpanda"
PLATFORMS = [ "binary_sensor", "button", "device_tracker", "sensor" ]
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

LOGIN_URLS = {
    "tw": 'https://www.foodpanda.com.tw/login/new/api',
    "hk": 'https://www.foodpanda.hk/login/new/api',
    "sg": 'https://www.foodpanda.sg/login/new/api'
}

BASE_URLS = {
    "tw": 'https://tw.fd-api.com/api/v5',
    "hk": 'https://hk.fd-api.com/api/v5',
    "sg": 'https://sg.fd-api.com/api/v5'
}

REQUEST_TIMEOUT = 10  # seconds

LOCALCODES = {
#    "en": "America/Los_Angeles",
    "tw": "Asia/Taipei",
    "hk": "Asia/Hong_Kong",
    "sg": "Asia/Singapore"
}

LANGUAGE_TRANSLATIONS = {
    "en": {
        "shop.order.status.message_awaiting_vendor_confirmation": "Awaiting vendor confirmation",
        "shop.order.status.message_order_accepted_by_vendor": "Order accepted by vendor",
        "shop.order.status.message_order_picked_by_rider": "Order picked by rider",
        "shop.order.status.message_order_rider_arrived": "Order rider arrvied"
    },
    "tw": {
        "shop.order.status.message_awaiting_vendor_confirmation": "\u8a02\u55ae\u6b63\u5728\u6e96\u5099\u4e2d\u3002",
        "shop.order.status.message_order_accepted_by_vendor": "\u9910\u5ef3\u5df2\u63a5\u53d7\u8a02\u55ae",
        "shop.order.status.message_order_picked_by_rider": "\u6b63\u524d\u5f80\u9818\u53d6\u8a02\u55ae\u3002",
        "shop.order.status.message_order_rider_arrived": "\u5373\u5c07\u62b5\u9054\u3002"
    }
}