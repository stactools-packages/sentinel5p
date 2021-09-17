import logging
import os

import click

from stactools.sentinel5p.stac import create_item

logger = logging.getLogger(__name__)


def create_sentinel5p_command(cli):
    """Creates the stactools-sentinel5p command line utility."""
    @cli.group(
        "sentinel5p",
        short_help=("Commands for working with stactools-sentinel5p"),
    )
    def sentinel5p():
        pass

    @sentinel5p.command(
        "create-item",
        short_help="Convert a Sentinel5p scene into a STAC item")
    @click.argument("src")
    @click.argument("dst")
    def create_item_command(src, dst):
        """Creates a STAC Item

        Args:
            src: Path to the scene
            dst: Path to the STAC Item JSON file that will be created
        """
        item = create_item(src)
        item_path = os.path.join(dst, "{}.json".format(item.id))
        item.set_self_href(item_path)
        item.save_object()

        return sentinel5p
