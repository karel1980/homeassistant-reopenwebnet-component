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
        """ Create an openwebnet light instance """
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
        """ Return name of this light. """
        return self._name

    @property
    def brightness(self):
        """ Return brightness of this light. """
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def brightness(self):
        return self._brightness

    def turn_on(self, **kwargs):
        brightness = kwargs.get('brightness', 255)
        gwstate = brightness_to_gwstate(brightness)
        self._gate.normal_request(1, self._address, gwstate)
        self._state = True
        self._brightness = brightness

    def turn_off(self, **kwargs):
        self._gate.normal_request(1, self._address, 0)
        self._state = False
        self._brightness = 0

    def update(self):
        gwstate = self._gate.status_request(1, self._address)

        if gwstate is not None:
            self._state = gwstate != '0'
            old_gwstate = brightness_to_gwstate(self._brightness)
            if old_gwstate != gwstate:
                self._brightness = state_to_brightness(gwstate)

        self.schedule_update_ha_state()

def brightness_to_gwstate(brightness):
    """ Returns openwebnet state corresponding to given brightness. Brightness 0 returns state 0, brightness 1 to 255 returns states from 2 to 10 """
    if brightness <= 0:
        return '0'

    if brightness > 255:
        return '10'

    return str(int(((brightness - 1) * 8 / 254) + 2))

def state_to_brightness(gwstate):
    """ Map openwebnet state to a brightness level
        Rules:
          - 0 => 0
          - 1, 10 => 255
          - 2-9 => 1-254
    """

    gwstate = int(gwstate)
    if gwstate <= 0:
        return 0
    elif gwstate == 1 or gwstate >= 10:
        return 255
    else:
        width = 253.0 / 8
        center = int((0.5 + gwstate - 2) * width)
        return center

