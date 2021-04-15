from gc import collect
from utils import hard_reset
from sensor_controller import SensorController
from animation_controller import AnimationController

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

try:
    import usocket as socket
except ImportError:
    import socket


class WebServer:
    HOST = "0.0.0.0"
    PORT = 80
    TYPE_HTML = "text/html; charset=utf-8"
    BUFFER_SIZE = 1024

    def __init__(self, sensor_ctrl: SensorController, animation_ctrl: AnimationController):
        self._controller_sensor = sensor_ctrl
        self._controller_animation = animation_ctrl

        self.is_enabled = False
        self._animation_params = ""
        self.addr = socket.getaddrinfo(self.HOST, self.PORT)[0][-1]
        self.socket = None
        self.state = dict()

        asyncio.run(self.start())

    async def start(self):
        self.is_enabled = True
        print("Start the web server")
        try:
            self.socket = socket.socket()
            self.socket.bind(self.addr)
        except OSError as e:
            if e.args[0] == 98:  # EADDRINUSE
                print("A socket is still opened, restarting...")
                hard_reset()
        self.socket.settimeout(2)
        self.socket.listen(5)
        self.socket.setblocking(False)
        await asyncio.sleep_ms(100)
        print("The HTTP server is listening on: {}".format(self.addr))

    async def stop(self):
        if self.is_enabled:
            self.is_enabled = False
            print("Stop the web server")
            self.socket.close()
            await asyncio.sleep_ms(100)

    async def restart(self):
        await self.stop()
        await self.start()
