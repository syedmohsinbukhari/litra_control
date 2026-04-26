#!/usr/bin/env python3
"""MCP Server for Litra Control.

This server exposes Litra device control as MCP tools for AI integration.
Run with: python mcp_server.py
Server runs on http://0.0.0.0:8000/mcp
"""

from fastmcp import FastMCP
from litra_control import list_devices

mcp = FastMCP("Litra Control")


def _find_device(name: str):
    devices = list_devices()
    for dev in devices:
        if dev.display_name.lower() == name.lower():
            return dev
    for dev in devices:
        if name.lower() in dev.display_name.lower():
            return dev
    return None


@mcp.tool()
def list_lights() -> list[str]:
    """List all connected Litra devices by their display names."""
    devices = list_devices()
    return [dev.display_name for dev in devices]


@mcp.tool()
def get_light_info(name: str) -> dict:
    """Get the current status of a Litra light.
    
    Args:
        name: The display name of the light (e.g., "RightLight", "LeftLight")
    
    Returns:
        Dict with keys: name, on, brightness, temperature
    """
    dev = _find_device(name)
    if not dev:
        return {"error": f"Light '{name}' not found"}
    
    return {
        "name": dev.display_name,
        "on": dev.is_on,
        "brightness": dev.brightness,
        "temperature": dev.temperature
    }


@mcp.tool()
def set_light_on(name: str) -> str:
    """Turn on a Litra light.
    
    Args:
        name: The display name of the light
    """
    dev = _find_device(name)
    if not dev:
        return f"Error: Light '{name}' not found"
    
    dev.on()
    return f"{dev.display_name} turned on"


@mcp.tool()
def set_light_off(name: str) -> str:
    """Turn off a Litra light.
    
    Args:
        name: The display name of the light
    """
    dev = _find_device(name)
    if not dev:
        return f"Error: Light '{name}' not found"
    
    dev.off()
    return f"{dev.display_name} turned off"


@mcp.tool()
def set_brightness(name: str, level: int) -> str:
    """Set the brightness of a Litra light.
    
    Args:
        name: The display name of the light
        level: Brightness level (0-100)
    """
    if level < 0 or level > 100:
        return "Error: Brightness must be between 0 and 100"
    
    dev = _find_device(name)
    if not dev:
        return f"Error: Light '{name}' not found"
    
    dev.set_brightness(level)
    return f"{dev.display_name} brightness set to {level}%"


@mcp.tool()
def set_temperature(name: str, kelvin: int) -> str:
    """Set the color temperature of a Litra light.
    
    Args:
        name: The display name of the light
        kelvin: Color temperature in Kelvin (2700-6500)
    """
    if kelvin < 2700 or kelvin > 6500:
        return "Error: Temperature must be between 2700K and 6500K"
    
    dev = _find_device(name)
    if not dev:
        return f"Error: Light '{name}' not found"
    
    dev.set_temperature(kelvin)
    return f"{dev.display_name} temperature set to {kelvin}K"


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
