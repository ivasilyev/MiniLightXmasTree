import math
from random import choice

BLACK = (0, ) * 3
WHITE = (255, ) * 3
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def get_random_color():
    return tuple([choice(range(256)) for _ in "rgb"])


def validate_color(color):
    return [k if k < 256 else 255 for k in [j if j > 0 else 0 for j in [int(round(i)) for i in color]]]


def adjust_brightness(color, brightness: float):
    return validate_color([float(i) * brightness for i in color])


def count_linspace(start, stop, steps: int = 10):
    if steps <= 2:
        return [start, stop]
    start = float(start)
    stop = float(stop)
    delta = stop - start
    step = delta / (steps - 1)
    out = [start, ]
    for ex in range(1, steps - 1):
        out.append(round(start + (ex * step), 2))
    out.append(stop)
    return out


def get_linear_transitions(start_color, stop_color, steps: int = 10):
    linspaces = [count_linspace(i, j, steps) for i, j in zip(start_color, stop_color)]
    return [tuple([i[j] for i in linspaces]) for j in range(steps)]


def count_sines(start, stop, steps: int = 10):
    coefficients = [(1 + math.cos(i / 100)) / 2
                    for i in count_linspace(0, round(math.pi * 100), steps)]
    return [round(start * i + stop * (1 - i)) for i in coefficients]


def get_sine_transitions(start_color, stop_color, steps: int = 10):
    linspaces = [count_sines(i, j, steps) for i, j in zip(start_color, stop_color)]
    return [tuple([i[j] for i in linspaces]) for j in range(steps)]


def get_color_loop(color_2d_array, steps: int = 10):
    out = []
    previous = None
    for color in color_2d_array:
        if previous:
            out.extend(get_sine_transitions(previous, color, steps)[:-1])
        previous = color
    out.extend(get_sine_transitions(color_2d_array[-1], color_2d_array[0], steps))
    return out


def convert_hex_to_rgb(s: str):
    try:
        return tuple(int(s.strip("#")[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        print("Failed converting HEX to RGB:", s)
        raise


def convert_rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)
