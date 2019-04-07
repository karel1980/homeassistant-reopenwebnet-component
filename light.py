#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Support for My Home Platform TEST light71

"""
import voluptuous as vol
import asyncio

from homeassistant.components.light import Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_DEVICES
import homeassistant.helpers.config_validation as cv

DOMAIN = "my_home"

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
    def __init__ (self,light,gate):
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
        brightness = kwargs.get('brightness', None)
        if brightness is None:
            self._gate.light_command(self._address, self._brightness)
            self._state = True
        elif brightness == 0:
            self._gate.light_off(self._address)
            self._state = False
            self._brightness = 0
        elif brightness <= 2:
            self._state = True
            self._brightness = 2
            self._gate.light_command(self._address, '2')
        elif brightness <= 10:
            self._state = True
            self._brightness = brightness 
            self._gate.light_command(self._address, str(brightness))
        else:
            self._state = True
            self._brightness = 10
            self._gate.light_command(self._address, str(brightness))

    def turn_off(self, **kwargs):
        self._gate.light_off(self._address)
        self._state = False

    def update(self):
        state = self._gate.light_status(self._address)
        if state is None:
            self._state = False
        if state == '0':
            self._state = False
        elif state == '1':
            self._state = True
            self._brightness = 10
        elif int(state) <= 2:
            self._state = True
            self._brightness = 2
        elif int(state) <= 10:
            self._state = True
            self._brightness = int(state) 
        else:
            self._state = True
            self._brightness = 10

        self.schedule_update_ha_state()
