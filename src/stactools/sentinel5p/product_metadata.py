import os
import netCDF4 as nc
from datetime import datetime
from typing import Any, Dict, List, Optional

from pystac.utils import str_to_datetime
from shapely.geometry import Polygon, mapping

class ProductMetadataError(Exception):
    pass

class ProductMetadata:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self._root = nc.Dataset(file_path)
        
        def _get_geometries():
            footprint_text = self._root['/METADATA/EOP_METADATA/om:featureOfInterest/eop:multiExtentOf/gml:surfaceMembers/gml:exterior'].getncattr('gml:posList')
            if footprint_text is None:
                ProductMetadataError(
                    f"Cannot parse footprint from product metadata at {self.file_path}"
                )
            footprint_value = [float(coord) for coord in footprint_text.replace(" ", ",").split(",")]
            footprint_points = [point[::-1] for point in list(zip(*[iter(footprint_value)] * 2))]
            footprint_polygon = Polygon(footprint_points)
            geometry = mapping(footprint_polygon)
            bbox = list(footprint_polygon.bounds)

            return (bbox, geometry)

        self.bbox, self.geometry = _get_geometries()
    
    @property
    def scene_id(self) -> str:
        """Returns the string to be used for a STAC Item id.

        """
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
        result = self._root.id
        if result is None:
            raise ValueError(
                "Cannot determine product ID using product metadata "
                f"at {self.file_path}"
            )
        else:
            return result
    
    @property
    def get_datetime(self) -> datetime:
        start_time = self._root.time_coverage_start
        end_time = self._root.time_coverage_end

        central_time = (
            datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ") +
            (datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ") - 
             datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")) / 2
        )

        if central_time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.file_path}"
            )
        else:
            return str_to_datetime(str(central_time))