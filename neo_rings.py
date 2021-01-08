from gc import collect
from machine import Pin
from utime import sleep_ms
from neopixel import NeoPixel
from utils import flatten_nd_array
from color_utils import BLACK, adjust_brightness, get_random_color, mutate_color, validate_color


class PixelsNotReadyThrowable(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class NeoRings(NeoPixel):
    def __init__(self, pin_number: int, rings: tuple, brightness: float = 1.,
                 auto_write: bool = False):
        # View the super class source:
        # https://github.com/micropython/micropython/blob/master/ports/esp32/modules/neopixel.py
        self._rings = self._generate_ranges(rings)
        self.range = flatten_nd_array(self._rings)
        self._range_backup = self.range.copy()
        self.is_enabled = True
        self.brightness = brightness
        self._auto_write = auto_write
        self._validate_args()
        self._pin_number = pin_number
        super().__init__(pin=Pin(self._pin_number), n=len(self.range), bpp=3)
        self.reset()

    @staticmethod
    def _generate_ranges(rings: tuple):
        first, last = (0, 0)
        reverse = False
        out = []
        for ring_length in rings:
            last += ring_length
            out.append(tuple(sorted(list(range(first, last)), reverse=reverse)))
            first += ring_length
            reverse = not reverse
        return out

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

    def __setitem__(self, index, color):
        if color == "random":
            color = get_random_color()
        if self.brightness < 1.:
            c = adjust_brightness(color, brightness=self.brightness)
        else:
            c = validate_color(color)
        super().__setitem__(index, c)
        self._apply()

    def alter(self, index, next_color, steps: int = 10):
        for color in mutate_color(start_color=self.get_pixels()[index], stop_color=next_color,
                                  steps=steps):
            self[index] = color

    def __len__(self):
        return self.n

    def __repr__(self):
        return "NeoRings object with {} pixels on pin {}".format(len(self), self._pin_number)

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

