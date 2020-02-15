
import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT
import reopenwebnet
from reopenwebnet.gatewayproxy import GatewayProxy
from reopenwebnet.config import Config
from threading import Lock

import homeassistant.helpers.config_validation as cv

DOMAIN = "hass_reopenwebnet"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_PORT, default = '20000'): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):
    host = config[DOMAIN].get(CONF_HOST)
    port = config[DOMAIN].get(CONF_PORT)
    password = config[DOMAIN].get(CONF_PASSWORD)
    config = Config(host, port, password)
    gw = GatewayProxy(config)
    print("CREATING GATEWAYPROXY")
    hass.data[DOMAIN] = gw
    gw.start()
    return True

