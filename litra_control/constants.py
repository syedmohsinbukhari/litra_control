"""Protocol constants for Logitech Litra devices."""

VENDOR_ID = 0x046d

LITRA_DEVICES = [
    {"name": "Litra Glow", "id": 0xc900, "endpoint": 0x02, "buffer_length": 64},
    {"name": "Litra Beam", "id": 0xc901, "endpoint": 0x01, "buffer_length": 32},
]

MIN_BRIGHTNESS = 0x14
MAX_BRIGHTNESS = 0xfa
MIN_TEMPERATURE = 2700
MAX_TEMPERATURE = 6500
TIMEOUT_MS = 3000

CMD_PREFIX = [0x11, 0xff, 0x04]
CMD_ON = 0x1c
CMD_OFF = 0x1c
CMD_BRIGHTNESS = 0x4c
CMD_TEMPERATURE = 0x9c

LIGHT_OFF = 0x00
LIGHT_ON = 0x01
