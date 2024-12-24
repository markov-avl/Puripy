import re
from typing import override
from unittest import TestCase
from unittest.mock import patch

from puripy.context.decorator import DecoratableType
from puripy.context.metadata import ScanPackagesMetadata
from puripy.marker import scanpackages


class TestScanPackages(TestCase):

    @override
    def setUp(self):
        self.is_valid_decoratable_patcher = patch("puripy.marker.marker.is_valid_decoratable")
        self.append_metadata_patcher = patch("puripy.marker.marker.append_metadata")

        self.is_valid_decoratable_mock = self.is_valid_decoratable_patcher.start()
        self.append_metadata_mock = self.append_metadata_patcher.start()

        self.is_valid_decoratable_mock.return_value = True

    @override
    def tearDown(self):
        self.is_valid_decoratable_patcher.stop()
        self.append_metadata_patcher.stop()

    def test_no_args_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = ScanPackagesMetadata(include=set(), exclude=set())

        # act
        decorated_test_class = scanpackages()(test_class)

        # assert
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertIs(test_class, decorated_test_class)

    def test_include_only_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = ScanPackagesMetadata(include={"package1", "package2"}, exclude=set())

        # act
        decorated_test_class = scanpackages(include=["package1", "package2"])(test_class)

        # assert
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertEqual(test_class, decorated_test_class)

    def test_exclude_only_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = ScanPackagesMetadata(include=set(), exclude={"package3"})

        # act
        decorated_test_class = scanpackages(exclude="package3")(test_class)

        # assert
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertEqual(test_class, decorated_test_class)

    def test_include_and_exclude_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = ScanPackagesMetadata(include={"package1"}, exclude={"package3"})

        # act
        decorated_test_class = scanpackages(include="package1", exclude=["package3"])(test_class)

        # assert
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertEqual(test_class, decorated_test_class)

    def test_invalid_include_type_raises(self):
        # arrange
        test_class = type("TestClass", (), {})
        exception_message_regex = re.compile(r"Expected a string, an iterable of strings, or None")

        # act & assert
        # noinspection PyTypeChecker
        self.assertRaisesRegex(TypeError, exception_message_regex, lambda: scanpackages(include=123)(test_class))

    def test_invalid_exclude_type_raises(self):
        # arrange
        test_class = type("TestClass", (), {})
        exception_message_regex = re.compile(r"Expected a string, an iterable of strings, or None")

        # act & assert
        # noinspection PyTypeChecker
        self.assertRaisesRegex(TypeError, exception_message_regex, lambda: scanpackages(exclude=123)(test_class))

    def test_as_class_decorator(self):
        # arrange
        test_class = type("TestClass", (), {})

        # act
        scanpackages()(test_class)

        # assert
        self.is_valid_decoratable_mock.assert_called_once_with(
            test_class,
            [DecoratableType.CLASS]
        )
