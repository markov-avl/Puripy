from typing import override
from unittest import TestCase
from unittest.mock import patch

from puripy.context.property.parser import PropertyParser, JsonPropertyParser, YamlPropertyParser
from puripy.utils.scan_utils import (find_objects,
                                     find_objects_in_packages,
                                     find_containerized,
                                     find_factories,
                                     is_defined_in_any)


class TestScanUtils(TestCase):

    @override
    def setUp(self):
        self.is_containerized_patcher = patch("puripy.utils.scan_utils.is_containerized")
        self.is_factory_patcher = patch("puripy.utils.scan_utils.is_factory")
        self.is_hashable_patcher = patch("puripy.utils.scan_utils.is_hashable")

        self.is_containerized_mock = self.is_containerized_patcher.start()
        self.is_factory_mock = self.is_factory_patcher.start()
        self.is_hashable_mock = self.is_hashable_patcher.start()

    @override
    def tearDown(self):
        self.is_containerized_patcher.stop()
        self.is_factory_patcher.stop()
        self.is_hashable_patcher.stop()

    def test_find_objects_1(self):
        """
        Tests that the ``find_objects`` function finds objects based on the provided filters.
        """

        # act
        result = find_objects(
            lambda m: m.startswith("puripy.context.property"),
            lambda obj: getattr(obj, "__name__", "").endswith("Parser")
        )

        # assert
        self.assertSetEqual(result, {PropertyParser, JsonPropertyParser, YamlPropertyParser})

    def test_find_objects_2(self):
        """
        Tests that the ``find_objects`` function returns an empty set when filters exclude all objects.
        """

        # act
        result = find_objects(lambda m: False, lambda obj: True)

        # assert
        self.assertSetEqual(result, set())

    def test_find_objects_in_packages_1(self):
        """
        Tests that the ``find_objects_in_packages`` function returns objects from specific packages.
        """

        # arrange
        self.is_hashable_mock.side_effect = lambda obj: True
        self.is_containerized_mock.side_effect = lambda obj: getattr(obj, "__name__", "").endswith("Parser")

        # act
        result = find_objects_in_packages(self.is_containerized_mock, {"puripy.context.property"})

        # assert
        self.assertSetEqual(result, {PropertyParser, JsonPropertyParser, YamlPropertyParser})

    def test_find_objects_in_packages_2(self):
        """
        Tests that the ``find_objects_in_packages`` function excludes objects from specific packages.
        """

        # act
        result = find_objects_in_packages(lambda obj: True, {"puripy.context.property"}, {"puripy.context.property"})

        # assert
        self.assertSetEqual(result, set())

    def test_find_objects_in_packages_3(self):
        """
        Tests that the ``find_objects_in_packages`` function returns an empty set when no packages are included.
        """

        # act
        result = find_objects_in_packages(lambda obj: True, set())

        # assert
        self.assertSetEqual(result, set())

    def test_find_objects_in_packages_4(self):
        """
        Tests that the ``find_objects_in_packages`` function checks all modules when no packages are provided.
        """

        # arrange
        self.is_hashable_mock.side_effect = lambda obj: isinstance(getattr(obj, "__name__", ""), str)

        # act
        result = find_objects_in_packages(lambda obj: getattr(obj, "__name__", "").endswith("int"))

        # assert
        self.assertTrue(int in result)

    def test_find_containerized_1(self):
        """
        Tests that the ``find_containerized`` function uses the ``is_containerized`` filter.
        """

        # arrange
        self.is_hashable_mock.return_value = True
        self.is_containerized_mock.side_effect = lambda obj: getattr(obj, "__name__", "").endswith("Parser")

        # act
        result = find_containerized({"puripy.context.property"})

        # assert
        self.is_containerized_mock.assert_called()
        self.assertSetEqual(result, {PropertyParser, JsonPropertyParser, YamlPropertyParser})

    def test_find_factories_1(self):
        """
        Tests that the ``find_factories`` function uses the ``is_factory`` filter.
        """

        # arrange
        self.is_hashable_mock.return_value = True
        self.is_factory_mock.side_effect = lambda obj: getattr(obj, "__name__", "").endswith("Parser")

        # act
        result = find_factories({"puripy.context.property"})

        # assert
        self.is_factory_mock.assert_called()
        self.assertSetEqual(result, {PropertyParser, JsonPropertyParser, YamlPropertyParser})

    def test_is_defined_in_any_1(self):
        """
        Tests that the ``is_defined_in_any`` function returns ``True``
        when the module name starts with any of the packages.
        """

        # arrange
        module_name = "package1.subpackage.module"
        packages = {"package1", "package2"}

        # act
        result = is_defined_in_any(module_name, packages)

        # assert
        self.assertTrue(result)

    def test_is_defined_in_any_2(self):
        """
        Tests that the ``is_defined_in_any`` function returns ``False``
        when the module name does not start with any of the packages.
        """

        # arrange
        module_name = "package3.subpackage.module"
        packages = {"package1", "package2"}

        # act
        result = is_defined_in_any(module_name, packages)

        # assert
        self.assertFalse(result)

    def test_is_defined_in_any_3(self):
        """
        Tests that the ``is_defined_in_any`` function returns ``False`` when the packages set is empty.
        """

        # arrange
        module_name = "package3.subpackage.module"
        packages = set()

        # act
        result = is_defined_in_any(module_name, packages)

        # assert
        self.assertFalse(result)
