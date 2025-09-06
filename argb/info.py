import click

from argb.session import Session


@click.command
def info() -> None:
    with Session() as session:
        for i, device in enumerate(session.client.devices):
            click.secho(f'{i}: {device.name} type={device.type}:', fg='yellow')
            for j, zone in enumerate(device.zones):
                click.secho(f'  {j}: {zone.name:>10s} type={zone.type} LEDs={len(zone.leds)}', fg='green')
