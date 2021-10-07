import json

import netCDF4 as nc  # type: ignore
import pystac

from .constants import SAFE_MANIFEST_ASSET_KEY, SENTINEL_TROPOMI_BANDS


class ManifestError(Exception):
    pass


class MetadataLinks:
    def __init__(self, file_path):
        self.file_path = file_path
        if file_path.endswith(".nc"):
            self._root = nc.Dataset(file_path)
        elif file_path.endswith(".json"):
            self._root = json.load(open(file_path))
        else:
            raise ManifestError("Source file format is not supported.")

    def create_manifest_asset(self):
        if self.file_path.endswith(".nc"):
            asset = pystac.Asset(
                href=self.file_path,
                media_type="application/x-netcdf",
                roles=["metadata"],
            )
        elif self.file_path.endswith(".json"):
            asset = pystac.Asset(
                href=self.file_path,
                media_type=pystac.MediaType.JSON,
                roles=["metadata"],
            )
        return (SAFE_MANIFEST_ASSET_KEY, asset)

    def create_band_asset(self):
        if "AER_AI" in self.file_path:
            band_dict_list = [SENTINEL_TROPOMI_BANDS["Band 3"]]
        elif "AER_LH" in self.file_path:
            band_dict_list = [SENTINEL_TROPOMI_BANDS["Band 6"]]
        elif "_CH4_" in self.file_path:
            band_dict_list = [
                SENTINEL_TROPOMI_BANDS["Band 6"],
                SENTINEL_TROPOMI_BANDS["Band 7"],
                SENTINEL_TROPOMI_BANDS["Band 8"]
            ]
        elif "_CO_" in self.file_path:
            band_dict_list = [
                SENTINEL_TROPOMI_BANDS["Band 7"],
                SENTINEL_TROPOMI_BANDS["Band 8"]
            ]
        elif "_NO2_" in self.file_path:
            band_dict_list = [SENTINEL_TROPOMI_BANDS["Band 4"]]
        elif "_BD3_" in self.file_path:
            band_dict_list = [SENTINEL_TROPOMI_BANDS["Band 3"]]
        elif "_BD6_" in self.file_path:
            band_dict_list = [SENTINEL_TROPOMI_BANDS["Band 6"]]
        elif "_BD7_" in self.file_path:
            band_dict_list = [SENTINEL_TROPOMI_BANDS["Band 7"]]
        else:
            band_dict_list = []

        file_format = self.file_path.split(".")[-1]
        asset_id = self.file_path.split('/')[-1].split(".")[0]
        if file_format == "nc":
            media_type = "application/x-netcdf"
            description = self._root.title
        elif file_format == "json":
            media_type = pystac.MediaType.JSON
            description = self._root['title']
        roles = ["data"]
        if not band_dict_list:
            asset = pystac.Asset(href=self.file_path,
                                 media_type=media_type,
                                 description=description,
                                 roles=roles)
        else:
            asset = pystac.Asset(href=self.file_path,
                                 media_type=media_type,
                                 description=description,
                                 roles=roles,
                                 extra_fields={"eo:bands": band_dict_list})
        return (asset_id, asset)
