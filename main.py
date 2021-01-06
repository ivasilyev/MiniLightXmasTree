from utime import sleep_ms
from neopixel import NeoPixel
from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20
from random import choice

pixels = NeoPixel(pin=Pin(27), n=25, bpp=3)
ds_sensor = DS18X20(OneWire(Pin(14)))
roms = ds_sensor.scan()
print('Found DS devices: ', roms)

while True:
for idx in range(pixels.n):
pixels[idx] = tuple([choice(range(256)) for _ in "rgb"])
pixels.write()
sleep_ms(100)


ds_sensor.convert_temp()
for rom in roms:
print(rom)
print(ds_sensor.read_temp(rom))

