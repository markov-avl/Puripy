import re
from unittest import TestCase

from puripy.context.decoration import DecoratableType
from puripy.context.marker import Marker
from puripy.context.metadata import Metadata


class TestContextMarker(TestCase):
    class TestClass:
        pass

    class NoArgsMarker(Marker):

        def __init__(self):
            super().__init__([DecoratableType.CLASS])

        def _to_metadata(self) -> Metadata: ...

    class ArguedMarker(Marker):

        def __init__(self, arg: str):
            super().__init__([DecoratableType.CLASS])
            self.arg = arg

        def _to_metadata(self) -> Metadata: ...

    class DefaultArguedMarker(Marker):

        def __init__(self, arg: str = "default value"):
            super().__init__([DecoratableType.CLASS])
            self.arg = arg

        def _to_metadata(self) -> Metadata: ...

    def test_no_args_init(self):
        # act
        marker = self.NoArgsMarker()
        test_class = marker(self.TestClass)

        # assert
        self.assertEqual(self.NoArgsMarker, type(marker))
        self.assertEqual(self.TestClass, test_class)

    def test_no_args_init_with_callable(self):
        # act
        # noinspection PyArgumentList
        test_class = self.NoArgsMarker(self.TestClass)

        # assert
        self.assertEqual(self.TestClass, test_class)

    def test_argued_init_with_pos_arg(self):
        # arrange
        exception_message_regex = re.compile(r".*missing 1 required positional argument.*")

        # act & assert
        self.assertRaisesRegex(TypeError, exception_message_regex, lambda: self.ArguedMarker("value"))

    def test_argued_init_with_kw_arg(self):
        # act
        marker = self.ArguedMarker(arg="value")
        test_class = marker(self.TestClass)

        # assert
        self.assertEqual(self.ArguedMarker, type(marker))
        self.assertEqual(self.TestClass, test_class)
        self.assertEqual("value", marker.arg)

    def test_argued_init_with_callable(self):
        # arrange
        exception_message_regex = re.compile(r".*missing 1 required positional argument.*")

        # act & assert
        # noinspection PyTypeChecker
        self.assertRaisesRegex(TypeError, exception_message_regex, lambda: self.ArguedMarker(self.TestClass))

    def test_default_argued_init_with_pos_arg(self):
        # act
        marker = self.DefaultArguedMarker()
        test_class = marker(self.TestClass)

        # assert
        self.assertEqual(self.DefaultArguedMarker, type(marker))
        self.assertEqual(self.TestClass, test_class)
        self.assertEqual(marker.arg, "default value")

    def test_default_argued_init_with_kw_arg(self):
        # act
        marker = self.DefaultArguedMarker(arg="value")
        test_class = marker(self.TestClass)

        # assert
        self.assertEqual(self.DefaultArguedMarker, type(marker))
        self.assertEqual(self.TestClass, test_class)
        self.assertEqual("value", marker.arg)

    def test_default_argued_init_with_callable(self):
        # act
        # noinspection PyTypeChecker
        test_class = self.DefaultArguedMarker(self.TestClass)

        # assert
        self.assertEqual(self.TestClass, test_class)
