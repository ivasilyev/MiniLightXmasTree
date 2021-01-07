
def flatten(x):
    for item in x:
        try:
            yield from flatten(item)
        except TypeError:
            yield item


def flatten_nd_array(arr):
    return list(flatten(arr))


def load_string(file: str):
    with open(file=file, mode="r", encoding="utf-8") as f:
        s = f.read()
        f.close()
    return s


def read_json(file: str):
    from json import load
    with open(file=file, mode="r", encoding="utf-8") as f:
        out = load(f)
        f.close()
    return out


def wlan_connect(wlan_essid, wlan_password, hostname: str = ""):
    from network import WLAN, STA_IF
    from utime import sleep
    nic = WLAN(STA_IF)
    if not nic.isconnected():
        print("Connecting to network: ...")
        nic.active(True)
        if len(hostname) > 0:
            nic.config(dhcp_hostname=hostname)
        nic.connect(wlan_essid, wlan_password)
        while not nic.isconnected():
            sleep(1)
    print("Network connected, the configuration: {}".format(nic.ifconfig()))


def rm(s):
    try:
        import uos as os
    except ImportError:
        import os
    try:
        _ = os.stat(s)[0]
        try:
            os.remove(s)  # A file
        except OSError:  # A folder
            for i in os.listdir(s):
                s_ = "{}/{}".format(s, i)
                rm(s_)
            os.rmdir(s)
    except OSError:
        print("Not found: '{}'".format(s))


def clean_lib():
    _JUNK = ['.github', '.gitignore', '.pre-commit-config.yaml', '.pylintrc', '.readthedocs.yml',
             '@PaxHeader', 'CODE_OF_CONDUCT.md', 'LICENSES', 'LICENSE', 'docs', 'examples',
             'pyproject.toml', 'requirements.txt']
    for j in _JUNK:
        rm("/lib/{}".format(j))


def timeit(func, run_number: int = 1, *args, **kwargs):
    import utime as time
    start = time.ticks_us()
    for i in range(run_number):
        _ = func(*args, **kwargs)
    return time.ticks_diff(time.ticks_us(), start)


def soft_reset():
    # From http://docs.micropython.org/en/v1.8.6/wipy/wipy/tutorial/reset.html
    import sys
    sys.exit()


def hard_reset():
    import machine
    machine.reset()


def parse_percent_encoding(s: str):
    # See https://en.wikipedia.org/wiki/Percent-encoding
    pasted_1 = """! 	# 	$ 	% 	& 	' 	( 	) 	* 	+ 	, 	/ 	: 	; 	= 	? 	@ 	[ 	]
    %21 	%23 	%24 	%25 	%26 	%27 	%28 	%29 	%2A 	%2B 	%2C 	%2F 	%3A 	%3B 	%3D 	%3F 	%40 	%5B 	%5D
    """
    pasted_2 = """" 	% 	- 	. 	< 	> 	\ 	^ 	_ 	` 	{ 	| 	} 	~ 	£ 	円
    %22 	%25 	%2D 	%2E 	%3C 	%3E 	%5C 	%5E 	%5F 	%60 	%7B 	%7C 	%7D 	%7E 	%C2%A3 	%E5%86%86
    """
    replacements = []
    for pasted in (pasted_1, pasted_2):
        chars, percents = [[l_ for l_ in [k.strip() for k in j.split(" ")] if len(l_) > 0] for j in
                           [i.strip() for i in pasted.split("\n")] if len(j) > 0]
        for char, percent in zip(chars, percents):
            replacements.append((percent, char))
    replacements.extend([(i.strip(), "\r\n") for i in "%0A or %0D or %0D%0A".split("or")])
    replacements.append(("%20", " "))
    replacements.sort(key=lambda x: len(x[0]), reverse=True)
    for replacement in replacements:
        s = s.replace(*replacement)
    return s
