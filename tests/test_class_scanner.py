from unittest import TestCase

from puripy.bone import Builder
from puripy.utils import ScanUtils


class TestClassScanner(TestCase):

    def test_scan(self):
        ScanUtils.scan_bones(Builder)
