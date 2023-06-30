import logging
from pathlib import Path
from typing import Any, List

import pystac
from pystac.extensions.sat import SatExtension

from .constants import (
    ABOUT_LINKS,
    ASSET_TITLES,
    FILENAME_EXPR,
    SENTINEL_CONSTELLATION,
    SENTINEL_PROVIDER,
)
from .metadata_links import MetadataLinks
from .product_metadata import ProductMetadata
from .properties import fill_sat_properties

logger = logging.getLogger(__name__)


# ---
# This module includes copious contributions ported from the Microsoft Planetary
# Computer Sentinel-5 dataset package:
# https://github.com/microsoft/planetary-computer-tasks/blob/main/datasets/sentinel-5p/


def recursive_round(coordinates: List[Any], precision: int) -> List[Any]:
    """Rounds a list of numbers. The list can contain additional nested lists
    or tuples of numbers.

    Any tuples encountered will be converted to lists.

    Args:
        coordinates (List[Any]): A list of numbers, possibly containing nested
            lists or tuples of numbers.
        precision (int): Number of decimal places to use for rounding.

    Returns:
        List[Any]: The list of numbers rounded to the given precision.
    """
    rounded: List[Any] = []
    for value in coordinates:
        if isinstance(value, (int, float)):
            rounded.append(round(value, precision))
        else:
            rounded.append(recursive_round(list(value), precision))
    return rounded


def create_item(file_path: str) -> pystac.Item:
    """Create a STC Item from a Sentinel-5P scene.

    Args:
        file_path (str): The path to a Sentinel-5P netCDF4 file.

    Returns:
        pystac.Item: An item representing the Sentinel-5P scene.
    """

    metalinks = MetadataLinks(file_path)

    product_metadata = ProductMetadata(file_path)

    item = pystac.Item(
        id=product_metadata.scene_id,
        geometry=product_metadata.get_geometry,
        bbox=product_metadata.get_bbox,
        datetime=product_metadata.get_datetime,
        properties={},
        stac_extensions=[],
    )

    s5p_naming = FILENAME_EXPR.match(Path(file_path).stem)
    if not s5p_naming:
        raise ValueError(
            "Granule name does not match Sentinel-5p naming convention(s):"
            + Path(file_path).stem
        )

    # ---- Add Extensions ----
    # sat
    sat = SatExtension.ext(item, add_if_missing=True)
    fill_sat_properties(sat, file_path)

    # s5p product properties
    item.properties.update({**product_metadata.metadata_dict})

    # --Common metadata--
    item.common_metadata.providers = [SENTINEL_PROVIDER]
    item.common_metadata.platform = product_metadata.platform
    item.common_metadata.constellation = SENTINEL_CONSTELLATION

    # product specific properties
    asset_spec_prefix = s5p_naming.group("product").strip("_").lower()
    asset_id = asset_spec_prefix.replace("_", "-")

    # special handling needed for np-bd products
    if asset_spec_prefix.startswith("np_bd"):
        asset_spec_prefix = asset_spec_prefix.replace("_", "")

    asset_spec_properties = {
        k.replace(f"{asset_spec_prefix}:", ""): v
        for k, v in item.properties.items()
        if k.startswith(asset_spec_prefix + ":")
    }
    for key in asset_spec_properties:
        del item.properties[f"{asset_spec_prefix}:{key}"]

    product_type = s5p_naming.group("product_type")
    s5p_properties = {
        "s5p:product_name": asset_id,
        "s5p:processing_mode": s5p_naming.group("mode"),
        "s5p:collection_identifier": s5p_naming.group("collection"),
        f"s5p:{asset_spec_prefix}": asset_spec_properties,
    }
    item.properties.update(s5p_properties)
    _, asset_obj, band_dict_list = metalinks.create_band_asset()
    asset_obj.title = ASSET_TITLES[product_type]
    item.add_asset(asset_id, asset_obj)

    item.links.append(
        pystac.Link(
            rel="about", target=ABOUT_LINKS[product_type], media_type="text/html"
        )
    )

    return item
