import re
from unittest import TestCase
from unittest.mock import patch, MagicMock

from puripy.context.marker import ContextMarker
from puripy.context.metadata import Metadata
from tests.patch_mocks import VALIDATION_UTILS_VALIDATE_DECORATABLE


class TestContextMarker(TestCase):
    class TestClass:
        pass

    class NoArgsMarker(ContextMarker):

        def _to_metadata(self) -> Metadata: ...

    class ArguedMarker(ContextMarker):

        def __init__(self, arg: str):
            super().__init__()
            self.arg = arg

        def _to_metadata(self) -> Metadata: ...

    class DefaultArguedMarker(ContextMarker):

        def __init__(self, arg: str = "default value"):
            super().__init__()
            self.arg = arg

        def _to_metadata(self) -> Metadata: ...

    @patch(VALIDATION_UTILS_VALIDATE_DECORATABLE)
    def test_no_args_init(self, validate_decoratable_mock: MagicMock):
        # act
        marker = self.NoArgsMarker()
        test_class = marker(self.TestClass)

        # assert
        validate_decoratable_mock.assert_not_called()
        self.assertEqual(self.NoArgsMarker, type(marker))
        self.assertEqual(self.TestClass, test_class)

    @patch(VALIDATION_UTILS_VALIDATE_DECORATABLE)
    def test_no_args_init_with_callable(self, validate_decoratable_mock: MagicMock):
        # act
        # noinspection PyArgumentList
        test_class = self.NoArgsMarker(self.TestClass)

        # assert
        validate_decoratable_mock.assert_called_once()
        self.assertEqual(self.TestClass, test_class)

    def test_argued_init_with_pos_arg(self):
        # arrange
        exception_message_regex = re.compile(r".*missing 1 required positional argument.*")

        # act & assert
        self.assertRaisesRegex(TypeError, exception_message_regex, lambda: self.ArguedMarker("value"))

    @patch(VALIDATION_UTILS_VALIDATE_DECORATABLE)
    def test_argued_init_with_kw_arg(self, validate_decoratable_mock: MagicMock):
        # act
        marker = self.ArguedMarker(arg="value")
        test_class = marker(self.TestClass)

        # assert
        validate_decoratable_mock.assert_not_called()
        self.assertEqual(self.ArguedMarker, type(marker))
        self.assertEqual(self.TestClass, test_class)
        self.assertEqual("value", marker.arg)

    def test_argued_init_with_callable(self):
        # arrange
        exception_message_regex = re.compile(r".*missing 1 required positional argument.*")

        # act & assert
        # noinspection PyTypeChecker
        self.assertRaisesRegex(TypeError, exception_message_regex, lambda: self.ArguedMarker(self.TestClass))

    @patch(VALIDATION_UTILS_VALIDATE_DECORATABLE)
    def test_default_argued_init_with_pos_arg(self, validate_decoratable_mock: MagicMock):
        # act
        marker = self.DefaultArguedMarker()
        test_class = marker(self.TestClass)

        # assert
        validate_decoratable_mock.assert_not_called()
        self.assertEqual(self.DefaultArguedMarker, type(marker))
        self.assertEqual(self.TestClass, test_class)
        self.assertEqual(marker.arg, "default value")

    @patch(VALIDATION_UTILS_VALIDATE_DECORATABLE)
    def test_default_argued_init_with_kw_arg(self, validate_decoratable_mock: MagicMock):
        # act
        marker = self.DefaultArguedMarker(arg="value")
        test_class = marker(self.TestClass)

        # assert
        validate_decoratable_mock.assert_not_called()
        self.assertEqual(self.DefaultArguedMarker, type(marker))
        self.assertEqual(self.TestClass, test_class)
        self.assertEqual("value", marker.arg)

    @patch(VALIDATION_UTILS_VALIDATE_DECORATABLE)
    def test_default_argued_init_with_callable(self, validate_decoratable_mock: MagicMock):
        # act
        # noinspection PyTypeChecker
        test_class = self.DefaultArguedMarker(self.TestClass)

        # assert
        validate_decoratable_mock.assert_called_once()
        self.assertEqual(self.TestClass, test_class)
