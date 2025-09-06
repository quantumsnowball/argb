import click

from argb.client import OpenRGB
from argb.info import info
from argb.mode import mode
from argb.monitor import monitor


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-m', '--mode', default=None, type=str, help='Sets the mode to be applied, check --list-devices to see which modes are supported on your device')
@click.option('-s', '--speed', default=None, type=click.IntRange(0, 100), help='Sets the speed as a percentage if the mode supports speed')
@click.option('-b', '--brightness', default=None, type=click.IntRange(0, 100), help='Sets the brightness as a percentage if the mode supports brightness')
@click.option('-c', '--color', default=None, type=str, help=(
    'Sets colors on each device directly if no effect is specified, and sets the effect color if an effect is specified. '
    'If there are more LEDs than colors given, the last color will be applied to the remaining LEDs'))
def argb(
    ctx: click.Context,
    mode: str | None,
    speed: int | None,
    brightness: int | None,
    color: str | None,
) -> None:
    # argb can be a standalone command
    if ctx.invoked_subcommand:
        return

    # preprocessing args
    if mode is not None:
        for char in ('-', '_'):
            mode = mode.replace(char, ' ')

    # openrgb cli
    with OpenRGB(mode, speed, brightness, color):
        pass


argb.add_command(monitor)
argb.add_command(mode)
argb.add_command(info)
