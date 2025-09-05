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
