import time
from subprocess import DEVNULL, Popen
from typing import Self

from openrgb import OpenRGBClient

from argb.utils import PORT


class Client(OpenRGBClient):
    def __init__(
        self,
        port: int = PORT,
    ) -> None:
        self._proc = Popen(
            ['openrgb', '--server', f'--server-port', str(port)],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        for _ in range(10):
            try:
                super().__init__(port=port)
                break
            except TimeoutError:
                time.sleep(1)
                continue
        else:
            raise TimeoutError

    def __enter__(self) -> Self:
        return self

    def __exit__(self, type, value, traceback) -> None:
        if self._proc is not None:
            self._proc.terminate()

    def stop(self) -> None:
        self.disconnect()


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
