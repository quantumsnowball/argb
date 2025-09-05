import click
from openrgb import OpenRGBClient

from argb.utils import PORT


@click.command
def info() -> None:
    client = OpenRGBClient(port=PORT)
    for i, device in enumerate(client.devices):
        click.secho(f'{i}: {device.name} type={device.type}:', fg='yellow')
        for j, zone in enumerate(device.zones):
            click.secho(f'  {j}: {zone.name:>10s} type={zone.type} LEDs={len(zone.leds)}', fg='green')
