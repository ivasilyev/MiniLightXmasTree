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
```text
esptool.py v3.0
Serial port COM5
Connecting....
Detecting chip type... ESP32
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: 10:52:1c:5e:64:48
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 3.2s
Hard resetting via RTS pin...
```
## Get & flash the ESP32 no-SPIRAM MicroPython firmware
#### ESP-IDF v3.x

```shell script
curl -fsSL https://micropython.org/resources/firmware/esp32-idf3-20200902-v1.13.bin -o ../micropython.bin
python esptool.py --port COM5 --baud 115200 erase_flash
python esptool.py --chip esp32 --port COM5 --baud 115200 write_flash --flash_size=detect -z 0x1000 ../micropython.bin
```

#### ESP-IDF v4.x

```shell script
python esptool.py --port COM5 --baud 115200 erase_flash
curl -fsSL "https://micropython.org/resources/firmware/esp32spiram-idf4-20200902-v1.13.bin" -o "../micropython-esp32spiram-idf4.bin"
python esptool.py --chip esp32 --port COM5 --baud 115200 write_flash --flash_size=detect -z 0x1000 ../micropython-esp32spiram-idf4.bin
```
import gc
import micropython

gc.collect()
gc.mem_free()
micropython.mem_info()




```text
esptool.py v3.0
Serial port COM5
Connecting....
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: 10:52:1c:5e:64:48
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Auto-detected Flash size: 4MB
Compressed 1448768 bytes to 926007...
Wrote 1448768 bytes (926007 compressed) at 0x00001000 in 21.3 seconds (effective 545.4 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```

