import pystac
import netCDF4 as nc

from .constants import (SAFE_MANIFEST_ASSET_KEY)

class ManifestError(Exception):
    pass

class MetadataLinks:
    def __init__(self, file_path):
        self.file_path = file_path
        self._root = nc.Dataset(file_path)

    def create_manifest_asset(self):
        asset = pystac.Asset(
            href=self.file_path,
            media_type="application/nc",
            roles=["metadata"],
        )
        return (SAFE_MANIFEST_ASSET_KEY, asset)