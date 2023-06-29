import re

import pystac
import shapely.geometry
from pystac import ProviderRole
from pystac.link import Link

INSPIRE_METADATA_ASSET_KEY = "inspire-metadata"
SAFE_MANIFEST_ASSET_KEY = "safe-manifest"
PRODUCT_METADATA_ASSET_KEY = "product-metadata"

SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/"
    + "247904/690755/Sentinel_Data_Legal_Notice",
)

SENTINEL_CONSTELLATION = "Sentinel-5P"

SENTINEL_INSTRUMENTS = ["TROPOMI"]

SENTINEL_PROVIDER = pystac.Provider(
    name="ESA",
    roles=[
        ProviderRole.PRODUCER,
        ProviderRole.PROCESSOR,
        ProviderRole.LICENSOR,
    ],
    url="https://earth.esa.int/web/guest/home",
)

INTERNATIONAL_DESIGNATOR = "2017-064A"

SENTINEL_TROPOMI_BANDS = {
    "Band 1": {
        "name": "Band 1",
        "spectrometer": "UV",
        "performance range": "270-320",
        "spectral range": "267-300",
        "spectral resolution": "0.45-0.5",
        "slit width": 560,
        "spectral dispersion": 0.065,
        "spectral magnification": 0.327,
    },
    "Band 2": {
        "name": "Band 2",
        "spectrometer": "UV",
        "performance range": "270-320",
        "spectral range": "300-332",
        "spectral resolution": "0.45-0.5",
        "slit width": 560,
        "spectral dispersion": 0.065,
        "spectral magnification": 0.329,
    },
    "Band 3": {
        "name": "Band 3",
        "spectrometer": "UVIS",
        "performance range": "320-490",
        "spectral range": "305-400",
        "spectral resolution": "0.45-0.65",
        "slit width": 280,
        "spectral dispersion": 0.195,
        "spectral magnification": 0.231,
    },
    "Band 4": {
        "name": "Band 4",
        "spectrometer": "UVIS",
        "performance range": "320-490",
        "spectral range": "400-499",
        "spectral resolution": "0.45-0.65",
        "slit width": 280,
        "spectral dispersion": 0.195,
        "spectral magnification": 0.231,
    },
    "Band 5": {
        "name": "Band 5",
        "spectrometer": "NIR",
        "performance range": "710-775",
        "spectral range": "661-725",
        "spectral resolution": "0.34-0.35",
        "slit width": 280,
        "spectral dispersion": 0.126,
        "spectral magnification": 0.263,
    },
    "Band 6": {
        "name": "Band 6",
        "spectrometer": "NIR",
        "performance range": "710-775",
        "spectral range": "725-786",
        "spectral resolution": "0.34-0.35",
        "slit width": 280,
        "spectral dispersion": 0.126,
        "spectral magnification": 0.263,
    },
    "Band 7": {
        "name": "Band 7",
        "spectrometer": "SWIR",
        "performance range": "2305-2385",
        "spectral range": "2300-2343",
        "spectral resolution": 0.227,
        "slit width": 308,
        "spectral dispersion": 0.094,
        "spectral magnification": 0.025,
    },
    "Band 8": {
        "name": "Band 8",
        "spectrometer": "SWIR",
        "performance range": "2305-2385",
        "spectral range": "2343-2389",
        "spectral resolution": 0.225,
        "slit width": 308,
        "spectral dispersion": 0.094,
        "spectral magnification": 0.021,
    },
}

FILENAME_EXPR = re.compile(
    r"S5P_(?P<mode>[A-Z]{4})_(?P<product_type>L(?P<level>[0-9]{1})_(?P<product>.{7}))_"
    r"(?P<start_datetime>[0-9,A-Z]{15})_(?P<end_datetime>[0-9,A-Z]{15})_"
    r"(?P<orbit>[0-9]{5})_(?P<collection>[0-9]{2})_(?P<processor_version>[0-9]{6})_"
    r"(?P<production_datetime>[0-9,A-Z]{15})"
)

ABOUT_LINKS = {
    "L2__AER_AI": "http://www.tropomi.eu/data-products/uv-aerosol-index",
    "L2__AER_LH": "http://www.tropomi.eu/data-products/aerosol-layer-height",
    "L2__CH4___": "http://www.tropomi.eu/data-products/methane",
    "L2__CLOUD_": "http://www.tropomi.eu/data-products/cloud",
    "L2__CO____": "http://www.tropomi.eu/data-products/carbon-monoxide",
    "L2__HCHO__": "http://www.tropomi.eu/data-products/formaldehyde",
    "L2__NO2___": "http://www.tropomi.eu/data-products/nitrogen-dioxide",
    "L2__O3____": "http://www.tropomi.eu/data-products/total-ozone-column",
    "L2__O3_TCL": "http://www.tropomi.eu/data-products/tropospheric-ozone-column",
    "L2__SO2___": "http://www.tropomi.eu/data-products/sulphur-dioxide",
    "L2__NP_BD3": "https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-5p/products-algorithms",  # noqa
    "L2__NP_BD6": "https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-5p/products-algorithms",  # noqa
    "L2__NP_BD7": "https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-5p/products-algorithms",  # noqa
}

ASSET_TITLES = {
    "L2__AER_AI": "Ultraviolet Aerosol Index",
    "L2__AER_LH": "Aerosol Layer Height",
    "L2__CH4___": "Methane Total Column",
    "L2__CLOUD_": "Cloud Fraction, Albedo, and Top Pressure",
    "L2__CO____": "Carbon Monoxide Total Column",
    "L2__HCHO__": "Formaldehyde Total Column",
    "L2__NO2___": "Nitrogen Dioxide Total Column",
    "L2__O3____": "Ozone Total Column",
    "L2__O3_TCL": "Ozone Tropospheric Column",
    "L2__SO2___": "Sulphur Dioxide Total Column",
    "L2__NP_BD3": "VIIRS/NPP Band 3 Cloud Mask",
    "L2__NP_BD6": "VIIRS/NPP Band 6 Cloud Mask",
    "L2__NP_BD7": "VIIRS/NPP Band 7 Cloud Mask",
}

O3_TCL_GEOMETRY = shapely.geometry.mapping(
    shapely.geometry.Polygon(
        [(-180, -19.75), (180, -19.75), (180, 19.75), (-180, 19.75)]
    )
)
O3_TCL_BBOX = [-180, -19.75, 180, 19.75]
