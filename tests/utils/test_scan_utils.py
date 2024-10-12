from unittest import TestCase

from puripy.utils import ScanUtils
from tests.testpackage.included import TestParticle, TestProperties


class TestScanUtils(TestCase):

    def test_find_containerized(self):
        # Act
        particles = ScanUtils.find_containerized({"tests.testpackage"})

        # Assert
        self.assertSetEqual({TestParticle, TestProperties}, particles)
