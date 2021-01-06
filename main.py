from utime import sleep_ms
from neopixel import NeoPixel
from machine import Pin
from random import choice

pixels = NeoPixel(pin=Pin(27), n=25, bpp=3)
pixels.fill((255, 255, 255))
pixels.write()

while True:
for idx in range(pixels.n):
pixels[idx] = tuple([choice(range(256)) for _ in "rgb"])
pixels.write()
sleep_ms(100)
pixels[idx] = (0, 0, 0)

import machine, onewire, ds18x20

ds_pin = machine.Pin(14)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

while True:
ds_sensor.convert_temp()
sleep_ms(750)
for rom in roms:
print(rom)
print(ds_sensor.read_temp(rom))
time.sleep(5)

