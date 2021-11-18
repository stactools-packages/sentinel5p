import json  # type: ignore

import netCDF4 as nc  # type: ignore

from .constants import INTERNATIONAL_DESIGNATOR


def fill_sat_properties(sat_ext, href):
    """Fills the properties for SAR.
    Based on the sat Extension.py
    Args:
        sat_ext (pystac.extensions.sat.SatExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an netCDF4 file.
    Returns:
        pystac.Asset: An asset with the SAT relevant properties.
    """

    if href.endswith('.nc'):
        root = nc.Dataset(href)
    elif href.endswith('.json'):
        root = json.load(open(href))

    sat_ext.platform_international_designator = INTERNATIONAL_DESIGNATOR

    if "O3_TCL" in href:
        pass
    else:
        if href.endswith('.nc'):
            sat_ext.absolute_orbit = int(root.orbit)
        elif href.endswith('.json'):
            sat_ext.absolute_orbit = int(root['orbit'])
