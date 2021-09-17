import logging

import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sat import SatExtension

from .constants import SENTINEL_CONSTELLATION, SENTINEL_PROVIDER
from .metadata_links import MetadataLinks
from .product_metadata import ProductMetadata
from .properties import fill_proj_properties, fill_sat_properties

logger = logging.getLogger(__name__)


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

    # ---- Add Extensions ----
    # sat
    sat = SatExtension.ext(item, add_if_missing=True)
    fill_sat_properties(sat, file_path)

    # eo
    EOExtension.ext(item, add_if_missing=True)

    # proj
    proj = ProjectionExtension.ext(item, add_if_missing=True)
    fill_proj_properties(proj, file_path)

    # s5p product properties
    item.properties.update({**product_metadata.metadata_dict})

    # --Common metadata--
    item.common_metadata.providers = [SENTINEL_PROVIDER]
    item.common_metadata.platform = product_metadata.platform
    item.common_metadata.constellation = SENTINEL_CONSTELLATION

    # Add assets to item
    item.add_asset(*metalinks.create_manifest_asset())

    # objects for bands
    file_to_check = ["_CLOUD_", "_HCHO_", "_O3__", "O3_TCL", "SO2"]
    if any(_str in file_path.split("/")[-1] for _str in file_to_check):
        pass
    else:
        item.add_asset(*metalinks.create_band_asset())

    return item
