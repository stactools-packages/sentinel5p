import unittest

import stactools.sentinel5p


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.sentinel5p.__version__)
