from machine import Pin
from utime import sleep
from onewire import OneWire
from ds18x20 import DS18X20

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


class SensorController:
    def __init__(self, pin: int, pause: int = 1):
        self._pin = pin
        self._temperature_sensor = DS18X20(OneWire(Pin(pin)))
        self._temperature_chips = self._temperature_sensor.scan()
        self.pause = pause
        self.state = dict(temperature=dict())
        print("The sensor controller module started")

    def __repr__(self):
        return "SensorController object on pin {}".format(self._pin)

    async def read_temperature(self):
        while True:
            for chip in self._temperature_chips:
                chip_id = "".join(map(chr, chip))
                try:
                    chip_data = self._temperature_sensor.read_temp(chip)
                    self.state["temperature"][chip_id] = chip_data
                except:  # CRC error
                    continue
            print(self.state["temperature"])
            await asyncio.sleep(self.pause)

    def run(self):
        loop = asyncio.get_event_loop()
        _ = loop.create_task(self.read_temperature())
        loop.run_forever()
