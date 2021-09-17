from datetime import datetime
from typing import Any, Dict, Optional

import netCDF4 as nc  # type: ignore
from pystac.utils import str_to_datetime
from shapely.geometry import Polygon, mapping  # type: ignore


class ProductMetadataError(Exception):
    pass


class ProductMetadata:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self._root = nc.Dataset(file_path)

    @property
    def scene_id(self) -> str:
        """Returns the string to be used for a STAC Item id.

        """
        product_id = self.product_id
        if not product_id.startswith("S5P"):
            raise ValueError("Unexpected value found at "
                             f"{product_id}: "
                             "this was expected to follow the sentinel 5P "
                             "naming convention, starting with S5P")
        scene_id = self.product_id

        return scene_id

    @property
    def product_id(self) -> str:
        result = self.file_path.split("/")[-1].split(".")[0]
        if result is None:
            raise ValueError(
                "Cannot determine product ID using product metadata "
                f"at {self.file_path}")
        else:
            return result

    @property
    def get_geometry(self):
        if "O3_TCL" in self.file_path:
            latitude_ccd = self._root['/PRODUCT/latitude_ccd'][:]
            longitude_ccd = self._root['/PRODUCT/longitude_ccd'][:]
            footprint_polygon = Polygon(
                list([[coord, latitude_ccd[0]] for coord in longitude_ccd] +
                     [[longitude_ccd[-1], coord] for coord in latitude_ccd] +
                     [[coord, latitude_ccd[-1]]
                      for coord in longitude_ccd[::-1]] +
                     [[longitude_ccd[0], coord]
                      for coord in latitude_ccd[::-1]]))
        else:
            footprint_text = self._root[
                '/METADATA/EOP_METADATA/'
                'om:featureOfInterest/eop:multiExtentOf/'
                'gml:surfaceMembers/gml:exterior'].getncattr('gml:posList')
            if footprint_text is None:
                ProductMetadataError(
                    f"Cannot parse footprint from product metadata at {self.file_path}"
                )
            footprint_value = [
                float(coord)
                for coord in footprint_text.replace(" ", ",").split(",")
            ]
            footprint_points = [
                point[::-1]
                for point in list(zip(*[iter(footprint_value)] * 2))
            ]
            footprint_polygon = Polygon(footprint_points)
        geometry = mapping(footprint_polygon)
        self.footprint_polygon = footprint_polygon
        return geometry

    @property
    def get_bbox(self) -> list:
        bbox = list(self.footprint_polygon.bounds)
        return bbox

    @property
    def get_datetime(self) -> datetime:
        start_time = self._root.time_coverage_start
        end_time = self._root.time_coverage_end
        format_1 = "%Y-%m-%dT%H:%M:%SZ"
        format_2 = "%Y-%m-%dT%H:%M:%S"
        if len(start_time) == 20:
            datetime_format = format_1
        elif len(start_time) == 19:
            datetime_format = format_2
        central_time = (datetime.strptime(start_time, datetime_format) +
                        (datetime.strptime(end_time, datetime_format) -
                         datetime.strptime(start_time, datetime_format)) / 2)

        if central_time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.file_path}")
        else:
            return str_to_datetime(str(central_time))

    @property
    def platform(self) -> Optional[str]:

        if "O3_TCL" in self.file_path:
            platform_name = str(
                self._root['METADATA/GRANULE_DESCRIPTION'].MissionName)
        else:
            platform_name = str(self._root[
                'METADATA/ISO_METADATA/gmi:acquisitionInformation/gmi:platform']
                                .getncattr("gmi:description"))

        return platform_name

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        if "_AER_AI_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start),
                "end_datetime":
                str(self._root.time_coverage_end),
                "s5p:instrument":
                str(self._root.sensor),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "aer_ai:spatial_resolution":
                str(self._root.spatial_resolution),
                "aer_ai:geolocation_grid_from_band":
                int(self._root.geolocation_grid_from_band),
                "aer_ai:input_band":
                str(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    'input.1.type')),
                "aer_ai:irradiance_accompanied":
                str(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    'input.1.irrType')),
            }
        elif "_AER_LH_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start),
                "end_datetime":
                str(self._root.time_coverage_end),
                "s5p:instrument":
                str(self._root.sensor),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "aer_lh:spatial_resolution":
                str(self._root.spatial_resolution),
                "aer_lh:geolocation_grid_from_band":
                int(self._root.geolocation_grid_from_band),
                "aer_lh:input_band": [
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.1.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.2.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.3.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.4.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.5.type'),
                ],
                "aer_lh:irradiance_accompanied":
                str(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    'input.1.irrType')),
            }
        elif "_CH4_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start),
                "end_datetime":
                str(self._root.time_coverage_end),
                "s5p:instrument":
                str(self._root.sensor),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "ch4:spatial_resolution":
                str(self._root.spatial_resolution),
                "ch4:geolocation_grid_from_band":
                int(self._root.geolocation_grid_from_band),
                "ch4:input_band": [
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.1.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.2.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.3.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.4.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.5.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.6.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.7.type'),
                ],
                "ch4:irradiance_accompanied": [
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.1.irrType'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.3.irrType'),
                ],
            }
        elif "_CLOUD_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start + "Z"),
                "end_datetime":
                str(self._root.time_coverage_end + "Z"),
                "s5p:instrument":
                str(self._root.sensor),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "cloud:spatial_resolution":
                str(self._root.spatial_resolution),
                "cloud:geolocation_grid_from_band":
                int(self._root.geolocation_grid_from_band),
                "cloud:cloud_mode":
                str(self._root.cloud_mode),
            }
        elif "_CO_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start),
                "end_datetime":
                str(self._root.time_coverage_end),
                "s5p:instrument":
                str(self._root.sensor),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "co:spatial_resolution":
                str(self._root.spatial_resolution),
                "co:geolocation_grid_from_band":
                int(self._root.geolocation_grid_from_band),
                "co:input_band": [
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.1.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.2.type')
                ],
                "co:irradiance_accompanied":
                str(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    'input.1.irrType')),
            }
        elif "_HCHO_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start + "Z"),
                "end_datetime":
                str(self._root.time_coverage_end + "Z"),
                "s5p:instrument":
                str(self._root.sensor),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "hcho:spatial_resolution":
                str(self._root.spatial_resolution),
                "hcho:geolocation_grid_from_band":
                int(self._root.geolocation_grid_from_band),
                "hcho:cloud_mode":
                str(self._root.cloud_mode)
            }
        elif "_NO2_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start),
                "end_datetime":
                str(self._root.time_coverage_end),
                "s5p:instrument":
                str(self._root.sensor),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "no2:spatial_resolution":
                str(self._root.spatial_resolution),
                "no2:geolocation_grid_from_band":
                int(self._root.geolocation_grid_from_band),
                "no2:input_band": [
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.1.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.2.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.3.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.4.type'),
                    self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                        'input.5.type'),
                ],
                "no2:irradiance_accompanied":
                str(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    'input.1.irrType')),
            }
        elif "_O3__" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start + "Z"),
                "end_datetime":
                str(self._root.time_coverage_end + "Z"),
                "s5p:instrument":
                str(self._root.sensor),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "o3:spatial_resolution":
                str(self._root.spatial_resolution),
                "o3:geolocation_grid_from_band":
                int(self._root.geolocation_grid_from_band),
                "o3:cloud_mode":
                str(self._root.cloud_mode)
            }
        elif "O3_TCL" in self.file_path:
            result = {
                "o3_tcl:shape_ccd": [
                    int(self._root['PRODUCT'].dimensions['latitude_ccd'].size),
                    int(self._root['PRODUCT'].dimensions['longitude_ccd'].size)
                ],
                "o3_tcl:shape_csa": [
                    int(self._root['PRODUCT'].dimensions['latitude_csa'].size),
                    int(self._root['PRODUCT'].dimensions['longitude_csa'].size)
                ],
                "s5p:instrument":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].InstrumentName.
                    upper()),
                "s5p:processing_mode":
                str(self._root['METADATA'].processingMode),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "o3_tcl:stratosphere_start_datetime":
                str(self._root.time_coverage_start + "Z"),
                "o3_tcl:stratosphere_end_datetime":
                str(self._root.time_coverage_end + "Z"),
                "o3_tcl:troposphere_start_datetime":
                str(self._root.time_coverage_troposphere_start + "Z"),
                "o3_tcl:troposphere_end_datetime":
                str(self._root.time_coverage_troposphere_end + "Z"),
                "o3_tcl:input_orbits": [
                    int(num)
                    for num in self._root['METADATA'].input_orbits.split(" ")
                ],
                "o3_tcl:input_files": [
                    file.split("/")[-1].split(".")[0]
                    for file in self._root['METADATA'].input_files.split(" ")
                ],
            }
        elif "_SO2_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start + "Z"),
                "end_datetime":
                str(self._root.time_coverage_end + "Z"),
                "s5p:instrument":
                str(self._root.sensor),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "so2:spatial_resolution":
                str(self._root.spatial_resolution),
                "so2:geolocation_grid_from_band":
                int(self._root.geolocation_grid_from_band),
                "so2:cloud_mode":
                str(self._root.cloud_mode)
            }
        elif "_BD3_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start),
                "end_datetime":
                str(self._root.time_coverage_end),
                "s5p:instrument":
                str(self.
                    _root['METADATA/EOP_METADATA/om:procedure/eop:instrument'].
                    getncattr("eop:shortName")),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "npbd3:analysed_s5p_band":
                int(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    "S5P_Band_Number")),
                "npbd3:VIIRS_band": [
                    int(band)
                    for band in self._root['METADATA/ALGORITHM_SETTINGS'].
                    getncattr("VIIRS_Bands").split("; ")[:-1]
                ],
                "npbd3:number_of_scaled_fov":
                int(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    "Number_of_scaled_FOV"))
            }
        elif "_BD6_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start),
                "end_datetime":
                str(self._root.time_coverage_end),
                "s5p:instrument":
                str(self.
                    _root['METADATA/EOP_METADATA/om:procedure/eop:instrument'].
                    getncattr("eop:shortName")),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "npbd6:analysed_s5p_band":
                int(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    "S5P_Band_Number")),
                "npbd6:VIIRS_band": [
                    int(band)
                    for band in self._root['METADATA/ALGORITHM_SETTINGS'].
                    getncattr("VIIRS_Bands").split("; ")[:-1]
                ],
                "npbd6:number_of_scaled_fov":
                int(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    "Number_of_scaled_FOV"))
            }
        elif "_BD7_" in self.file_path:
            result = {
                "start_datetime":
                str(self._root.time_coverage_start),
                "end_datetime":
                str(self._root.time_coverage_end),
                "s5p:instrument":
                str(self.
                    _root['METADATA/EOP_METADATA/om:procedure/eop:instrument'].
                    getncattr("eop:shortName")),
                "s5p:processing_mode":
                str(self._root[
                    'METADATA/EOP_METADATA/eop:metaDataProperty/eop:processing']
                    .getncattr('eop:processingMode')),
                "s5p:product_type":
                str(self._root['METADATA/GRANULE_DESCRIPTION'].getncattr(
                    'ProductShortName')),
                "npbd7:analysed_s5p_band":
                int(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    "S5P_Band_Number")),
                "npbd7:VIIRS_band": [
                    int(band)
                    for band in self._root['METADATA/ALGORITHM_SETTINGS'].
                    getncattr("VIIRS_Bands").split("; ")[:-1]
                ],
                "npbd7:number_of_scaled_fov":
                int(self._root['METADATA/ALGORITHM_SETTINGS'].getncattr(
                    "Number_of_scaled_FOV"))
            }

        return {k: v for k, v in result.items() if v is not None}
