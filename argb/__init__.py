import click

from argb.info import info
from argb.mode import mode
from argb.monitor import monitor


@click.group()
def argb() -> None:
    pass


argb.add_command(monitor)
argb.add_command(mode)
argb.add_command(info)
