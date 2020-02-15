import logging
import voluptuous as vol
import asyncio

from homeassistant.components.light import Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_DEVICES
import homeassistant.helpers.config_validation as cv

from reopenwebnet import messages

_LOGGER = logging.getLogger(__name__)
DOMAIN = "hass_reopenwebnet"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): vol.All(cv.ensure_list,[
        {
            vol.Required(CONF_NAME): cv.string,
            vol.Required('address'): cv.string,
            vol.Optional('debug'): cv.boolean,
        }
    ])
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    gate = hass.data[DOMAIN]
    add_devices(MyHomeLight(light,gate) for light in config[CONF_DEVICES])

class MyHomeLight(Light):
    def __init__ (self, light, gate):
        """ Create an openwebnet light instance """
        self._gate = gate
        self._name = light[CONF_NAME]
        self._address = light['address']
        self._debug = light.get('debug', False)

        self._state = False
        self._brightness = 0

        self.register_listener()

    def debug_print(self, *args, **kwargs):
        if self._debug:
            print(*args, **kwargs)

    def register_listener(self):
        def on_change(msg):
            self.debug_print("LIGHT received update", self._address, msg)
            self.process_msg(msg)
            self.schedule_update_ha_state()

        self._gate.register_listener('1', self._address, on_change)

    def process_msg(self, msg):
        if msg.what == '0':
            self._state = False 
        else:
            self._state = 1
            self._brightness = 255

        #TODO: handle 2-9 values
        #TODO: meaning of 10?

    @asyncio.coroutine
    def async_added_toHass(self):
        yield from self.hass.async_add_job(update())

    @property
    def name(self):
        return self._name

    @property
    def brightness(self):
        return self._brightness

    @property
    def is_on(self):
        return self._state

    async def turn_on(self, **kwargs):
        await self._gate.cmd(messages.NormalMessage('1', '1', self._address))

    async def turn_off(self, **kwargs):
        await self._gate.cmd(messages.NormalMessage('1', '0', self._address))

    def update(self):
        # nothing needed to do, state should always be in sync
        pass

