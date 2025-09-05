import click
from openrgb import OpenRGBClient
from openrgb.utils import DeviceType

from argb.utils import PORT


@click.command
@click.argument('mode', required=True, type=str)
def mode(mode: str) -> None:
    client = OpenRGBClient(port=PORT)
    client.clear()
    device = client.get_devices_by_type(DeviceType.MOTHERBOARD)[0]
    for char in ('-', '_'):
        mode = mode.replace(char, ' ')
    device.set_mode(mode, save=True)
    # device.modes[device.active_mode].speed = 255
