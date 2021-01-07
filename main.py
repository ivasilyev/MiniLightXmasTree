import _thread
from neo_rings import NeoRings
from animations import Animations
from sensor_controller import SensorController
from animation_controller import AnimationController


def main():
    pixels = NeoRings(pin_number=27, pixel_count=16, brightness=1., auto_write=False)

    animations = Animations(pixels)
    animation_controller = AnimationController(animations)
    _thread.start_new_thread(animation_controller.run, ())

    sensor_controller = SensorController(pin=14, pause=1)
    _thread.start_new_thread(sensor_controller.run, ())
