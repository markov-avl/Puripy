from unittest import TestCase

from puripy.utils import ScanUtils
from tests.testpackage import Application


class TestClassScanner(TestCase):

    def test_scan(self):
        print(ScanUtils.scan_particles(Application))
