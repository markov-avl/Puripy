from unittest import TestCase

from puripy.particle import Builder
from puripy.utils import ScanUtils


class TestClassScanner(TestCase):

    def disabled_test_scan(self):
        ScanUtils.scan_particles(Builder)
