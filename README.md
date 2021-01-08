# Installation requirements for ESP32-WROVER

## Install `esptool`

```shell script
curl -fsSL https://github.com/espressif/esptool/archive/v3.0.zip -o esptool.zip
unzip esptool.zip
rm esptool.zip
cd esptool-3.0
python3 setup.py install

# Try to upgrade esptool & necessary tools
pip install --upgrade esptool docopt adafruit-ampy
```

## Erase the ESP32 factory firmware

```shell script
python esptool.py --port COM5 erase_flash
```

## Get & flash the ESP32 SPIRAM v4.x MicroPython firmware

```shell script
python esptool.py --port COM5 --baud 115200 erase_flash
curl -fsSL "https://micropython.org/resources/firmware/esp32spiram-idf4-20200902-v1.13.bin" -o "../micropython-esp32spiram-idf4.bin"
python esptool.py --chip esp32 --port COM5 --baud 115200 write_flash --flash_size=detect -z 0x1000 ../micropython-esp32spiram-idf4.bin
```

# Connect to ESP32 Test the MicroPython REPL

```python
import gc
import micropython

gc.collect()
gc.mem_free()
micropython.mem_info()
```
```text
4076560

stack: 720 out of 15360
GC: total: 4098240, used: 21776, free: 4076464
 No. of 1-blocks: 351, 2-blocks: 117, max blk sz: 41, max free sz: 254068
```
