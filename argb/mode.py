import click
from openrgb.utils import DeviceType

from argb.client import Client


@click.command
@click.argument('mode', required=True, type=str)
def mode(mode: str) -> None:
    with Client() as client:
        client.clear()
        device = client.get_devices_by_type(DeviceType.MOTHERBOARD)[0]
        for char in ('-', '_'):
            mode = mode.replace(char, ' ')
        try:
            device.set_mode(mode, save=True)
            d = device.modes[device.active_mode]
            click.secho(f'Set device mode to {d.id}: {d.name}\n{d}', fg='green')
        except ValueError as e:
            click.secho(e, fg='red')

        # device.modes[device.active_mode].speed = 255
