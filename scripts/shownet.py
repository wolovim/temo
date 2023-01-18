import click
from ape.cli import network_option, NetworkBoundCommand


@click.command(cls=NetworkBoundCommand)
@network_option()
def cli(network):
    click.echo(f"You are connected to network '{network}'.")
