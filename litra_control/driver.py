"""Core USB driver for Litra devices."""

import time
import usb.core
import usb.util
from .constants import VENDOR_ID, LITRA_DEVICES, TIMEOUT_MS


class LitraDriver:
    def __init__(self):
        self._devices = []
        self._serials = {}
        self._endpoints = {}
        self._buffer_lengths = {}
        self._session = None

    def scan(self):
        """Scan for all connected Litra devices."""
        self._devices = []
        self._serials = {}
        self._endpoints = {}
        self._buffer_lengths = {}

        for product in LITRA_DEVICES:
            found = usb.core.find(idVendor=VENDOR_ID, idProduct=product["id"], find_all=True)
            for dev in found:
                idx = len(self._devices)
                self._devices.append(dev)
                try:
                    self._serials[idx] = dev.serial_number
                except Exception:
                    self._serials[idx] = None
                self._endpoints[idx] = product["endpoint"]
                self._buffer_lengths[idx] = product["buffer_length"]

        return len(self._devices)

    def get_device(self, index):
        """Get device by index."""
        if index >= len(self._devices):
            raise IndexError(f"Device index {index} out of range")
        return self._devices[index]

    def get_serial(self, index):
        """Get serial number by index."""
        return self._serials.get(index)

    def _open_session(self, index):
        """Open USB session for a device."""
        if self._session is not None:
            self._close_session()
        
        time.sleep(0.2)  # Wait before trying to open
        
        dev = self._devices[index]
        endpoint = self._endpoints[index]
        buffer_len = self._buffer_lengths[index]
        
        reattach = False
        try:
            if dev.is_kernel_driver_active(0):
                reattach = True
                dev.detach_kernel_driver(0)
        except AttributeError:
            pass

        try:
            dev.set_configuration()
        except Exception as e:
            print("Warning: set_configuration failed, trying to continue: {}".format(e))
        
        time.sleep(0.5)
        
        try:
            usb.util.claim_interface(dev, 0)
        except Exception as e:
            print("Warning: claim_interface failed: {}".format(e))
            # Try to continue anyway
            pass
        
        time.sleep(0.5)
        
        self._session = {
            'dev': dev,
            'endpoint': endpoint,
            'buffer_len': buffer_len,
            'reattach': reattach
        }
        
        return self._session

    def _close_session(self):
        """Close USB session."""
        if self._session is None:
            return
        
        try:
            dev = self._session['dev']
            reattach = self._session['reattach']
            
            try:
                usb.util.dispose_resources(dev)
            except Exception as e:
                print("Warning during dispose: {}".format(e))
            
            if reattach:
                try:
                    dev.attach_kernel_driver(0)
                except Exception:
                    pass
        except Exception as e:
            print("Warning during close: {}".format(e))
        
        self._session = None

    def send_command(self, index, cmd_bytes):
        """Send command to specific device."""
        # Always open a fresh session for each command to avoid issues
        self._open_session(index)
        
        dev = self._session['dev']
        endpoint = self._session['endpoint']
        buffer_len = self._session['buffer_len']

        try:
            dev.write(endpoint, cmd_bytes, TIMEOUT_MS)
            time.sleep(1.0)
            dev.read(endpoint, buffer_len, TIMEOUT_MS)
        except Exception as e:
            print("Warning during send: {}".format(e))
        finally:
            self._close_session()

    def close(self):
        """Close the current session."""
        self._close_session()
