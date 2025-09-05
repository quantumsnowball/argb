import time

import click
import psutil
import pynvml
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

from argb.utils import PORT


@click.command
def monitor() -> None:
    # Connect to OpenRGB
    client = OpenRGBClient(port=PORT)
    device = client.devices[0]

    # Force Static mode
    device.set_mode("Static")

    # Pick Zone
    cpu_zone = device.zones[1]
    gpu_zone = device.zones[3]
    vram_zone = device.zones[2]

    # Simple usage → color mapping: green = idle, red = full load
    def usage_to_color(usage: float):
        r = int((usage / 100) * 255)
        g = int(255 - (usage / 100) * 255)
        b = 0
        return RGBColor(r, g, b)

    # Warm up measurement
    psutil.cpu_percent(interval=None)
    pynvml.nvmlInit()

    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    while True:
        try:
            cpu_usage = psutil.cpu_percent()
            cpu_zone.set_color(usage_to_color(cpu_usage))
            gpu_util = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle)
            gpu_usage = gpu_util.gpu
            gpu_zone.set_color(usage_to_color(float(gpu_usage)))
            vram_info = pynvml.nvmlDeviceGetMemoryInfo(gpu_handle)
            vram_usage = float(vram_info.used) / float(vram_info.total) * 100
            vram_zone.set_color(usage_to_color(float(vram_usage)))
            time.sleep(0.2)
        except KeyboardInterrupt:
            cpu_zone.set_color(RGBColor(255, 255, 255))
            gpu_zone.set_color(RGBColor(255, 255, 255))
            vram_zone.set_color(RGBColor(255, 255, 255))
            pynvml.nvmlShutdown()
            break
