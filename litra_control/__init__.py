"""Litra Control - Individual device control for Logitech Litra lights."""

from .driver import LitraDriver
from .device import LitraDevice
from .constants import LITRA_DEVICES

__all__ = ['list_devices']

def list_devices():
    """Find and return all connected Litra devices.
    
    Returns:
        list[LitraDevice]: List of LitraDevice objects
    """
    driver = LitraDriver()
    count = driver.scan()
    
    devices = []
    for idx in range(count):
        usb_dev = driver.get_device(idx)
        
        product_id = usb_dev.idProduct
        default_name = "Litra Unknown"
        for product in LITRA_DEVICES:
            if product["id"] == product_id:
                default_name = product["name"]
                break
        
        devices.append(LitraDevice(idx, default_name, product_id, driver, usb_dev))
    
    return devices
