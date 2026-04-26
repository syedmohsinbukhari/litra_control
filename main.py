#!/usr/bin/env python3
"""Example usage of litra_control."""

from litra_control import list_devices


def main():
    devices = list_devices()

    if not devices:
        print("No Litra devices found")
        return

    print(f"Found {len(devices)} device(s):")
    for dev in devices:
        print(f"  [{dev.index}] {dev.name} (PID: 0x{dev.product_id:04x})")

    print()

    # Control each device individually
    if devices:
        print("Controlling device 0 only...")
        devices[0].on()
        devices[0].set_brightness(100)
        devices[0].set_temperature(2700)
        print(f"  Device 0: on={devices[0].is_on}, brightness={devices[0].brightness}, temp={devices[0].temperature}")

    if len(devices) > 1:
        print("Controlling device 1 only (different settings)...")
        devices[1].on()
        devices[1].set_brightness(30)
        devices[1].set_temperature(6500)
        print(f"  Device 1: on={devices[1].is_on}, brightness={devices[1].brightness}, temp={devices[1].temperature}")


if __name__ == "__main__":
    main()
