from sys import modules
from unittest import TestCase
from unittest.mock import patch, call

from puripy.property.parser import PropertyParser, JsonPropertyParser, YamlPropertyParser
from puripy.utils.scan_utils import find_containerized


class TestScanUtils(TestCase):

    def setUp(self):
        self.is_defined_in_any_patcher = patch("puripy.utils.scan_utils.is_defined_in_any")
        self.is_containerized_patcher = patch("puripy.utils.scan_utils.is_containerized")

        self.is_defined_in_any_mock = self.is_defined_in_any_patcher.start()
        self.is_containerized_mock = self.is_containerized_patcher.start()

    def tearDown(self):
        self.is_defined_in_any_patcher.stop()
        self.is_containerized_patcher.stop()

    def test_find_containerized_1(self):
        """
        Tests that the ``find_containerized`` function correctly finds and returns containerized types
        from the specified packages.
        """

        # arrange
        self.is_defined_in_any_mock.side_effect = lambda module_name, _: module_name.startswith("puripy.property")
        self.is_containerized_mock.side_effect = lambda m: getattr(m, "__name__", "").endswith("PropertyParser")

        # act
        result = find_containerized({"puripy"})

        # assert
        self.assertSetEqual(result, {PropertyParser, JsonPropertyParser, YamlPropertyParser})

    def test_find_containerized_2(self):
        """
        Tests that the ``find_containerized`` function returns an empty set
        when acceptable packages is an empty set.
        """

        # arrange
        self.is_defined_in_any_mock.return_value = False

        # act
        result = find_containerized(set())

        # assert
        self.is_defined_in_any_mock.assert_called()
        self.is_containerized_mock.assert_not_called()
        self.assertSetEqual(result, set())

    def test_find_containerized_3(self):
        """
        Tests that the ``find_containerized`` function checks all packages
        when no acceptable packages are specified.
        """

        # arrange
        self.is_containerized_mock.return_value = False
        member_calls = [call(member) for module in modules.values() for member in module.__dict__.values()]

        # act
        result = find_containerized()

        # assert
        self.is_defined_in_any_mock.assert_not_called()
        self.is_containerized_mock.assert_has_calls(member_calls, any_order=False)
        self.assertSetEqual(result, set())

    def test_find_containerized_4(self):
        """
        Tests that the ``find_containerized`` function returns an empty set
        when no containerized types are found.
        """

        # arrange
        self.is_defined_in_any_mock.return_value = True
        self.is_containerized_mock.return_value = False

        # act
        result = find_containerized({"puripy"})

        # assert
        self.is_defined_in_any_mock.assert_called()
        self.is_containerized_mock.assert_called()
        self.assertSetEqual(result, set())
