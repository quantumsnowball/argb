import time
from subprocess import DEVNULL, Popen
from typing import Self

from openrgb import OpenRGBClient
from openrgb.orgb import Device
from openrgb.utils import DeviceType

from argb.utils import PORT


class Session:
    def __init__(
        self,
        port: int = PORT,
    ) -> None:
        self._port = port
        self._server: Popen | None = None
        self._client: OpenRGBClient | None = None

    @property
    def server(self) -> Popen:
        assert self._server is not None
        return self._server

    @property
    def client(self) -> OpenRGBClient:
        assert self._client is not None
        return self._client

    @property
    def motherboard(self) -> Device:
        try:
            return next(dev for dev in self.client.devices if dev.type == DeviceType.MOTHERBOARD)
        except StopIteration:
            raise RuntimeError("No motherboard device found")

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.stop()

    def start(self) -> None:
        self._server = Popen(
            ['openrgb', '--server', f'--server-port', str(self._port)],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        for _ in range(10):
            try:
                self._client = OpenRGBClient(port=self._port)
                break
            except TimeoutError:
                time.sleep(1)
                continue
        else:
            raise TimeoutError

    def stop(self) -> None:
        if self._client is not None:
            self._client.disconnect()
        if self._server is not None:
            self._server.terminate()


class OpenRGB:
    def __init__(
        self,
        mode: str | None,
        speed: int | None,
        brightness: int | None,
        color: str | None,
    ) -> None:
        self._args = ['openrgb', ]
        if mode is not None:
            self._args += ['-m', str(mode)]
        if speed is not None:
            self._args += ['-s', str(speed)]
        if brightness is not None:
            self._args += ['-b', str(brightness)]
        if color is not None:
            self._args += ['-c', str(color)]
        self._proc: Popen | None = None

    def __enter__(self) -> Self:
        self._proc = Popen(self._args, stdout=DEVNULL, stderr=DEVNULL)
        self._proc.wait()
        return self

    def __exit__(self, type, value, traceback) -> None:
        if self._proc is not None:
            self._proc.terminate()
