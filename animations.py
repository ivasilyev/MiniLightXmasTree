from gc import collect
from random import choice
from utime import sleep_ms
from utils import flatten_2d_array
from color_utils import BLACK, get_color_loop
from neo_rings import NeoRings, PixelsNotReadyThrowable
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


class Animations:
    # Based on: https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
    def __init__(self, rings: NeoRings, clear: bool = True):
        self.is_enabled = True
        self._pixels = rings
        self._pixels.disable_auto_write()
        self.is_clear = clear
        self.state = dict()
        print("The animation module started")

    def stop(self):
        self.is_enabled = False
        sleep_ms(100)
        collect()
        self.is_enabled = True
        # self._pixels.blacken()  # Throws `maximum recursion depth exceeded` when in separate thread

    def get_pixels(self):
        return self._pixels

    @staticmethod
    async def _pause(ms: int):
        await asyncio.sleep_ms(ms)

    def pause(self, ms: int):
        if ms > 100:
            collect()
        asyncio.run(self._pause(ms))

    def blink_single_smooth(self, index, color, pause: int = 15, steps: int = 50):
        bg = self._pixels[index]
        _colors = get_color_loop([bg, color], steps=steps)
        for _color in _colors:
            self._pixels[index] = _color
            self._pixels.write()
            self.pause(pause)
        self._pixels[index] = bg

    def blink_single(self, index, color, pause: int = 15):
        """
        Blinks a certain LED with the given color
        """
        if not self.is_enabled:
            return
        bg = self._pixels[index]
        self._pixels[index] = color
        self._pixels.write()
        self.pause(pause)
        self._pixels[index] = bg

    def blink_all(self, colors, pause: int = 15):
        """
        Blinks the whole strip with the given colors
        """
        bg = self._pixels[0]
        for color in colors:
            if not self.is_enabled:
                return
            self._pixels.fill(bg)
            self._pixels.fill(color)
            self._pixels.write()
            self.pause(pause)

    def random_blink(self, colors, background=BLACK, pause: int = 15, smooth: bool = False,
                     steps: int = 50):
        """
        Blinks a random LED with the given colors
        """
        idx = choice(self._pixels.range)
        k = "random_blink_index"
        while idx == self.state.get(k):
            idx = choice(self._pixels.range)
        self.state[k] = idx
        for color in colors:
            if not self.is_enabled:
                return
            if smooth:
                self.blink_single_smooth(idx, color, pause, steps)
            else:
                self.blink_single(idx, color, pause)
        self._pixels[idx] = background

    def bounce(self, color, pause: int = 60):
        for i in range(4 * len(self._pixels)):
            for j in self._pixels.range:
                self._pixels[j] = color
            if (i // len(self._pixels)) % 2 == 0:
                self._pixels[i % len(self._pixels)] = BLACK
            else:
                self._pixels[len(self._pixels) - 1 - (i % len(self._pixels))] = BLACK
            self._pixels.write()
            self.pause(pause)

    def bounce2(self, colors, background=BLACK, pause: int = 20, always_lit: bool = False):
        _range = self._pixels.range + self._pixels.range[1:-1][::-1]
        for color in colors:
            for idx in _range:
                if not self.is_enabled:
                    return
                self._pixels[idx] = color
                self._pixels.write()
                if not always_lit:
                    self._pixels[idx] = background
                self.pause(pause)

    def cycle(self, color, pause: int = 25):
        for i in range(4 * len(self._pixels)):
            for j in self._pixels.range:
                self._pixels[j] = BLACK
            self._pixels[i % len(self._pixels)] = color
            self._pixels.write()
            self.pause(pause)

    def cycle2(self, colors, background=BLACK, reverse: bool = False, pause: int = 20,
               always_lit: bool = False):
        if not reverse:
            _range = self._pixels.range
        else:
            _range = self._pixels.range[::-1]
        for color in colors:
            for idx in _range:
                if not self.is_enabled:
                    return
                self._pixels[idx] = color
                self._pixels.write()
                if not always_lit:
                    self._pixels[idx] = background
                self.pause(pause)

    def centrifugal(self, colors, reverse: bool = False, pause: int = 20):
        if reverse:
            _range = self._pixels.rings.copy()[::-1]
        else:
            _range = self._pixels.rings.copy()
        for color in colors:
            for ring_range in _range:
                if not self.is_enabled:
                    return
                self._pixels.fill(color, ring_range)
            self._pixels.write()
            self.pause(pause)

    def pulse(self, colors, pause: int = 20, steps: int = 50):
        bg = self._pixels[0]
        _colors = get_color_loop(flatten_2d_array([[bg, i] for i in colors]), steps=steps)
        for color in _colors:
            if not self.is_enabled:
                return
            self._pixels.fill(color)
            self._pixels.write()
            self.pause(pause)

    def fade(self):
        for i in range(0, 4 * 256, 8):
            for j in self._pixels.range:
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                self._pixels[j] = (val, 0, 0)
            self._pixels.write()

    def fade2(self, color, period: int = 500):
        brightest = max(color)
        darken_speed = brightest // period
        while period > 0 and sum(color) > 0:
            color = [i - 1 if i > 0 else 0 for i in color]
            self._pixels.fill(color)
            self._pixels.write()
            period -= 1

    def _clear(self):
        if self.is_clear:
            self._pixels.blacken()

    def animate(self, func, *args, **kwargs):
        self._clear()
        try:
            while True:
                func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            self._pixels.blacken()

