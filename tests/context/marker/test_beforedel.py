from unittest import TestCase
from unittest.mock import patch, MagicMock, ANY

from puripy.context.marker import beforedel
from puripy.context.metadata import BeforedelMetadata


class TestBeforedel(TestCase):
    @staticmethod
    def function(): ...

    @patch("puripy.context.marker.marker.append_metadata")
    def test_no_args_decoration(self, append_metadata_mock: MagicMock):
        # act
        marker = beforedel()
        # noinspection PyTypeChecker
        test_function = marker(self.function)

        # assert
        append_metadata_mock.assert_called_once_with(self.function, ANY)
        self.assertEqual(BeforedelMetadata, type(append_metadata_mock.call_args[0][1]))
        self.assertEqual(self.function, test_function)
        self.assertEqual(beforedel, type(marker))

    @patch("puripy.context.marker.marker.append_metadata")
    def test_no_args_uncalled_decoration(self, append_metadata_mock: MagicMock):
        # act
        test_function = beforedel(self.function)

        # assert
        append_metadata_mock.assert_called_once_with(self.function, ANY)
        self.assertEqual(BeforedelMetadata, type(append_metadata_mock.call_args[0][1]))
        self.assertEqual(self.function, test_function)
