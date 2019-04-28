
import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT
import reopenwebnet
from reopenwebnet import CommandClient
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

def setup(hass, config):
    host = config[DOMAIN].get(CONF_HOST)
    port = config[DOMAIN].get(CONF_PORT)
    password = config[DOMAIN].get(CONF_PASSWORD)
    hass.data[DOMAIN] = Client(host, port, password)
    return True

class Client():
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.client = CommandClient(self.host, self.port, self.password)

    def normal_request(self, who, where, what):
        self.client.normal_request(1, where, what)
        
    def status_request(self, who, where):
        return self.client.request_state(who, where) 
