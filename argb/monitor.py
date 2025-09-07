import signal
import threading
import time
import types
from typing import Self

import click
import psutil
import pynvml
from openrgb.utils import RGBColor

from argb.session import Session


class Monitor:
    def __init__(self, session: Session) -> None:
        self._device = session.motherboard
        self._stop_event = threading.Event()

        def on_sigint(_signum: int, _frame: types.FrameType | None) -> None:
            self._stop_event.set()
        signal.signal(signal.SIGINT, on_sigint)

    def __enter__(self) -> Self:
        pynvml.nvmlInit()
        self._device.set_mode('Static')
        return self

    def __exit__(self, type, value, traceback) -> None:
        self._device.set_mode('Color shift')
        pynvml.nvmlShutdown()

    def run(self) -> None:
        # Simple usage → color mapping: green = idle, red = full load
        def usage_to_color(usage: float, *, floor: float = 0.0, ceiling: float = 100.0):
            # Normalize ratio
            ratio = (usage - floor) / (ceiling - floor)
            ratio = max(0.0, min(1.0, ratio))
            # calc color
            r = int(ratio * 255)
            g = int(255 - ratio * 255)
            b = 0
            return RGBColor(r, g, b)

        cpu_zone = self._device.zones[1]
        gpu_zone = self._device.zones[3]
        vram_zone = self._device.zones[2]
        gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        while not self._stop_event.is_set():
            # cpu
            cpu_usage = psutil.cpu_percent()
            cpu_zone.set_color(usage_to_color(cpu_usage))
            # gpu
            gpu_util = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle)
            gpu_usage = gpu_util.gpu
            gpu_zone.set_color(usage_to_color(float(gpu_usage), ceiling=70))
            # vram
            vram_info = pynvml.nvmlDeviceGetMemoryInfo(gpu_handle)
            vram_usage = float(vram_info.used) / float(vram_info.total) * 100
            vram_zone.set_color(usage_to_color(float(vram_usage)))
            #
            time.sleep(0.2)


@click.command
def monitor() -> None:
    with (
        Session() as session,
        Monitor(session) as monitor,
    ):
        monitor.run()
