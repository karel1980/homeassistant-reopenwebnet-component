import logging
import voluptuous as vol
import asyncio

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_NAME, CONF_ACCESS_TOKEN, CONF_NAME, CONF_PATH, CONF_URL, CONF_DEVICES)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)
DOMAIN = "hass_reopenwebnet"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): vol.All(cv.ensure_list,[
        {
            vol.Required(CONF_NAME): cv.string,
            vol.Required('who'): cv.string,
            vol.Required('address'): cv.string,
        }
    ])
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    gate = hass.data[DOMAIN]
    add_devices([OpenWebNetSensor(sensor, gate) for sensor in config[CONF_DEVICES]])

class OpenWebNetSensor(Entity):
    def __init__(self, sensor, gate):
        self._gate = gate
        self._name = sensor[CONF_NAME]
        self._who = sensor['who']
        self._address = sensor['address']
        self._state = '0'

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        state = self._gate.status_request(self._who, self._address)
        if state != None:
            self._state = state
