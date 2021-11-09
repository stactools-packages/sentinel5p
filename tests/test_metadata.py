import unittest

import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sat import SatExtension

from stactools.sentinel5p.product_metadata import ProductMetadata
from stactools.sentinel5p.properties import (fill_proj_properties,
                                             fill_sat_properties)
from tests import test_data


class Sentinel3OLCIMetadataTest(unittest.TestCase):
    def test_parses_aerai_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__AER_AI_"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010302_"
                                           "20200306T032414.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "spatial_resolution":
            item.properties["aer_ai:spatial_resolution"],
            "geolocation_grid_from_band":
            item.properties["aer_ai:geolocation_grid_from_band"],
            "input_band":
            item.properties["aer_ai:input_band"],
            "irradiance_accompanied":
            item.properties["aer_ai:irradiance_accompanied"],
        }

        expected = {
            "bbox": [-179.94377, -85.99168, 179.66743, 86.48782],
            "epsg": 4326,
            "datetime": "2020-03-03T02:26:33.500000Z",
            "absolute_orbit": 12367,
            "shape": [4172, 450],
            "instruments": ["TROPOMI"],
            "processing_mode": "OFFL",
            "product_type": "L2__AER_AI",
            "spatial_resolution": "7x3.5km2",
            "geolocation_grid_from_band": 3,
            "input_band": "L1B_RA_BD3",
            "irradiance_accompanied": "L1B_IR_UVN"
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_aerlh_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__AER_LH_"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010302_"
                                           "20200306T053814.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "spatial_resolution":
            item.properties["aer_lh:spatial_resolution"],
            "geolocation_grid_from_band":
            item.properties["aer_lh:geolocation_grid_from_band"],
            "input_band":
            item.properties["aer_lh:input_band"],
            "irradiance_accompanied":
            item.properties["aer_lh:irradiance_accompanied"],
        }

        expected = {
            "bbox": [-179.90239, -86.10597, 179.70866, 86.44622],
            "epsg":
            4326,
            "datetime":
            "2020-03-03T02:26:33.500000Z",
            "absolute_orbit":
            12367,
            "shape": [4172, 448],
            "instruments": ["TROPOMI"],
            "processing_mode":
            "OFFL",
            "product_type":
            "L2__AER_LH",
            "spatial_resolution":
            "7x3.5km2",
            "geolocation_grid_from_band":
            6,
            "input_band": [
                "L1B_RA_BD6", "L2__FRESCO", "L2__AER_AI", "L2__NP_BD6",
                "L2__CLOUD_"
            ],
            "irradiance_accompanied":
            "L1B_IR_UVN"
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_ch4_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__CH4____"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010302_"
                                           "20200306T053811.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "spatial_resolution":
            item.properties["ch4:spatial_resolution"],
            "geolocation_grid_from_band":
            item.properties["ch4:geolocation_grid_from_band"],
            "input_band":
            item.properties["ch4:input_band"],
            "irradiance_accompanied":
            item.properties["ch4:irradiance_accompanied"],
        }

        expected = {
            "bbox": [-179.9934, -85.990204, 179.84909, 86.633255],
            "epsg":
            4326,
            "datetime":
            "2020-03-03T02:26:33.500000Z",
            "absolute_orbit":
            12367,
            "shape": [4172, 215],
            "instruments": ["TROPOMI"],
            "processing_mode":
            "OFFL",
            "product_type":
            "L2__CH4___",
            "spatial_resolution":
            "7x7km2",
            "geolocation_grid_from_band":
            7,
            "input_band": [
                "L1B_RA_BD7", "L1B_RA_BD8", "L1B_RA_BD6", "L2__CO____",
                "L2__FRESCO", "L2__NP_BD6", "L2__NP_BD7"
            ],
            "irradiance_accompanied": ["L1B_IR_SIR", "L1B_IR_UVN"]
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_cloud_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__CLOUD__"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010107_"
                                           "20200306T032410.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "spatial_resolution":
            item.properties["cloud:spatial_resolution"],
            "geolocation_grid_from_band":
            item.properties["cloud:geolocation_grid_from_band"],
            "cloud_mode":
            item.properties["cloud:cloud_mode"],
        }

        expected = {
            "bbox": [-179.94377, -85.99168, 179.66743, 86.48782],
            "epsg": 4326,
            "datetime": "2020-03-03T02:26:33.500000Z",
            "absolute_orbit": 12367,
            "shape": [4172, 450],
            "instruments": ["TROPOMI"],
            "processing_mode": "OFFL",
            "product_type": "L2__CLOUD_",
            "spatial_resolution": "7x3.5km2",
            "geolocation_grid_from_band": 3,
            "cloud_mode": "cal",
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_co_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__CO_____"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010302_"
                                           "20200306T032410.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "spatial_resolution":
            item.properties["co:spatial_resolution"],
            "geolocation_grid_from_band":
            item.properties["co:geolocation_grid_from_band"],
            "input_band":
            item.properties["co:input_band"],
            "irradiance_accompanied":
            item.properties["co:irradiance_accompanied"]
        }

        expected = {
            "bbox": [-179.9934, -85.990204, 179.84909, 86.633255],
            "epsg": 4326,
            "datetime": "2020-03-03T02:26:33.500000Z",
            "absolute_orbit": 12367,
            "shape": [4172, 215],
            "instruments": ["TROPOMI"],
            "processing_mode": "OFFL",
            "product_type": "L2__CO____",
            "spatial_resolution": "7x7km2",
            "geolocation_grid_from_band": 7,
            "input_band": ["L1B_RA_BD7", "L1B_RA_BD8"],
            "irradiance_accompanied": "L1B_IR_SIR"
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_hcho_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__HCHO___"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010107_"
                                           "20200306T053811.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "spatial_resolution":
            item.properties["hcho:spatial_resolution"],
            "geolocation_grid_from_band":
            item.properties["hcho:geolocation_grid_from_band"],
            "cloud_mode":
            item.properties["hcho:cloud_mode"]
        }

        expected = {
            "bbox": [-179.94377, -85.99168, 179.66743, 86.48782],
            "epsg": 4326,
            "datetime": "2020-03-03T02:26:33.500000Z",
            "absolute_orbit": 12367,
            "shape": [4172, 450],
            "instruments": ["TROPOMI"],
            "processing_mode": "OFFL",
            "product_type": "L2__HCHO__",
            "spatial_resolution": "7x3.5km2",
            "geolocation_grid_from_band": 3,
            "cloud_mode": "crb"
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_no2_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__NO2____"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010302_"
                                           "20200306T053815.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "spatial_resolution":
            item.properties["no2:spatial_resolution"],
            "geolocation_grid_from_band":
            item.properties["no2:geolocation_grid_from_band"],
            "input_band":
            item.properties["no2:input_band"],
            "irradiance_accompanied":
            item.properties["no2:irradiance_accompanied"]
        }

        expected = {
            "bbox": [-179.94377, -85.99168, 179.66743, 86.48782],
            "epsg":
            4326,
            "datetime":
            "2020-03-03T02:26:33.500000Z",
            "absolute_orbit":
            12367,
            "shape": [4172, 450],
            "instruments": ["TROPOMI"],
            "processing_mode":
            "OFFL",
            "product_type":
            "L2__NO2___",
            "spatial_resolution":
            "7x3.5km2",
            "geolocation_grid_from_band":
            4,
            "input_band": [
                "L1B_RA_BD4", "L2__FRESCO", "L2__AER_AI", "L2__CLOUD_",
                "L2__O22CLD"
            ],
            "irradiance_accompanied":
            "L1B_IR_UVN"
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_o3_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__O3_____"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010107_"
                                           "20200306T053811.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "spatial_resolution":
            item.properties["o3:spatial_resolution"],
            "geolocation_grid_from_band":
            item.properties["o3:geolocation_grid_from_band"],
            "cloud_mode":
            item.properties["o3:cloud_mode"]
        }

        expected = {
            "bbox": [-179.94377, -85.99168, 179.66743, 86.48782],
            "epsg": 4326,
            "datetime": "2020-03-03T02:26:33.500000Z",
            "absolute_orbit": 12367,
            "shape": [4172, 450],
            "instruments": ["TROPOMI"],
            "processing_mode": "OFFL",
            "product_type": "L2__O3____",
            "spatial_resolution": "7x3.5km2",
            "geolocation_grid_from_band": 3,
            "cloud_mode": "crb",
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_o3tcl_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__O3_TCL_"
                                           "20200303T120623_20200309T125248_"
                                           "12373_01_010108_"
                                           "20200318T000106.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "shape":
            item.properties["proj:shape"],
            "shape_ccd":
            item.properties["o3_tcl:shape_ccd"],
            "shape_csa":
            item.properties["o3_tcl:shape_csa"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "stratosphere_start_datetime":
            item.properties["o3_tcl:stratosphere_start_datetime"],
            "stratosphere_end_datetime":
            item.properties["o3_tcl:stratosphere_end_datetime"],
            "troposphere_start_datetime":
            item.properties["o3_tcl:troposphere_start_datetime"],
            "troposphere_end_datetime":
            item.properties["o3_tcl:troposphere_end_datetime"],
            "input_orbits":
            item.properties["o3_tcl:input_orbits"],
            "input_files":
            item.properties["o3_tcl:input_files"]
        }

        expected = {
            "bbox": [-179.5, -19.75, 179.5, 19.75],
            "epsg":
            4326,
            "datetime":
            "2020-03-06T12:29:35.500000Z",
            "shape": [80, 360],
            "shape_ccd": [80, 360],
            "shape_csa": [8, 18],
            "instruments": ["TROPOMI"],
            "processing_mode":
            "OFFL",
            "product_type":
            "L2__O3_TCL",
            "stratosphere_start_datetime":
            "2020-03-03T12:06:23Z",
            "stratosphere_end_datetime":
            "2020-03-09T12:52:48Z",
            "troposphere_start_datetime":
            "2020-03-04T23:38Z",
            "troposphere_end_datetime":
            "2020-03-08T00:22Z",
            "input_orbits": [
                12373, 12374, 12375, 12376, 12377, 12378, 12379, 12380, 12381,
                12382, 12383, 12384, 12385, 12386, 12387, 12388, 12389, 12390,
                12391, 12392, 12393, 12394, 12395, 12396, 12397, 12398, 12399,
                12400, 12401, 12402, 12403, 12404, 12405, 12406, 12407, 12408,
                12409, 12410, 12411, 12412, 12413, 12414, 12415, 12416, 12417,
                12418, 12419, 12420, 12421, 12422, 12423, 12424, 12425, 12426,
                12427, 12428, 12429, 12430, 12431, 12432, 12433, 12434, 12435,
                12436, 12437, 12438, 12439, 12440, 12441, 12442, 12443, 12444,
                12445, 12446, 12447, 12448, 12449, 12450, 12451, 12452, 12453,
                12454, 12455, 12456, 12457, 12458
            ],
            "input_files": [
                "S5P_OFFL_L2__O3_____20200303T114449_20200303T132620_"
                "12373_01_010107_20200306T170003",
                "S5P_OFFL_L2__O3_____20200303T132620_20200303T150750_"
                "12374_01_010107_20200306T182028",
                "S5P_OFFL_L2__O3_____20200303T150750_20200303T164920_"
                "12375_01_010107_20200306T200743",
                "S5P_OFFL_L2__O3_____20200303T164920_20200303T183051_"
                "12376_01_010107_20200306T213844",
                "S5P_OFFL_L2__O3_____20200303T183051_20200303T201221_"
                "12377_01_010107_20200306T230821",
                "S5P_OFFL_L2__O3_____20200303T201221_20200303T215351_"
                "12378_01_010107_20200307T010636",
                "S5P_OFFL_L2__O3_____20200303T215351_20200303T233522_"
                "12379_01_010107_20200307T025926",
                "S5P_OFFL_L2__O3_____20200303T233522_20200304T011652_"
                "12380_01_010107_20200307T041446",
                "S5P_OFFL_L2__O3_____20200304T011652_20200304T025822_"
                "12381_01_010107_20200307T052756",
                "S5P_OFFL_L2__O3_____20200304T025822_20200304T043953_"
                "12382_01_010107_20200307T073145",
                "S5P_OFFL_L2__O3_____20200304T043953_20200304T062123_"
                "12383_01_010107_20200307T092706",
                "S5P_OFFL_L2__O3_____20200304T062123_20200304T080254_"
                "12384_01_010107_20200307T110630",
                "S5P_OFFL_L2__O3_____20200304T080254_20200304T094424_"
                "12385_01_010107_20200307T123841",
                "S5P_OFFL_L2__O3_____20200304T094424_20200304T112554_"
                "12386_01_010107_20200307T144512",
                "S5P_OFFL_L2__O3_____20200304T112554_20200304T130725_"
                "12387_01_010107_20200307T163406",
                "S5P_OFFL_L2__O3_____20200304T130725_20200304T144855_"
                "12388_01_010107_20200307T174529",
                "S5P_OFFL_L2__O3_____20200304T144855_20200304T163025_"
                "12389_01_010107_20200307T193347",
                "S5P_OFFL_L2__O3_____20200304T163025_20200304T181156_"
                "12390_01_010107_20200307T213401",
                "S5P_OFFL_L2__O3_____20200304T181156_20200304T195326_"
                "12391_01_010107_20200307T225836",
                "S5P_OFFL_L2__O3_____20200304T195326_20200304T213456_"
                "12392_01_010107_20200308T002340",
                "S5P_OFFL_L2__O3_____20200304T213456_20200304T231627_"
                "12393_01_010107_20200308T025429",
                "S5P_OFFL_L2__O3_____20200304T231627_20200305T005757_"
                "12394_01_010107_20200308T034542",
                "S5P_OFFL_L2__O3_____20200305T005757_20200305T023927_"
                "12395_01_010107_20200308T053244",
                "S5P_OFFL_L2__O3_____20200305T023927_20200305T042058_"
                "12396_01_010107_20200308T070640",
                "S5P_OFFL_L2__O3_____20200305T042058_20200305T060228_"
                "12397_01_010107_20200308T092931",
                "S5P_OFFL_L2__O3_____20200305T060228_20200305T074359_"
                "12398_01_010107_20200308T105340",
                "S5P_OFFL_L2__O3_____20200305T074359_20200305T092529_"
                "12399_01_010107_20200308T120820",
                "S5P_OFFL_L2__O3_____20200305T092529_20200305T110659_"
                "12400_01_010107_20200308T142338",
                "S5P_OFFL_L2__O3_____20200305T110659_20200305T124830_"
                "12401_01_010107_20200308T160619",
                "S5P_OFFL_L2__O3_____20200305T124830_20200305T143000_"
                "12402_01_010107_20200308T174044",
                "S5P_OFFL_L2__O3_____20200305T143000_20200305T161130_"
                "12403_01_010107_20200308T185946",
                "S5P_OFFL_L2__O3_____20200305T161130_20200305T175301_"
                "12404_01_010107_20200308T210309",
                "S5P_OFFL_L2__O3_____20200305T175301_20200305T193431_"
                "12405_01_010107_20200308T225228",
                "S5P_OFFL_L2__O3_____20200305T193431_20200305T211602_"
                "12406_01_010107_20200309T000858",
                "S5P_OFFL_L2__O3_____20200305T211602_20200305T225732_"
                "12407_01_010107_20200309T022445",
                "S5P_OFFL_L2__O3_____20200305T225732_20200306T003902_"
                "12408_01_010107_20200309T033313",
                "S5P_OFFL_L2__O3_____20200306T003902_20200306T022033_"
                "12409_01_010107_20200309T045529",
                "S5P_OFFL_L2__O3_____20200306T022033_20200306T040203_"
                "12410_01_010107_20200309T065258",
                "S5P_OFFL_L2__O3_____20200306T040203_20200306T054333_"
                "12411_01_010107_20200309T085014",
                "S5P_OFFL_L2__O3_____20200306T054333_20200306T072504_"
                "12412_01_010107_20200309T102822",
                "S5P_OFFL_L2__O3_____20200306T072504_20200306T090634_"
                "12413_01_010107_20200309T115316",
                "S5P_OFFL_L2__O3_____20200306T090634_20200306T104805_"
                "12414_01_010107_20200309T140600",
                "S5P_OFFL_L2__O3_____20200306T104805_20200306T122935_"
                "12415_01_010107_20200309T161059",
                "S5P_OFFL_L2__O3_____20200306T122935_20200306T141105_"
                "12416_01_010107_20200309T171214",
                "S5P_OFFL_L2__O3_____20200306T141105_20200306T155235_"
                "12417_01_010107_20200309T184451",
                "S5P_OFFL_L2__O3_____20200306T155235_20200306T173406_"
                "12418_01_010107_20200309T202951",
                "S5P_OFFL_L2__O3_____20200306T173406_20200306T191536_"
                "12419_01_010107_20200309T222813",
                "S5P_OFFL_L2__O3_____20200306T191536_20200306T205707_"
                "12420_01_010107_20200310T001429",
                "S5P_OFFL_L2__O3_____20200306T205707_20200306T223837_"
                "12421_01_010107_20200310T014311",
                "S5P_OFFL_L2__O3_____20200306T223837_20200307T002007_"
                "12422_01_010107_20200310T032121",
                "S5P_OFFL_L2__O3_____20200307T002007_20200307T020138_"
                "12423_01_010107_20200310T042900",
                "S5P_OFFL_L2__O3_____20200307T020138_20200307T034308_"
                "12424_01_010107_20200310T062207",
                "S5P_OFFL_L2__O3_____20200307T034308_20200307T052438_"
                "12425_01_010107_20200310T084429",
                "S5P_OFFL_L2__O3_____20200307T052438_20200307T070609_"
                "12426_01_010107_20200310T095951",
                "S5P_OFFL_L2__O3_____20200307T070609_20200307T084739_"
                "12427_01_010107_20200310T113730",
                "S5P_OFFL_L2__O3_____20200307T084739_20200307T102910_"
                "12428_01_010107_20200310T175559",
                "S5P_OFFL_L2__O3_____20200307T102910_20200307T121040_"
                "12429_01_010107_20200310T175312",
                "S5P_OFFL_L2__O3_____20200307T121040_20200307T135210_"
                "12430_01_010107_20200310T175351",
                "S5P_OFFL_L2__O3_____20200307T135210_20200307T153341_"
                "12431_01_010107_20200310T183217",
                "S5P_OFFL_L2__O3_____20200307T153341_20200307T171511_"
                "12432_01_010108_20200312T101018",
                "S5P_OFFL_L2__O3_____20200307T171511_20200307T185641_"
                "12433_01_010108_20200312T101715",
                "S5P_OFFL_L2__O3_____20200307T185641_20200307T203812_"
                "12434_01_010108_20200312T102133",
                "S5P_OFFL_L2__O3_____20200307T203812_20200307T221942_"
                "12435_01_010108_20200312T102107",
                "S5P_OFFL_L2__O3_____20200307T221942_20200308T000112_"
                "12436_01_010108_20200312T104314",
                "S5P_OFFL_L2__O3_____20200308T000112_20200308T014243_"
                "12437_01_010108_20200312T095104",
                "S5P_OFFL_L2__O3_____20200308T014243_20200308T032413_"
                "12438_01_010108_20200312T100243",
                "S5P_OFFL_L2__O3_____20200308T032413_20200308T050543_"
                "12439_01_010108_20200312T101750",
                "S5P_OFFL_L2__O3_____20200308T050543_20200308T064714_"
                "12440_01_010108_20200312T101824",
                "S5P_OFFL_L2__O3_____20200308T064714_20200308T082844_"
                "12441_01_010108_20200312T103104",
                "S5P_OFFL_L2__O3_____20200308T082844_20200308T101015_"
                "12442_01_010108_20200312T103411",
                "S5P_OFFL_L2__O3_____20200308T101015_20200308T115145_"
                "12443_01_010108_20200312T105149",
                "S5P_OFFL_L2__O3_____20200308T115145_20200308T133315_"
                "12444_01_010108_20200312T104632",
                "S5P_OFFL_L2__O3_____20200308T133315_20200308T151446_"
                "12445_01_010108_20200312T102440",
                "S5P_OFFL_L2__O3_____20200308T151446_20200308T165616_"
                "12446_01_010108_20200312T102837",
                "S5P_OFFL_L2__O3_____20200308T165616_20200308T183746_"
                "12447_01_010108_20200312T104932",
                "S5P_OFFL_L2__O3_____20200308T183746_20200308T201917_"
                "12448_01_010108_20200312T103653",
                "S5P_OFFL_L2__O3_____20200308T201917_20200308T220047_"
                "12449_01_010108_20200312T102249",
                "S5P_OFFL_L2__O3_____20200308T220047_20200308T234218_"
                "12450_01_010108_20200312T111106",
                "S5P_OFFL_L2__O3_____20200308T234218_20200309T012348_"
                "12451_01_010108_20200312T102859",
                "S5P_OFFL_L2__O3_____20200309T012348_20200309T030518_"
                "12452_01_010108_20200312T161945",
                "S5P_OFFL_L2__O3_____20200309T030518_20200309T044649_"
                "12453_01_010108_20200312T161829",
                "S5P_OFFL_L2__O3_____20200309T044649_20200309T062819_"
                "12454_01_010108_20200312T170548",
                "S5P_OFFL_L2__O3_____20200309T062819_20200309T080949_"
                "12455_01_010108_20200312T170827",
                "S5P_OFFL_L2__O3_____20200309T080949_20200309T095120_"
                "12456_01_010108_20200312T174255",
                "S5P_OFFL_L2__O3_____20200309T095120_20200309T113250_"
                "12457_01_010108_20200312T225108",
                "S5P_OFFL_L2__O3_____20200309T113250_20200309T131421_"
                "12458_01_010108_20200312T231414"
            ]
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_so2_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__SO2____"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010107_"
                                           "20200306T144427.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instruments":
            item.properties["instruments"],
            "processing_mode":
            item.properties["s5p:processing_mode"],
            "product_type":
            item.properties["s5p:product_type"],
            "spatial_resolution":
            item.properties["so2:spatial_resolution"],
            "geolocation_grid_from_band":
            item.properties["so2:geolocation_grid_from_band"],
            "cloud_mode":
            item.properties["so2:cloud_mode"]
        }

        expected = {
            "bbox": [-179.94377, -85.99168, 179.66743, 86.48782],
            "epsg": 4326,
            "datetime": "2020-03-03T02:26:33.500000Z",
            "absolute_orbit": 12367,
            "shape": [4172, 450],
            "instruments": ["TROPOMI"],
            "processing_mode": "OFFL",
            "product_type": "L2__SO2___",
            "spatial_resolution": "7x3.5km2",
            "geolocation_grid_from_band": 3,
            "cloud_mode": "crb",
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_npbd3_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__NP_BD3_"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010002_"
                                           "20200306T032410.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox": item.bbox,
            "epsg": item.properties["proj:epsg"],
            "datetime": item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit": item.properties["sat:absolute_orbit"],
            "shape": item.properties["proj:shape"],
            "instruments": item.properties["instruments"],
            "processing_mode": item.properties["s5p:processing_mode"],
            "product_type": item.properties["s5p:product_type"],
            "analysed_s5p_band": item.properties["npbd3:analysed_s5p_band"],
            "VIIRS_band": item.properties["npbd3:VIIRS_band"],
            "number_of_scaled_fov":
            item.properties["npbd3:number_of_scaled_fov"]
        }

        expected = {
            "bbox": [-179.94377, -85.99168, 179.66743, 86.48782],
            "epsg": 4326,
            "datetime": "2020-03-03T02:26:33.500000Z",
            "absolute_orbit": 12367,
            "shape": [4172, 450],
            "instruments": ["TROPOMI"],
            "processing_mode": "OFFL",
            "product_type": "L2__NP_BD3",
            "analysed_s5p_band": 3,
            "VIIRS_band": [7, 9, 11],
            "number_of_scaled_fov": 4
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_npbd6_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__NP_BD6_"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010002_"
                                           "20200306T032654.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox": item.bbox,
            "epsg": item.properties["proj:epsg"],
            "datetime": item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit": item.properties["sat:absolute_orbit"],
            "shape": item.properties["proj:shape"],
            "instruments": item.properties["instruments"],
            "processing_mode": item.properties["s5p:processing_mode"],
            "product_type": item.properties["s5p:product_type"],
            "analysed_s5p_band": item.properties["npbd6:analysed_s5p_band"],
            "VIIRS_band": item.properties["npbd6:VIIRS_band"],
            "number_of_scaled_fov":
            item.properties["npbd6:number_of_scaled_fov"]
        }

        expected = {
            "bbox": [-179.90239, -86.10597, 179.70866, 86.44622],
            "epsg": 4326,
            "datetime": "2020-03-03T02:26:33.500000Z",
            "absolute_orbit": 12367,
            "shape": [4172, 448],
            "instruments": ["TROPOMI"],
            "processing_mode": "OFFL",
            "product_type": "L2__NP_BD6",
            "analysed_s5p_band": 6,
            "VIIRS_band": [7, 9, 11],
            "number_of_scaled_fov": 4
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)

    def test_parses_npbd7_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path("data-files/"
                                           "S5P_OFFL_L2__NP_BD7_"
                                           "20200303T013547_20200303T031717_"
                                           "12367_01_010002_"
                                           "20200306T032925.nc")

        product_metadata = ProductMetadata(manifest_path)

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.get_geometry,
            bbox=product_metadata.get_bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, manifest_path)

        # eo
        EOExtension.ext(item, add_if_missing=True)

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, manifest_path)

        # s5p product properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s5p_props = {
            "bbox": item.bbox,
            "epsg": item.properties["proj:epsg"],
            "datetime": item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "absolute_orbit": item.properties["sat:absolute_orbit"],
            "shape": item.properties["proj:shape"],
            "instruments": item.properties["instruments"],
            "processing_mode": item.properties["s5p:processing_mode"],
            "product_type": item.properties["s5p:product_type"],
            "analysed_s5p_band": item.properties["npbd7:analysed_s5p_band"],
            "VIIRS_band": item.properties["npbd7:VIIRS_band"],
            "number_of_scaled_fov":
            item.properties["npbd7:number_of_scaled_fov"]
        }

        expected = {
            "bbox": [-179.9934, -85.990204, 179.84909, 86.633255],
            "epsg": 4326,
            "datetime": "2020-03-03T02:26:33.500000Z",
            "absolute_orbit": 12367,
            "shape": [4172, 215],
            "instruments": ["TROPOMI"],
            "processing_mode": "OFFL",
            "product_type": "L2__NP_BD7",
            "analysed_s5p_band": 7,
            "VIIRS_band": [7, 9, 11],
            "number_of_scaled_fov": 4
        }

        for k, v in expected.items():
            self.assertIn(k, s5p_props)
            self.assertEqual(s5p_props[k], v)
