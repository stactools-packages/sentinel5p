import pystac
from pystac import ProviderRole
from pystac.link import Link

INSPIRE_METADATA_ASSET_KEY = "inspire-metadata"
SAFE_MANIFEST_ASSET_KEY = "safe-manifest"
PRODUCT_METADATA_ASSET_KEY = "product-metadata"

SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/" +
    "247904/690755/Sentinel_Data_Legal_Notice",
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

SAFE_MANIFEST_ASSET_KEY = "safe-manifest"

INTERNATIONAL_DESIGNATOR = "2017-064A"

SENTINEL_TROPOMI_BANDS = {
    "Band 1": {
        "name": "Band 1",
        "spectrometer": "UV",
        "performance range": "270-320",
        "spectral range": "267-300",
        "spectral resoluton": "0.45-0.5",
        "slit width": 560,
        "spectral dispersion": 0.065,
        "spectral magnification": 0.327
    },
    "Band 2": {
        "name": "Band 2",
        "spectrometer": "UV",
        "performance range": "270-320",
        "spectral range": "300-332",
        "spectral resoluton": "0.45-0.5",
        "slit width": 560,
        "spectral dispersion": 0.065,
        "spectral magnification": 0.329
    },
    "Band 3": {
        "name": "Band 3",
        "spectrometer": "UVIS",
        "performance range": "320-490",
        "spectral range": "305-400",
        "spectral resoluton": "0.45-0.65",
        "slit width": 280,
        "spectral dispersion": 0.195,
        "spectral magnification": 0.231
    },
    "Band 4": {
        "name": "Band 4",
        "spectrometer": "UVIS",
        "performance range": "320-490",
        "spectral range": "400-499",
        "spectral resoluton": "0.45-0.65",
        "slit width": 280,
        "spectral dispersion": 0.195,
        "spectral magnification": 0.231
    },
    "Band 5": {
        "name": "Band 5",
        "spectrometer": "NIR",
        "performance range": "710-775",
        "spectral range": "661-725",
        "spectral resoluton": "0.34-0.35",
        "slit width": 280,
        "spectral dispersion": 0.126,
        "spectral magnification": 0.263
    },
    "Band 6": {
        "name": "Band 6",
        "spectrometer": "NIR",
        "performance range": "710-775",
        "spectral range": "725-786",
        "spectral resoluton": "0.34-0.35",
        "slit width": 280,
        "spectral dispersion": 0.126,
        "spectral magnification": 0.263
    },
    "Band 7": {
        "name": "Band 7",
        "spectrometer": "SWIR",
        "performance range": "2305-2385",
        "spectral range": "2300-2343",
        "spectral resoluton": 0.227,
        "slit width": 308,
        "spectral dispersion": 0.094,
        "spectral magnification": 0.025
    },
    "Band 8": {
        "name": "Band 8",
        "spectrometer": "SWIR",
        "performance range": "2305-2385",
        "spectral range": "2343-2389",
        "spectral resoluton": 0.225,
        "slit width": 308,
        "spectral dispersion": 0.094,
        "spectral magnification": 0.021
    }
}
