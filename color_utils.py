from random import choice

BLACK = (0, ) * 3
WHITE = (255, ) * 3
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def get_random_color():
    return tuple([choice(range(256)) for _ in "rgb"])


def validate_color(color):
    return [k if k < 256 else 255 for k in [j if j > 0 else 0 for j in [round(i) for i in color]]]


def adjust_brightness(color, brightness: float):
    return validate_color([float(i) * brightness for i in color])


def count_linspace(start, stop, count: int = 10):
    if count <= 2:
        return [start, stop]
    start = float(start)
    stop = float(stop)
    delta = stop - start
    step = delta / (count - 1)
    out = [start, ]
    for ex in range(1, count - 1):
        out.append(round(start + (ex * step), 2))
    out.append(stop)
    return out


def mutate_color(start_color, stop_color, steps: int = 10):
    linspaces = [count_linspace(i, j, steps) for i, j in zip(start_color, stop_color)]
    return [tuple([i[j] for i in linspaces]) for j in range(steps)]


def create_color_loop(color_2d_array, steps: int = 10):
    out = []
    previous = None
    for color in color_2d_array:
        if previous:
            out.extend(mutate_color(previous, color, steps)[:-1])
        previous = color
    out.extend(mutate_color(color_2d_array[-1], color_2d_array[0], steps))
    return out


def convert_hex_to_rgb(s: str):
    try:
        return tuple(int(s.strip("#")[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        print("Failed converting HEX to RGB:", s)
        raise


def convert_rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)
