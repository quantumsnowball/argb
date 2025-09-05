import time

from openrgb import OpenRGBClient
from openrgb.utils import DeviceType, RGBColor

client = OpenRGBClient(port=6742)

client.clear()  # Turns everything off

# List all detected devices
for i, d in enumerate(client.devices):
    print(i, d.name, d.type, len(d.leds), len(d.zones))


device = client.get_devices_by_type(DeviceType.MOTHERBOARD)[0]

colors = [
    RGBColor(255, 0, 0),  # red
    RGBColor(0, 255, 0),  # green
    RGBColor(0, 0, 255),  # blue
]
device.set_mode('Static')
for i, zone in enumerate(device.zones[1:]):
    print(f"Testing zone {i}: {zone.name} ({len(zone.leds)} LEDs)")
    for color in colors:
        zone.set_color(color)
        time.sleep(1)
    # Turn off after test
    zone.set_color(RGBColor(0, 0, 0))
    # time.sleep(0.5)
