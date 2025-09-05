import click

from argb.mode import mode
from argb.monitor import monitor


@click.group()
def argb() -> None:
    pass


argb.add_command(monitor)
argb.add_command(mode)
