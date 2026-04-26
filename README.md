# litra-control

Individual device control for Logitech Litra Glow and Litra Beam lights.

This package allows you to control multiple Litra devices independently, each with its own on/off state, brightness, and temperature settings.

## Features

- List all connected Litra devices
- Control each device individually
- Set brightness (0-100%)
- Set color temperature (2700K-6500K)
- Persistent device naming via config file
- Works on Linux with libusb

## Installation

```bash
cd ~/workspace/litra_control
pip install -e .
```

Requires: Python 3.6+, pyusb, fastmcp

## Usage

```python
from litra_control import list_devices

# Find all connected devices
devices = list_devices()

# Control individually
devices[0].on()                                    # Turn on
devices[0].set_brightness(75)                     # Set brightness 75%
devices[0].set_temperature(4000)                  # Set 4000K (neutral)

devices[1].off()                                  # Turn off

# Or use display names (configured in ~/.config/litra_control/devices.json)
for dev in devices:
    print(dev.display_name)  # e.g., "RightLight", "LeftLight"

# Set custom name
devices[0].set_name("Desk Lamp")
```

### Device Properties

- `device.display_name` - Configured name or default ("Litra Glow"/"Litra Beam")
- `device.is_on` - Boolean, on/off state
- `device.brightness` - Integer 0-100
- `device.temperature` - Integer 2700-6500

### Device Methods

- `device.on()` - Turn on
- `device.off()` - Turn off
- `device.set_brightness(level)` - Set brightness (0-100)
- `device.set_temperature(temp)` - Set temperature (2700-6500K)
- `device.set_name(name)` - Save custom name to config
- `device.close()` - Close USB session

## MCP Server

This package includes an MCP (Model Context Protocol) server for AI integration with tools like Claude Desktop, Cursor, and other MCP-compatible AI clients.

### Running the Server

```bash
cd ~/workspace/litra_control
python mcp_server.py
```

The server runs on `http://0.0.0.0:8000/mcp` and is accessible on your local network at:
`http://elcid-raspberry-pi-zero-2w.local:8000/mcp`

### Available Tools

| Tool | Description |
|------|-------------|
| `list_lights` | List all connected Litra devices |
| `get_light_info` | Get status (on/off, brightness, temperature) |
| `set_light_on` | Turn on a light |
| `set_light_off` | Turn off a light |
| `set_brightness` | Set brightness (0-100) |
| `set_temperature` | Set temperature (2700-6500K) |

### Client Configuration

**Claude Desktop:**
Add to your Claude Desktop config (typically `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "litra-control": {
      "url": "http://elcid-raspberry-pi-zero-2w.local:8000/mcp"
    }
  }
}
```

**Cursor:**
Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "litra-control": {
      "url": "http://elcid-raspberry-pi-zero-2w.local:8000/mcp"
    }
  }
}
```

### Example AI Prompts

Once connected, you can ask your AI assistant:
- "Turn on the RightLight"
- "Set LeftLight brightness to 50%"
- "Set both lights to 4000K"
- "What's the current status of all lights?"

## USB Permissions

On Linux, you may need udev rules to access the device without sudo:

```bash
# For Litra Glow
sudo tee /etc/udev/rules.d/82-litra-glow.rules <<< 'SUBSYSTEM=="usb", ATTR{idVendor}=="046d", ATTR{idProduct}=="c900",MODE="0666"'

# For Litra Beam
sudo tee /etc/udev/rules.d/82-litra-beam.rules <<< 'SUBSYSTEM=="usb", ATTR{idVendor}=="046d", ATTR{idProduct}=="c901",MODE="0666"'

sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Credits

This project is based on the [litra-driver](https://github.com/kharyam/litra-driver) project by Khary Mendez. The USB protocol bytes and command formats were reverse-engineered from that project.

## License

This project is licensed under the GNU General Public License v3 (GPLv3). See the LICENSE file for details.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.