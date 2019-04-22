
import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT
from reopenwebnet import CommandClient

import homeassistant.helpers.config_validation as cv

DOMAIN = "hass_reopenwebnet"
REQUIREMENTS = ['reopenwebnet==1.4.1']

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_PORT, default = '20000'): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)

def setup(hass,config):
    host = config[DOMAIN].get(CONF_HOST)
    port = config[DOMAIN].get(CONF_PORT)
    password = config[DOMAIN].get(CONF_PASSWORD)
    hass.data[DOMAIN] = CommandClient(host,port,password)
    return True
