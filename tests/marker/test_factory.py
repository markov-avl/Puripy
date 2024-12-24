import re
from typing import override
from unittest import TestCase
from unittest.mock import patch, ANY

from puripy.marker import factory
from puripy.context.metadata import FactoryMetadata


class TestFactory(TestCase):

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
        class TestClass: ...

        # act
        marker = factory()
        wrapped_test_function = marker(TestClass)

        # assert
        self.append_metadata_mock.assert_called_once_with(TestClass, ANY)
        self.assertEqual(FactoryMetadata, type(self.append_metadata_mock.call_args[0][1]))
        self.assertEqual(factory, type(marker))
        self.assertIs(TestClass, wrapped_test_function)

    def test_no_args_uncalled_decoration(self):
        # arrange
        class TestClass: ...

        # act
        # noinspection PyArgumentList
        wrapped_test_function = factory(TestClass)

        # assert
        self.append_metadata_mock.assert_called_once_with(TestClass, ANY)
        self.assertEqual(FactoryMetadata, type(self.append_metadata_mock.call_args[0][1]))
        self.assertIs(TestClass, wrapped_test_function)

    def test_invalid_decoration(self):
        # arrange
        class TestClass: ...

        self.is_valid_decoratable_mock.return_value = False
        exception_message_regex = re.compile(r".* must be any of the following types: class")

        # act & assert
        # noinspection PyArgumentList
        self.assertRaisesRegex(RuntimeError, exception_message_regex, lambda: factory(TestClass))
        self.is_valid_decoratable_mock.assert_called_once_with(TestClass, ANY)
        self.append_metadata_mock.assert_not_called()
