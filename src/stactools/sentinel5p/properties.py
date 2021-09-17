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

    root = nc.Dataset(href)
    sat_ext.platform_international_designator = INTERNATIONAL_DESIGNATOR

    if "O3_TCL" in href:
        pass
    else:
        sat_ext.absolute_orbit = int(root.orbit)


def fill_proj_properties(proj_ext, href):
    """Fills the properties for PROJ.
    Based on the proj Extension.py
    Args:
        proj_ext (pystac.extensions.projection.ProjectionExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an netCDF4 file.
    Returns:
        pystac.Asset: An asset with the PROJECTION relevant properties.
    """

    root = nc.Dataset(href)
    product = root['METADATA/GRANULE_DESCRIPTION'].getncattr(
        'ProductShortName')
    BDx = [f"BD{num}" for num in range(1, 9)]
    if any(_str in product for _str in BDx):
        path_to_dimensions = f"BAND{product[-1]}_NPPC/STANDARD_MODE"
    else:
        path_to_dimensions = "PRODUCT"
    proj_ext.epsg = 4326
    if "O3_TCL" in href:
        proj_ext.shape = [
            root[path_to_dimensions].dimensions['latitude_ccd'].size,
            root[path_to_dimensions].dimensions['longitude_ccd'].size
        ]
    else:
        proj_ext.shape = [
            root[path_to_dimensions].dimensions['scanline'].size,
            root[path_to_dimensions].dimensions['ground_pixel'].size
        ]
