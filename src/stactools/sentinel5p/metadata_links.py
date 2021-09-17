import netCDF4 as nc  # type: ignore
import pystac

from .constants import SAFE_MANIFEST_ASSET_KEY, SENTINEL_TROPOMI_BANDS


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
        asset = pystac.Asset(href=self.file_path,
                             media_type="application/nc",
                             roles=["metadata"],
                             extra_fields={"band_fields": band_dict_list})
        return ("eo:bands", asset)
