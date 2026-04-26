import os
import json

CONFIG_DIR = os.path.expanduser("~/.config/litra_control")
CONFIG_FILE = os.path.join(CONFIG_DIR, "devices.json")


def _load_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_device_name(index):
    config = _load_config()
    return config.get(str(index))


def set_device_name(index, name):
    config = _load_config()
    config[str(index)] = name
    _save_config(config)


def get_all_devices():
    return _load_config()


def remove_device(index):
    config = _load_config()
    key = str(index)
    if key in config:
        del config[key]
        _save_config(config)
