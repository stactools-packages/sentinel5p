import logging

import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sat import SatExtension

from .product_metadata import ProductMetadata
from .properties import fill_sat_properties, fill_proj_properties

logger = logging.getLogger(__name__)

def create_item(file_path: str) -> pystac.Item:
    """Create a STC Item from a Sentinel-5P scene.

    Args:
        file_path (str): The path to a Sentinel-5P netCDF4 file.

    Returns:
        pystac.Item: An item representing the Sentinel-5P scene.
    """

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

    return item
