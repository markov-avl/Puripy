from unittest import TestCase
from unittest.mock import patch, MagicMock, ANY

from puripy.context.marker import afterinit
from puripy.context.metadata import AfterinitMetadata
from tests.patch_mocks import METADATA_UTILS_APPEND_METADATA


class TestAfterinit(TestCase):
    @staticmethod
    def function():
        pass

    @patch(METADATA_UTILS_APPEND_METADATA)
    def test_no_args_decoration(self, append_metadata_mock: MagicMock):
        # act
        marker = afterinit()
        # noinspection PyTypeChecker
        test_function = marker(self.function)

        # assert
        append_metadata_mock.assert_called_once_with(self.function, ANY)
        self.assertEqual(AfterinitMetadata, type(append_metadata_mock.call_args[0][1]))
        self.assertEqual(self.function, test_function)
        self.assertEqual(afterinit, type(marker))

    @patch(METADATA_UTILS_APPEND_METADATA)
    def test_no_args_uncalled_decoration(self, append_metadata_mock: MagicMock):
        # act
        test_function = afterinit(self.function)

        # assert
        append_metadata_mock.assert_called_once_with(self.function, ANY)
        self.assertEqual(AfterinitMetadata, type(append_metadata_mock.call_args[0][1]))
        self.assertEqual(self.function, test_function)
