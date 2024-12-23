import re
from typing import override
from unittest import TestCase
from unittest.mock import patch, ANY

from puripy.marker import beforedel
from puripy.context.metadata import BeforeDelMetadata


class TestBeforedel(TestCase):

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
        def test_function(): ...

        # act
        marker = beforedel()
        wrapped_test_function = marker(test_function)

        # assert
        self.append_metadata_mock.assert_called_once_with(test_function, ANY)
        self.assertEqual(BeforeDelMetadata, type(self.append_metadata_mock.call_args[0][1]))
        self.assertEqual(beforedel, type(marker))
        self.assertIs(test_function, wrapped_test_function)

    def test_no_args_uncalled_decoration(self):
        # arrange
        def test_function(): ...

        # act
        # noinspection PyArgumentList
        wrapped_test_function = beforedel(test_function)

        # assert
        self.append_metadata_mock.assert_called_once_with(test_function, ANY)
        self.assertEqual(BeforeDelMetadata, type(self.append_metadata_mock.call_args[0][1]))
        self.assertIs(test_function, wrapped_test_function)

    def test_invalid_decoration(self):
        # arrange
        def test_function(): ...

        self.is_valid_decoratable_mock.return_value = False
        exception_message_regex = re.compile(r".* must be any of the following types: function")

        # act & assert
        # noinspection PyArgumentList
        self.assertRaisesRegex(RuntimeError, exception_message_regex, lambda: beforedel(test_function))
        self.is_valid_decoratable_mock.assert_called_once_with(test_function, ANY)
        self.append_metadata_mock.assert_not_called()
