import click


@click.command
@click.argument('mode', required=True, type=str)
def mode(mode: str) -> None:
    print(f'Gonna change openrgb mode to {mode} ...')
