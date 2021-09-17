import os.path
from tempfile import TemporaryDirectory

import pystac
from pystac.utils import is_absolute_href
from stactools.testing import CliTestCase

from stactools.sentinel5p.commands import create_sentinel5p_command
from stactools.sentinel5p.constants import SENTINEL_TROPOMI_BANDS
from tests import test_data


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_sentinel5p_command]

    def test_create_aerai_item(self):
        item_id = str("S5P_OFFL_L2__AER_AI_"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010302_"
                      "20200306T032414")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__AER_AI_"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010302_"
                                          "20200306T032414.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [SENTINEL_TROPOMI_BANDS["Band 3"]["name"]]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_aerlh_item(self):
        item_id = str("S5P_OFFL_L2__AER_LH_"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010302_"
                      "20200306T053814")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__AER_LH_"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010302_"
                                          "20200306T053814.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [SENTINEL_TROPOMI_BANDS["Band 6"]["name"]]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_ch4_item(self):
        item_id = str("S5P_OFFL_L2__CH4____"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010302_"
                      "20200306T053811")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__CH4____"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010302_"
                                          "20200306T053811.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    SENTINEL_TROPOMI_BANDS["Band 6"]["name"],
                    SENTINEL_TROPOMI_BANDS["Band 7"]["name"],
                    SENTINEL_TROPOMI_BANDS["Band 8"]["name"]
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_cloud_item(self):
        item_id = str("S5P_OFFL_L2__CLOUD__"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010107_"
                      "20200306T032410")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__CLOUD__"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010107_"
                                          "20200306T032410.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = []

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_co_item(self):
        item_id = str("S5P_OFFL_L2__CO_____"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010302_"
                      "20200306T032410")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__CO_____"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010302_"
                                          "20200306T032410.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    SENTINEL_TROPOMI_BANDS["Band 7"]["name"],
                    SENTINEL_TROPOMI_BANDS["Band 8"]["name"]
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_hcho_item(self):
        item_id = str("S5P_OFFL_L2__HCHO___"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010107_"
                      "20200306T053811")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__HCHO___"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010107_"
                                          "20200306T053811.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = []

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_no2_item(self):
        item_id = str("S5P_OFFL_L2__NO2____"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010302_"
                      "20200306T053815")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__NO2____"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010302_"
                                          "20200306T053815.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    SENTINEL_TROPOMI_BANDS["Band 4"]["name"],
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_o3_item(self):
        item_id = str("S5P_OFFL_L2__O3_____"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010107_"
                      "20200306T053811")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__O3_____"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010107_"
                                          "20200306T053811.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = []

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_o3tcl_item(self):
        item_id = str("S5P_OFFL_L2__O3_TCL_"
                      "20200303T120623_20200309T125248_"
                      "12373_01_010108_"
                      "20200318T000106")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__O3_TCL_"
                                          "20200303T120623_20200309T125248_"
                                          "12373_01_010108_"
                                          "20200318T000106.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = []

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_so2_item(self):
        item_id = str("S5P_OFFL_L2__SO2____"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010107_"
                      "20200306T144427")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__SO2____"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010107_"
                                          "20200306T144427.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = []

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_npbd3_item(self):
        item_id = str("S5P_OFFL_L2__NP_BD3_"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010002_"
                      "20200306T032410")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__NP_BD3_"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010002_"
                                          "20200306T032410.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    SENTINEL_TROPOMI_BANDS["Band 3"]["name"],
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_npbd6_item(self):
        item_id = str("S5P_OFFL_L2__NP_BD6_"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010002_"
                      "20200306T032654")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__NP_BD6_"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010002_"
                                          "20200306T032654.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    SENTINEL_TROPOMI_BANDS["Band 6"]["name"],
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_npbd7_item(self):
        item_id = str("S5P_OFFL_L2__NP_BD7_"
                      "20200303T013547_20200303T031717_"
                      "12367_01_010002_"
                      "20200306T032925")
        granule_href = test_data.get_path("data-files/"
                                          "S5P_OFFL_L2__NP_BD7_"
                                          "20200303T013547_20200303T031717_"
                                          "12367_01_010002_"
                                          "20200306T032925.nc")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel5p", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    SENTINEL_TROPOMI_BANDS["Band 7"]["name"],
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b["name"]
                            for b in asset.extra_fields["band_fields"])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")
