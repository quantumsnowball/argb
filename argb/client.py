import time
from subprocess import DEVNULL, Popen

from openrgb import OpenRGBClient

from argb.utils import PORT


class Client:
    def __init__(
        self,
        port: int = PORT,
    ) -> None:
        self._proc: Popen | None = None
        self._client: OpenRGBClient | None = None
        self._port = port

    def __enter__(self) -> OpenRGBClient:
        self._proc = Popen(
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

        return self._client

    def __exit__(self, type, value, traceback) -> None:
        if self._proc is not None:
            self._proc.terminate()
