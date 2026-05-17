#!/usr/bin/env python3
"""HTTP REST Server for Litra Control.

Exposes Litra device control as REST endpoints.
Run with: python http_server.py
Server runs on http://0.0.0.0:8000/docs (Swagger UI)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from litra_control import list_devices

_driver = None
_devices_cache = None


def _find_device(name: str):
    global _devices_cache
    if _devices_cache is None:
        _devices_cache = list_devices()
    if not name:
        return None
    for dev in _devices_cache:
        if dev.display_name.lower() == name.lower():
            return dev
    for dev in _devices_cache:
        if name.lower() in dev.display_name.lower():
            return dev
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _driver, _devices_cache
    _devices_cache = list_devices()
    if _devices_cache:
        _driver = _devices_cache[0]._driver
    yield
    if _driver:
        _driver.close()


app = FastAPI(
    title="Litra Control API",
    description="REST API for controlling Logitech Litra desk lights",
    version="0.1.0",
    lifespan=lifespan,
)


class BrightnessRequest(BaseModel):
    level: int


class TemperatureRequest(BaseModel):
    kelvin: int


class LightInfo(BaseModel):
    name: str
    on: bool
    brightness: int
    temperature: int


class MessageResponse(BaseModel):
    message: str


@app.get("/", response_model=dict)
def root():
    return {
        "service": "Litra Control API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/lights", response_model=list[str])
def list_lights():
    global _devices_cache
    if _devices_cache is None:
        _devices_cache = list_devices()
    return [dev.display_name for dev in _devices_cache]


@app.get("/lights/{name}", response_model=LightInfo)
def get_light(name: str):
    dev = _find_device(name)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Light '{name}' not found")
    return LightInfo(
        name=dev.display_name,
        on=dev.is_on,
        brightness=dev.brightness,
        temperature=dev.temperature,
    )


@app.post("/lights/{name}/on", response_model=MessageResponse)
def set_light_on(name: str):
    dev = _find_device(name)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Light '{name}' not found")
    dev.on()
    return MessageResponse(message=f"{dev.display_name} turned on")


@app.post("/lights/{name}/off", response_model=MessageResponse)
def set_light_off(name: str):
    dev = _find_device(name)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Light '{name}' not found")
    dev.off()
    return MessageResponse(message=f"{dev.display_name} turned off")


@app.patch("/lights/{name}/brightness", response_model=MessageResponse)
def set_brightness(name: str, body: BrightnessRequest):
    if body.level < 0 or body.level > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Brightness must be between 0 and 100")
    dev = _find_device(name)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Light '{name}' not found")
    dev.set_brightness(body.level)
    return MessageResponse(message=f"{dev.display_name} brightness set to {body.level}%")


@app.patch("/lights/{name}/temperature", response_model=MessageResponse)
def set_temperature(name: str, body: TemperatureRequest):
    if body.kelvin < 2700 or body.kelvin > 6500:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Temperature must be between 2700K and 6500K")
    dev = _find_device(name)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Light '{name}' not found")
    dev.set_temperature(body.kelvin)
    return MessageResponse(message=f"{dev.display_name} temperature set to {body.kelvin}K")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
