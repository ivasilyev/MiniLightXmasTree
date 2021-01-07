from gc import collect
from utime import sleep_ms
from animations import Animations
from neo_rings import PixelsNotReadyThrowable


class AnimationController:
    def __init__(self, animations: Animations):
        self.is_running = False
        self._animations = animations
        self._pixels = self._animations.get_pixels()
        self._current_animation = None
        self._current_animation_args = ()
        self._current_animation_kwargs = dict()
        print("The animation controller module started")

    def restart(self):
        pause = 100
        pause_ = self._current_animation_kwargs.get("pause")
        if pause_ is not None and pause_ > pause:
            pause = pause_
        try:
            self._pixels.reset(pause)
        except PixelsNotReadyThrowable:
            pass
        except Exception as e:
            print("Animation restart problem:", e)
        sleep_ms(pause)

    def set_animation(self, animation_name: str, *args, **kwargs):
        if animation_name not in dir(self._animations):
            print("No such animation:", animation_name)
            return
        args_string = ", ".join(str(i) for i in [animation_name, args, kwargs])
        if args_string == self._animations.state.get("current_animation_args"):
            print("The animation parameters were already set")
            return
        print("Change animation to:", animation_name, args, kwargs)
        self._animations.state["current_animation_args"] = args_string
        if "brightness" in kwargs:
            self._pixels.brightness = kwargs["brightness"]
            del kwargs["brightness"]
        self.is_running = True
        self._current_animation = animation_name
        self._current_animation_args = args
        self._current_animation_kwargs = kwargs
        self._animations.stop()
        self.restart()

    def run(self):
        while True:
            while not self._current_animation or not self.is_running:
                sleep_ms(100)
            try:
                getattr(self._animations, self._current_animation)(
                    *self._current_animation_args, **self._current_animation_kwargs)
            except PixelsNotReadyThrowable:
                collect()
            except Exception as e:
                print("Caught general exception in AnimationController:", e)
                sleep_ms(100)
                collect()
