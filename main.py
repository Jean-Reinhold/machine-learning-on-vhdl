import click
import logging
import config
from ml_to_vhdl.mlp.cli import mlp_cli

logger = logging.getLogger(__name__)


@click.group()
def main():
    logger.debug("Entered main CLI group.")


main.add_command(mlp_cli, "mlp")

if __name__ == "__main__":
    main()
