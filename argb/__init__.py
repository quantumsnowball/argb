import click

from argb.info import info
from argb.mode import mode
from argb.monitor import monitor


@click.group(invoke_without_command=True)
@click.pass_context
def argb(ctx: click.Context) -> None:
    # argb can be a standalone command
    if ctx.invoked_subcommand:
        return
    print('do some direct openrgb settings here')


argb.add_command(monitor)
argb.add_command(mode)
argb.add_command(info)
