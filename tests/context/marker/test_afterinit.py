from unittest import TestCase
from unittest.mock import patch, MagicMock, ANY

from puripy.context.marker import afterinit
from puripy.context.metadata import AfterinitMetadata


class TestAfterinit(TestCase):
    @staticmethod
    def function(): ...

    @patch('puripy.context.marker.context_marker.append_metadata')
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

    @patch('puripy.context.marker.context_marker.append_metadata')
    def test_no_args_uncalled_decoration(self, append_metadata_mock: MagicMock):
        # act
        test_function = afterinit(self.function)

        # assert
        append_metadata_mock.assert_called_once_with(self.function, ANY)
        self.assertEqual(AfterinitMetadata, type(append_metadata_mock.call_args[0][1]))
        self.assertEqual(self.function, test_function)
