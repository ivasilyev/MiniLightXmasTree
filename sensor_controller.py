from machine import Pin
from utime import sleep
from onewire import OneWire
from ds18x20 import DS18X20


class SensorController:
    def __init__(self, pin: int, polling_interval: int = 1):
        self.temperature_sensor = DS18X20(OneWire(Pin(pin)))
        self.temperature_chips = self.temperature_sensor.scan()
        self.pause = polling_interval
        self.state = dict(temperature=dict())
        print("The sensor controller module started")

    def read_temperature(self):
        for chip in self.temperature_chips:
            chip_id = "".join(map(chr, chip))
            chip_data = self.temperature_sensor.read_temp(chip)
            self.state["temperature"][chip_id] = chip_data

    def run(self):
        while True:
            self.read_temperature()
            sleep(self.pause)
