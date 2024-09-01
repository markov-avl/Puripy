import re
from unittest import TestCase
from unittest.mock import patch, MagicMock

from puripy.context.annotation import ContextAnnotation


class TestContextAnnotation(TestCase):
    VALIDATE_DECORATABLE_PATH = "puripy.utility.ValidationUtility.validate_decoratable"

    class TestClass:
        pass

    class NoArgsAnnotation(ContextAnnotation):
        pass

    class ArguedAnnotation(ContextAnnotation):

        def __init__(self, arg: str):
            super().__init__()
            self.arg = arg

    class DefaultArguedAnnotation(ContextAnnotation):

        def __init__(self, arg: str = "default value"):
            super().__init__()
            self.arg = arg

    @patch(VALIDATE_DECORATABLE_PATH)
    def test_no_args_init(self, validate_decoratable_mock: MagicMock):
        # act
        annotation = self.NoArgsAnnotation()
        test_class = annotation(self.TestClass)

        # assert
        validate_decoratable_mock.assert_not_called()
        self.assertEqual(self.NoArgsAnnotation, type(annotation))
        self.assertEqual(self.TestClass, test_class)

    @patch(VALIDATE_DECORATABLE_PATH)
    def test_no_args_init_with_callable(self, validate_decoratable_mock: MagicMock):
        # act
        # noinspection PyArgumentList
        test_class = self.NoArgsAnnotation(self.TestClass)

        # assert
        validate_decoratable_mock.assert_called_once()
        self.assertEqual(self.TestClass, test_class)

    def test_argued_init_with_pos_arg(self):
        # arrange
        exception_message_regex = re.compile(r".*missing 1 required positional argument.*")

        # act & assert
        self.assertRaisesRegex(TypeError, exception_message_regex, lambda: self.ArguedAnnotation("value"))

    @patch(VALIDATE_DECORATABLE_PATH)
    def test_argued_init_with_kw_arg(self, validate_decoratable_mock: MagicMock):
        # act
        annotation = self.ArguedAnnotation(arg="value")
        test_class = annotation(self.TestClass)

        # assert
        validate_decoratable_mock.assert_not_called()
        self.assertEqual(self.ArguedAnnotation, type(annotation))
        self.assertEqual(self.TestClass, test_class)
        self.assertEqual("value", annotation.arg)

    def test_argued_init_with_callable(self):
        # arrange
        exception_message_regex = re.compile(r".*missing 1 required positional argument.*")

        # act & assert
        # noinspection PyTypeChecker
        self.assertRaisesRegex(TypeError, exception_message_regex, lambda: self.ArguedAnnotation(self.TestClass))

    @patch(VALIDATE_DECORATABLE_PATH)
    def test_default_argued_init_with_pos_arg(self, validate_decoratable_mock: MagicMock):
        # act
        annotation = self.DefaultArguedAnnotation()
        test_class = annotation(self.TestClass)

        # assert
        validate_decoratable_mock.assert_not_called()
        self.assertEqual(self.DefaultArguedAnnotation, type(annotation))
        self.assertEqual(self.TestClass, test_class)
        self.assertEqual(annotation.arg, "default value")

    @patch(VALIDATE_DECORATABLE_PATH)
    def test_default_argued_init_with_kw_arg(self, validate_decoratable_mock: MagicMock):
        # act
        annotation = self.ArguedAnnotation(arg="value")
        test_class = annotation(self.TestClass)

        # assert
        validate_decoratable_mock.assert_not_called()
        self.assertEqual(self.ArguedAnnotation, type(annotation))
        self.assertEqual(self.TestClass, test_class)
        self.assertEqual("value", annotation.arg)

    @patch(VALIDATE_DECORATABLE_PATH)
    def test_default_argued_init_with_callable(self, validate_decoratable_mock: MagicMock):
        # act
        # noinspection PyTypeChecker
        test_class = self.DefaultArguedAnnotation(self.TestClass)

        # assert
        validate_decoratable_mock.assert_called_once()
        self.assertEqual(self.TestClass, test_class)
