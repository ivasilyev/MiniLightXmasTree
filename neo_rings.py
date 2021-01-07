from gc import collect
from machine import Pin
from utime import sleep_ms
from neopixel import NeoPixel
from color_utils import BLACK, get_random_color, validate_color


class PixelsNotReadyThrowable(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class NeoRings(NeoPixel):
    def __init__(self, pin_number: int, pixel_count: int, brightness: float = 1.,
                 auto_write: bool = False):
        # View the super class source:
        # https://github.com/micropython/micropython/blob/master/ports/esp32/modules/neopixel.py
        super().__init__(pin=Pin(pin_number), n=pixel_count, bpp=3)
        self.PIN_NUMBER = pin_number
        self.PIXEL_COUNT = pixel_count
        self.range = sorted(list(range(self.PIXEL_COUNT)))
        self._range_backup = self.range.copy()
        self.is_enabled = True
        self.brightness = brightness
        self._auto_write = auto_write
        self._validate_args()
        self.reset()

    def get_pixels(self):
        return {k: self.__getitem__(k) for k in self.range}

    def _validate_args(self):
        if self.brightness > 1.:
            raise ValueError("The brightness coefficient cannot be greater than 1!")

    def disable_auto_write(self):
        self._auto_write = False

    def write(self):
        if not self.is_enabled:
            raise PixelsNotReadyThrowable
        super().write()

    def _apply(self):
        if self._auto_write:
            self.write()

    def _get_color(self, color):
        if color == "random":
            color = get_random_color()
        return validate_color([round(i * self.brightness) for i in color])

    def __setitem__(self, index, color):
        super().__setitem__(index, self._get_color(color))
        self._apply()

    def __len__(self):
        return self.PIXEL_COUNT

    def __repr__(self):
        return "NeoRings object with {} pixels on pin {}".format(self.PIXEL_COUNT, self.PIN_NUMBER)

    def fill(self, color, range_=()):
        if len(range_) == 0:
            range_ = self.range
        for idx in range_:
            if not self.is_enabled:
                return
            self[idx] = color
        self._apply()

    def blacken(self):
        # An ultimate directive
        super().fill(BLACK)
        super().write()

    def reset(self, pause: int = 100):
        self.is_enabled = False
        sleep_ms(pause)  # Otherwise the translator does not even notice that
        self.is_enabled = True
        self.blacken()
        collect()

    def fill_except(self, color, index: int):
        if index > len(self):
            return
        range_ = self.range.copy()
        range_.pop(index)
        self.fill(color, range_)
        self._apply()

    def flip_order(self):
        self.range = self.range[::-1]
        collect()

    def loop_order(self):
        self.range = self.range + self.range[1:-1][::-1]
        collect()

    def restore_order(self):
        self.range = self._range_backup.copy()
        collect()

