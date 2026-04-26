"""Device class for individual Litra device control."""

from .driver import LitraDriver
from .constants import (
    CMD_PREFIX, CMD_ON, CMD_OFF, CMD_BRIGHTNESS, CMD_TEMPERATURE,
    LIGHT_OFF, LIGHT_ON, MIN_BRIGHTNESS, MAX_BRIGHTNESS,
    MIN_TEMPERATURE, MAX_TEMPERATURE
)
from . import config


class LitraDevice:
    def __init__(self, index, name, product_id, driver, usb_device):
        self._index = index
        self._default_name = name
        self._product_id = product_id
        self._driver = driver
        self._usb_device = usb_device
        self._is_on = False
        self._brightness = 0
        self._temperature = MIN_TEMPERATURE

    @property
    def index(self):
        return self._index

    @property
    def name(self):
        return self._default_name

    @property
    def product_id(self):
        return self._product_id

    @property
    def serial(self):
        return None

    @property
    def display_name(self):
        custom = config.get_device_name(self._index)
        return custom if custom else self._default_name

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @property
    def temperature(self):
        return self._temperature

    def set_name(self, name):
        config.set_device_name(self._index, name)

    def _send(self, cmd_bytes):
        self._driver.send_command(self._index, cmd_bytes)

    def on(self):
        cmd = CMD_PREFIX + [CMD_ON, LIGHT_ON] + [0] * 15
        self._send(cmd)
        self._is_on = True

    def off(self):
        cmd = CMD_PREFIX + [CMD_OFF, LIGHT_OFF] + [0] * 15
        self._send(cmd)
        self._is_on = False

    def set_brightness(self, level):
        if level < 0 or level > 100:
            raise ValueError("Brightness must be between 0 and 100")

        adjusted = int(MIN_BRIGHTNESS + (level / 100) * (MAX_BRIGHTNESS - MIN_BRIGHTNESS))
        cmd = CMD_PREFIX + [CMD_BRIGHTNESS, 0x00, adjusted] + [0] * 14
        self._send(cmd)
        self._brightness = level

    def set_temperature(self, temp):
        if temp < MIN_TEMPERATURE or temp > MAX_TEMPERATURE:
            msg = "Temperature must be between {} and {}".format(MIN_TEMPERATURE, MAX_TEMPERATURE)
            raise ValueError(msg)

        temp_bytes = temp.to_bytes(2, byteorder="big")
        cmd = CMD_PREFIX + [CMD_TEMPERATURE, temp_bytes[0], temp_bytes[1]] + [0] * 14
        self._send(cmd)
        self._temperature = temp
    
    def close(self):
        self._driver.close()
