from unittest import TestCase

from puripy.utils import ScanUtils
from tests.testpackage import TestApplication
from tests.testpackage.included import TestParticle, TestProperties


class TestScanUtils(TestCase):

    def test_find_particles(self):
        # Act
        particles = ScanUtils.find_particles(TestApplication)

        # Assert
        self.assertSetEqual({TestParticle, TestProperties}, particles)
