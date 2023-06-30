import json  # type: ignore
import re
from datetime import datetime
from typing import Any, Dict, Optional

import antimeridian
import netCDF4 as nc  # type: ignore
from pystac.utils import str_to_datetime
from shapely.geometry import Polygon, mapping  # type: ignore

from .constants import O3_TCL_GEOMETRY


class ProductMetadataError(Exception):
    pass


class ProductMetadata:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        if file_path.endswith(".nc"):
            self._root = nc.Dataset(file_path)
        elif file_path.endswith(".json"):
            self._root = json.load(open(file_path))
        else:
            raise ProductMetadataError("Source file format is not supported.")

    @property
    def scene_id(self) -> str:
        """Returns the string to be used for a STAC Item id."""
        product_id = self.product_id
        if not product_id.startswith("S5P"):
            raise ValueError(
                "Unexpected value found at "
                f"{product_id}: "
                "this was expected to follow the sentinel 5P "
                "naming convention, starting with S5P"
            )
        scene_id = self.product_id

        return scene_id

    @property
    def product_id(self) -> str:
        result = self.file_path.split("/")[-1].split(".")[0]
        if result is None:
            raise ValueError(
                "Cannot determine product ID using product metadata "
                f"at {self.file_path}"
            )
        else:
            return result

    @property
    def get_geometry(self):
        if "O3_TCL" in self.file_path:
            # # Included metadata uses incorrect extent of data, so use hardcode for now
            # if self.file_path.endswith(".nc"):
            #     latitude_ccd = self._root["/PRODUCT/latitude_ccd"][:]
            #     longitude_ccd = self._root["/PRODUCT/longitude_ccd"][:]
            # else:
            #     latitude_ccd = self._root["PRODUCT"]["latitude_ccd"][:]
            #     longitude_ccd = self._root["PRODUCT"]["longitude_ccd"][:]
            # footprint_polygon = Polygon(
            #     list(
            #         [[coord, latitude_ccd[0]] for coord in longitude_ccd]
            #         + [[longitude_ccd[-1], coord] for coord in latitude_ccd]
            #         + [[coord, latitude_ccd[-1]] for coord in longitude_ccd[::-1]]
            #         + [[longitude_ccd[0], coord] for coord in latitude_ccd[::-1]]
            #     )
            # )
            footprint_polygon = O3_TCL_GEOMETRY
        else:
            if self.file_path.endswith(".nc"):
                footprint_text = self._root[
                    "/METADATA/EOP_METADATA/"
                    "om:featureOfInterest/eop:multiExtentOf/"
                    "gml:surfaceMembers/gml:exterior"
                ].getncattr("gml:posList")
            else:
                footprint_text = self._root["METADATA"]["EOP_METADATA"][
                    "om:featureOfInterest"
                ]["eop:multiExtentOf"]["gml:surfaceMembers"]["gml:exterior"][
                    "gml:posList"
                ]
            if footprint_text is None:
                ProductMetadataError(
                    f"Cannot parse footprint from product metadata at {self.file_path}"
                )
            footprint_value = [
                float(coord) for coord in footprint_text.replace(" ", ",").split(",")
            ]
            footprint_points = [
                point[::-1] for point in list(zip(*[iter(footprint_value)] * 2))
            ]
            footprint_polygon_alpha = Polygon(footprint_points)
            footprint_polygon = antimeridian.fix_polygon(
                footprint_polygon_alpha, fix_winding=False
            )
        geometry = mapping(footprint_polygon)
        self.footprint_polygon = footprint_polygon
        return geometry

    @property
    def get_bbox(self) -> list:
        bbox = list(self.footprint_polygon.bounds)
        return bbox

    @property
    def get_datetime(self) -> datetime:
        if self.file_path.endswith(".nc"):
            start_time = self._root.time_coverage_start
            end_time = self._root.time_coverage_end
        else:
            start_time = self._root["time_coverage_start"]
            end_time = self._root["time_coverage_end"]
        format_1 = "%Y-%m-%dT%H:%M:%SZ"
        format_2 = "%Y-%m-%dT%H:%M:%S"
        if len(start_time) == 20:
            datetime_format = format_1
        elif len(start_time) == 19:
            datetime_format = format_2
        else:
            raise ValueError("Source datetime format is not supported.")
        central_time = (
            datetime.strptime(start_time, datetime_format)
            + (
                datetime.strptime(end_time, datetime_format)
                - datetime.strptime(start_time, datetime_format)
            )
            / 2
        )

        if central_time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.file_path}"
            )
        else:
            return str_to_datetime(str(central_time))

    @property
    def platform(self) -> Optional[str]:
        if "O3_TCL" in self.file_path:
            if self.file_path.endswith(".nc"):
                platform_name = str(
                    self._root["METADATA/GRANULE_DESCRIPTION"].MissionName
                )
            else:
                platform_name = str(
                    self._root["METADATA"]["GRANULE_DESCRIPTION"]["MissionName"]
                )
        else:
            if self.file_path.endswith(".nc"):
                platform_name = str(
                    self._root[
                        "METADATA/ISO_METADATA/gmi:acquisitionInformation/gmi:platform"
                    ].getncattr("gmi:description")
                )
            else:
                platform_name = str(
                    self._root["METADATA"]["ISO_METADATA"][
                        "gmi:acquisitionInformation"
                    ]["gmi:platform"]["gmi:description"]
                )
        return platform_name

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        def _get_start_datetime(product_path, product_root):
            if "O3_TCL" in product_path:
                stratosphere_start_datetime = product_root.time_coverage_start
                troposphere_start_datetime = (
                    product_root.time_coverage_troposphere_start
                )
                start_datetime = [
                    stratosphere_start_datetime,
                    troposphere_start_datetime,
                ]
            else:
                start_datetime = [product_root.time_coverage_start]
            return start_datetime

        def _observed_after_res_upgraded(observed_time):
            format_1 = "%Y-%m-%dT%H:%M:%SZ"
            format_2 = "%Y-%m-%dT%H:%M:%S"
            if len(observed_time) == 20:
                datetime_format = format_1
            elif len(observed_time) == 19:
                datetime_format = format_2
            else:
                raise ValueError("Source datetime format is not supported.")
            observed_time = datetime.strptime(observed_time, datetime_format)
            res_upgrade_time = datetime(year=2019, month=8, day=6, hour=13, minute=30)
            return observed_time > res_upgrade_time

        def _correct_resolution(resolution):
            return resolution.replace("7x", "5.5x")

        def str_res_to_list(spatial_resolution: str):
            resolution_pat = re.compile(r"^([0-9\.]+)x([0-9\.]+) *km2$")
            resolution_match = resolution_pat.match(spatial_resolution)
            if not resolution_match:
                raise ValueError(
                    f"Unexpected spatial_resolutio: '{spatial_resolution}'"
                )
            return [int(1000 * float(x)) for x in resolution_match.groups()]

        def _get_resolution(product_path, product_root, observed_after_res_upgraded):
            excludes = ["O3_TCL", "_BD3_", "_BD6_", "_BD7_"]
            if any([product in product_path for product in excludes]):
                if observed_after_res_upgraded:
                    spatial_resolution = "5.5x3.5km2"
                else:
                    spatial_resolution = "7x3.5km2"
            else:
                if observed_after_res_upgraded:
                    spatial_resolution = _correct_resolution(
                        product_root.spatial_resolution
                    )
                else:
                    spatial_resolution = product_root.spatial_resolution
            return str_res_to_list(spatial_resolution)

        def _get_start_datetime_from_json(product_path, product_root):
            if "O3_TCL" in product_path:
                stratosphere_start_datetime = product_root["time_coverage_start"] + "Z"
                troposphere_start_datetime = (
                    product_root["time_coverage_troposphere_start"] + "Z"
                )
                start_datetime = [
                    stratosphere_start_datetime,
                    troposphere_start_datetime,
                ]
            else:
                start_datetime = [product_root["time_coverage_start"]]
            return start_datetime

        def _get_resolution_from_json(
            product_path, product_root, observed_after_res_upgraded
        ):
            excludes = ["O3_TCL", "_BD3_", "_BD6_", "_BD7_"]
            if any([product in product_path for product in excludes]):
                if observed_after_res_upgraded:
                    spatial_resolution = "5.5x3.5km2"
                else:
                    spatial_resolution = "7x3.5km2"
            else:
                if observed_after_res_upgraded:
                    spatial_resolution = _correct_resolution(
                        product_root["spatial_resolution"]
                    )
                else:
                    spatial_resolution = product_root["spatial_resolution"]
            return spatial_resolution

        if self.file_path.endswith(".nc"):
            start_datetime = _get_start_datetime(self.file_path, self._root)
            observed_after_res_upgraded = _observed_after_res_upgraded(
                start_datetime[0]
            )
            spatial_resolution = _get_resolution(
                self.file_path, self._root, observed_after_res_upgraded
            )
            if "_AER_AI_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root.time_coverage_end),
                    "instruments": [str(self._root.sensor)],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"].dimensions["scanline"].size),
                        int(self._root["PRODUCT"].dimensions["ground_pixel"].size),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "aer_ai:geolocation_grid_from_band": int(
                        self._root.geolocation_grid_from_band
                    ),
                    "aer_ai:input_band": str(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.type"
                        )
                    ),
                    "aer_ai:irradiance_accompanied": str(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.irrType"
                        )
                    ),
                }
            elif "_AER_LH_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root.time_coverage_end),
                    "instruments": [str(self._root.sensor)],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"].dimensions["scanline"].size),
                        int(self._root["PRODUCT"].dimensions["ground_pixel"].size),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "aer_lh:geolocation_grid_from_band": int(
                        self._root.geolocation_grid_from_band
                    ),
                    "aer_lh:input_band": [
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.2.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.3.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.4.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.5.type"
                        ),
                    ],
                    "aer_lh:irradiance_accompanied": str(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.irrType"
                        )
                    ),
                }
            elif "_CH4_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root.time_coverage_end),
                    "instruments": [str(self._root.sensor)],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"].dimensions["scanline"].size),
                        int(self._root["PRODUCT"].dimensions["ground_pixel"].size),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "ch4:geolocation_grid_from_band": int(
                        self._root.geolocation_grid_from_band
                    ),
                    "ch4:input_band": [
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.2.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.3.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.4.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.5.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.6.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.7.type"
                        ),
                    ],
                    "ch4:irradiance_accompanied": [
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.irrType"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.3.irrType"
                        ),
                    ],
                }
            elif "_CLOUD_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0] + "Z"),
                    "end_datetime": str(self._root.time_coverage_end + "Z"),
                    "instruments": [str(self._root.sensor)],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"].dimensions["scanline"].size),
                        int(self._root["PRODUCT"].dimensions["ground_pixel"].size),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "cloud:geolocation_grid_from_band": int(
                        self._root.geolocation_grid_from_band
                    ),
                    "cloud:cloud_mode": str(self._root.cloud_mode),
                }
            elif "_CO_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root.time_coverage_end),
                    "instruments": [str(self._root.sensor)],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"].dimensions["scanline"].size),
                        int(self._root["PRODUCT"].dimensions["ground_pixel"].size),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "co:geolocation_grid_from_band": int(
                        self._root.geolocation_grid_from_band
                    ),
                    "co:input_band": [
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.2.type"
                        ),
                    ],
                    "co:irradiance_accompanied": str(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.irrType"
                        )
                    ),
                }
            elif "_HCHO_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0] + "Z"),
                    "end_datetime": str(self._root.time_coverage_end + "Z"),
                    "instruments": [str(self._root.sensor)],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"].dimensions["scanline"].size),
                        int(self._root["PRODUCT"].dimensions["ground_pixel"].size),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "hcho:geolocation_grid_from_band": int(
                        self._root.geolocation_grid_from_band
                    ),
                    "hcho:cloud_mode": str(self._root.cloud_mode),
                }
            elif "_NO2_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root.time_coverage_end),
                    "instruments": [str(self._root.sensor)],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"].dimensions["scanline"].size),
                        int(self._root["PRODUCT"].dimensions["ground_pixel"].size),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "no2:geolocation_grid_from_band": int(
                        self._root.geolocation_grid_from_band
                    ),
                    "no2:input_band": [
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.2.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.3.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.4.type"
                        ),
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.5.type"
                        ),
                    ],
                    "no2:irradiance_accompanied": str(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "input.1.irrType"
                        )
                    ),
                }
            elif "_O3__" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0] + "Z"),
                    "end_datetime": str(self._root.time_coverage_end + "Z"),
                    "instruments": [str(self._root.sensor)],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"].dimensions["scanline"].size),
                        int(self._root["PRODUCT"].dimensions["ground_pixel"].size),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "o3:geolocation_grid_from_band": int(
                        self._root.geolocation_grid_from_band
                    ),
                    "o3:cloud_mode": str(self._root.cloud_mode),
                }
            elif "O3_TCL" in self.file_path:
                result = {
                    "instruments": [
                        str(
                            self._root[
                                "METADATA/GRANULE_DESCRIPTION"
                            ].InstrumentName.upper()
                        )
                    ],
                    "s5p:processing_mode": str(self._root["METADATA"].processingMode),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:spatial_resolution": spatial_resolution,
                    "o3_tcl:shape_ccd": [
                        int(self._root["PRODUCT"].dimensions["latitude_ccd"].size),
                        int(self._root["PRODUCT"].dimensions["longitude_ccd"].size),
                    ],
                    "o3_tcl:shape_csa": [
                        int(self._root["PRODUCT"].dimensions["latitude_csa"].size),
                        int(self._root["PRODUCT"].dimensions["longitude_csa"].size),
                    ],
                    "o3_tcl:stratosphere_start_datetime": str(start_datetime[0] + "Z"),
                    "o3_tcl:stratosphere_end_datetime": str(
                        self._root.time_coverage_end + "Z"
                    ),
                    "o3_tcl:troposphere_start_datetime": str(start_datetime[1] + "Z"),
                    "o3_tcl:troposphere_end_datetime": str(
                        self._root.time_coverage_troposphere_end + "Z"
                    ),
                    "o3_tcl:input_orbits": [
                        int(num)
                        for num in self._root["METADATA"].input_orbits.split(" ")
                    ],
                    "o3_tcl:input_files": [
                        file.split("/")[-1].split(".")[0]
                        for file in self._root["METADATA"].input_files.split(" ")
                    ],
                }
            elif "_SO2_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0] + "Z"),
                    "end_datetime": str(self._root.time_coverage_end + "Z"),
                    "instruments": [str(self._root.sensor)],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"].dimensions["scanline"].size),
                        int(self._root["PRODUCT"].dimensions["ground_pixel"].size),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "so2:geolocation_grid_from_band": int(
                        self._root.geolocation_grid_from_band
                    ),
                    "so2:cloud_mode": str(self._root.cloud_mode),
                }
            elif "_BD3_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root.time_coverage_end),
                    "instruments": [
                        str(
                            self._root[
                                "METADATA/EOP_METADATA/om:procedure/eop:instrument"
                            ].getncattr("eop:shortName")
                        )
                    ],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(
                            self._root["BAND3_NPPC/STANDARD_MODE"]
                            .dimensions["scanline"]
                            .size
                        ),
                        int(
                            self._root["BAND3_NPPC/STANDARD_MODE"]
                            .dimensions["ground_pixel"]
                            .size
                        ),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "npbd3:analysed_s5p_band": int(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "S5P_Band_Number"
                        )
                    ),
                    "npbd3:VIIRS_band": [
                        int(band)
                        for band in self._root["METADATA/ALGORITHM_SETTINGS"]
                        .getncattr("VIIRS_Bands")
                        .split("; ")[:-1]
                    ],
                    "npbd3:number_of_scaled_fov": int(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "Number_of_scaled_FOV"
                        )
                    ),
                }
            elif "_BD6_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root.time_coverage_end),
                    "instruments": [
                        str(
                            self._root[
                                "METADATA/EOP_METADATA/om:procedure/eop:instrument"
                            ].getncattr("eop:shortName")
                        )
                    ],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(
                            self._root["BAND6_NPPC/STANDARD_MODE"]
                            .dimensions["scanline"]
                            .size
                        ),
                        int(
                            self._root["BAND6_NPPC/STANDARD_MODE"]
                            .dimensions["ground_pixel"]
                            .size
                        ),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "npbd6:analysed_s5p_band": int(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "S5P_Band_Number"
                        )
                    ),
                    "npbd6:VIIRS_band": [
                        int(band)
                        for band in self._root["METADATA/ALGORITHM_SETTINGS"]
                        .getncattr("VIIRS_Bands")
                        .split("; ")[:-1]
                    ],
                    "npbd6:number_of_scaled_fov": int(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "Number_of_scaled_FOV"
                        )
                    ),
                }
            elif "_BD7_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root.time_coverage_end),
                    "instruments": [
                        str(
                            self._root[
                                "METADATA/EOP_METADATA/om:procedure/eop:instrument"
                            ].getncattr("eop:shortName")
                        )
                    ],
                    "s5p:processing_mode": str(
                        self._root[
                            "METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing"
                        ].getncattr("eop:processingMode")
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA/GRANULE_DESCRIPTION"].getncattr(
                            "ProductShortName"
                        )
                    ),
                    "s5p:shape": [
                        int(
                            self._root["BAND7_NPPC/STANDARD_MODE"]
                            .dimensions["scanline"]
                            .size
                        ),
                        int(
                            self._root["BAND7_NPPC/STANDARD_MODE"]
                            .dimensions["ground_pixel"]
                            .size
                        ),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "npbd7:analysed_s5p_band": int(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "S5P_Band_Number"
                        )
                    ),
                    "npbd7:VIIRS_band": [
                        int(band)
                        for band in self._root["METADATA/ALGORITHM_SETTINGS"]
                        .getncattr("VIIRS_Bands")
                        .split("; ")[:-1]
                    ],
                    "npbd7:number_of_scaled_fov": int(
                        self._root["METADATA/ALGORITHM_SETTINGS"].getncattr(
                            "Number_of_scaled_FOV"
                        )
                    ),
                }
        else:
            start_datetime = _get_start_datetime_from_json(self.file_path, self._root)
            observed_after_res_upgraded = _observed_after_res_upgraded(
                start_datetime[0]
            )
            spatial_resolution = _get_resolution_from_json(
                self.file_path, self._root, observed_after_res_upgraded
            )
            if "_AER_AI_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root["time_coverage_end"]),
                    "instruments": [str(self._root["sensor"])],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"]["dimensions"]["scanline"]),
                        int(self._root["PRODUCT"]["dimensions"]["ground_pixel"]),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "aer_ai:geolocation_grid_from_band": int(
                        self._root["geolocation_grid_from_band"]
                    ),
                    "aer_ai:input_band": str(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.type"]
                    ),
                    "aer_ai:irradiance_accompanied": str(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.irrType"]
                    ),
                }
            elif "_AER_LH_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root["time_coverage_end"]),
                    "instruments": [str(self._root["sensor"])],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"]["dimensions"]["scanline"]),
                        int(self._root["PRODUCT"]["dimensions"]["ground_pixel"]),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "aer_lh:geolocation_grid_from_band": int(
                        self._root["geolocation_grid_from_band"]
                    ),
                    "aer_lh:input_band": [
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.2.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.3.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.4.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.5.type"],
                    ],
                    "aer_lh:irradiance_accompanied": str(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.irrType"]
                    ),
                }
            elif "_CH4_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root["time_coverage_end"]),
                    "instruments": [str(self._root["sensor"])],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"]["dimensions"]["scanline"]),
                        int(self._root["PRODUCT"]["dimensions"]["ground_pixel"]),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "ch4:geolocation_grid_from_band": int(
                        self._root["geolocation_grid_from_band"]
                    ),
                    "ch4:input_band": [
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.2.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.3.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.4.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.5.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.6.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.7.type"],
                    ],
                    "ch4:irradiance_accompanied": [
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.irrType"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.3.irrType"],
                    ],
                }
            elif "_CLOUD_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0] + "Z"),
                    "end_datetime": str(self._root["time_coverage_end"] + "Z"),
                    "instruments": [str(self._root["sensor"])],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"]["dimensions"]["scanline"]),
                        int(self._root["PRODUCT"]["dimensions"]["ground_pixel"]),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "cloud:geolocation_grid_from_band": int(
                        self._root["geolocation_grid_from_band"]
                    ),
                    "cloud:cloud_mode": str(self._root["cloud_mode"]),
                }
            elif "_CO_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root["time_coverage_end"]),
                    "instruments": [str(self._root["sensor"])],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"]["dimensions"]["scanline"]),
                        int(self._root["PRODUCT"]["dimensions"]["ground_pixel"]),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "co:geolocation_grid_from_band": int(
                        self._root["geolocation_grid_from_band"]
                    ),
                    "co:input_band": [
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.2.type"],
                    ],
                    "co:irradiance_accompanied": str(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.irrType"]
                    ),
                }
            elif "_HCHO_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0] + "Z"),
                    "end_datetime": str(self._root["time_coverage_end"] + "Z"),
                    "instruments": [str(self._root["sensor"])],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"]["dimensions"]["scanline"]),
                        int(self._root["PRODUCT"]["dimensions"]["ground_pixel"]),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "hcho:geolocation_grid_from_band": int(
                        self._root["geolocation_grid_from_band"]
                    ),
                    "hcho:cloud_mode": str(self._root["cloud_mode"]),
                }
            elif "_NO2_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root["time_coverage_end"]),
                    "instruments": [str(self._root["sensor"])],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"]["dimensions"]["scanline"]),
                        int(self._root["PRODUCT"]["dimensions"]["ground_pixel"]),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "no2:geolocation_grid_from_band": int(
                        self._root["geolocation_grid_from_band"]
                    ),
                    "no2:input_band": [
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.2.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.3.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.4.type"],
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.5.type"],
                    ],
                    "no2:irradiance_accompanied": str(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["input.1.irrType"]
                    ),
                }
            elif "_O3__" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0] + "Z"),
                    "end_datetime": str(self._root["time_coverage_end"] + "Z"),
                    "instruments": [str(self._root["sensor"])],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"]["dimensions"]["scanline"]),
                        int(self._root["PRODUCT"]["dimensions"]["ground_pixel"]),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "o3:geolocation_grid_from_band": int(
                        self._root["geolocation_grid_from_band"]
                    ),
                    "o3:cloud_mode": str(self._root["cloud_mode"]),
                }
            elif "O3_TCL" in self.file_path:
                result = {
                    "instruments": [
                        str(
                            self._root["METADATA"]["GRANULE_DESCRIPTION"][
                                "InstrumentName"
                            ].upper()
                        )
                    ],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:spatial_resolution": spatial_resolution,
                    "o3_tcl:shape_ccd": [
                        int(self._root["PRODUCT"]["dimensions"]["latitude_ccd"]),
                        int(self._root["PRODUCT"]["dimensions"]["longitude_ccd"]),
                    ],
                    "o3_tcl:shape_csa": [
                        int(self._root["PRODUCT"]["dimensions"]["latitude_csa"]),
                        int(self._root["PRODUCT"]["dimensions"]["longitude_csa"]),
                    ],
                    "o3_tcl:stratosphere_start_datetime": str(start_datetime[0] + "Z"),
                    "o3_tcl:stratosphere_end_datetime": str(
                        self._root["time_coverage_end"] + "Z"
                    ),
                    "o3_tcl:troposphere_start_datetime": str(start_datetime[1] + "Z"),
                    "o3_tcl:troposphere_end_datetime": str(
                        self._root["time_coverage_troposphere_end"] + "Z"
                    ),
                    "o3_tcl:input_orbits": [
                        int(num)
                        for num in self._root["METADATA"]["input_orbits"].split(" ")
                    ],
                    "o3_tcl:input_files": [
                        file.split("/")[-1].split(".")[0]
                        for file in self._root["METADATA"]["input_files"].split(" ")
                    ],
                }
            elif "_SO2_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0] + "Z"),
                    "end_datetime": str(self._root["time_coverage_end"] + "Z"),
                    "instruments": [str(self._root["sensor"])],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:shape": [
                        int(self._root["PRODUCT"]["dimensions"]["scanline"]),
                        int(self._root["PRODUCT"]["dimensions"]["ground_pixel"]),
                    ],
                    "s5p:spatial_resolution": spatial_resolution,
                    "so2:geolocation_grid_from_band": int(
                        self._root["geolocation_grid_from_band"]
                    ),
                    "so2:cloud_mode": str(self._root["cloud_mode"]),
                }
            elif "_BD3_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root["time_coverage_end"]),
                    "instruments": [
                        str(
                            self._root["METADATA"]["EOP_METADATA"]["om:procedure"][
                                "eop:instrument"
                            ]["eop:shortName"]
                        )
                    ],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:spatial_resolution": spatial_resolution,
                    "s5p:shape": [
                        int(
                            self._root["BAND3_NPPC"]["STANDARD_MODE"]["dimensions"][
                                "scanline"
                            ]
                        ),
                        int(
                            self._root["BAND3_NPPC"]["STANDARD_MODE"]["dimensions"][
                                "ground_pixel"
                            ]
                        ),
                    ],
                    "npbd3:analysed_s5p_band": int(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["S5P_Band_Number"]
                    ),
                    "npbd3:VIIRS_band": [
                        int(band)
                        for band in self._root["METADATA"]["ALGORITHM_SETTINGS"][
                            "VIIRS_Bands"
                        ].split("; ")[:-1]
                    ],
                    "npbd3:number_of_scaled_fov": int(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"][
                            "Number_of_scaled_FOV"
                        ]
                    ),
                }
            elif "_BD6_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root["time_coverage_end"]),
                    "instruments": [
                        str(
                            self._root["METADATA"]["EOP_METADATA"]["om:procedure"][
                                "eop:instrument"
                            ]["eop:shortName"]
                        )
                    ],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:spatial_resolution": spatial_resolution,
                    "s5p:shape": [
                        int(
                            self._root["BAND6_NPPC"]["STANDARD_MODE"]["dimensions"][
                                "scanline"
                            ]
                        ),
                        int(
                            self._root["BAND6_NPPC"]["STANDARD_MODE"]["dimensions"][
                                "ground_pixel"
                            ]
                        ),
                    ],
                    "npbd6:analysed_s5p_band": int(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["S5P_Band_Number"]
                    ),
                    "npbd6:VIIRS_band": [
                        int(band)
                        for band in self._root["METADATA"]["ALGORITHM_SETTINGS"][
                            "VIIRS_Bands"
                        ].split("; ")[:-1]
                    ],
                    "npbd6:number_of_scaled_fov": int(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"][
                            "Number_of_scaled_FOV"
                        ]
                    ),
                }
            elif "_BD7_" in self.file_path:
                result = {
                    "start_datetime": str(start_datetime[0]),
                    "end_datetime": str(self._root["time_coverage_end"]),
                    "instruments": [
                        str(
                            self._root["METADATA"]["EOP_METADATA"]["om:procedure"][
                                "eop:instrument"
                            ]["eop:shortName"]
                        )
                    ],
                    "s5p:processing_mode": str(
                        self._root["METADATA"]["EOP_METADATA"]["eop:metaDataProperty"][
                            "eop:processing"
                        ]["eop:processingMode"]
                    ),
                    "s5p:product_type": str(
                        self._root["METADATA"]["GRANULE_DESCRIPTION"][
                            "ProductShortName"
                        ]
                    ),
                    "s5p:spatial_resolution": spatial_resolution,
                    "s5p:shape": [
                        int(
                            self._root["BAND7_NPPC"]["STANDARD_MODE"]["dimensions"][
                                "scanline"
                            ]
                        ),
                        int(
                            self._root["BAND7_NPPC"]["STANDARD_MODE"]["dimensions"][
                                "ground_pixel"
                            ]
                        ),
                    ],
                    "npbd7:analysed_s5p_band": int(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"]["S5P_Band_Number"]
                    ),
                    "npbd7:VIIRS_band": [
                        int(band)
                        for band in self._root["METADATA"]["ALGORITHM_SETTINGS"][
                            "VIIRS_Bands"
                        ].split("; ")[:-1]
                    ],
                    "npbd7:number_of_scaled_fov": int(
                        self._root["METADATA"]["ALGORITHM_SETTINGS"][
                            "Number_of_scaled_FOV"
                        ]
                    ),
                }

        return {k: v for k, v in result.items() if v is not None}
