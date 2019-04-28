import logging
import voluptuous as vol
import asyncio

from homeassistant.components.light import Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_DEVICES
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
DOMAIN = "hass_reopenwebnet"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): vol.All(cv.ensure_list,[
        {
            vol.Required(CONF_NAME): cv.string,
            vol.Required('address'): cv.string,
        }
    ])
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    gate = hass.data[DOMAIN]
    add_devices(MyHomeLight(light,gate) for light in config[CONF_DEVICES])

class MyHomeLight(Light):
    def __init__ (self, light, gate):
        self._gate = gate
        self._name = light[CONF_NAME]
        self._address = light['address']
        self._state = False
        self._brightness = 0

    @asyncio.coroutine
    def async_added_toHass(self):
        yield from self.hass.async_add_job(update())

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def brightness(self):
        return self._brightness

    def turn_on(self, **kwargs):
        self._gate.normal_request(1, self._address, 1)

    def turn_off(self, **kwargs):
        self._gate.normal_request(1, self._address, 0)

    def update(self):
        state = self._gate.status_request(1, self._address)
        self._state = state == '1'
        self.schedule_update_ha_state()
