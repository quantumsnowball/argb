import time

import psutil

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

# Connect to OpenRGB
client = OpenRGBClient()
device = client.devices[0]

# Force Static mode
device.set_mode("Static")

# Pick Zone 1 (CPU)
cpu_zone = device.zones[1]

# Simple usage → color mapping: green = idle, red = full load


def usage_to_color(usage):
    r = int((usage / 100) * 255)
    g = int(255 - (usage / 100) * 255)
    b = 0
    return RGBColor(r, g, b)


# Warm up CPU measurement
psutil.cpu_percent(interval=None)

while True:
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_zone.set_color(usage_to_color(cpu_usage))
        time.sleep(0.2)
    except KeyboardInterrupt:
        cpu_zone.set_color(RGBColor(255, 255, 255))
        break
