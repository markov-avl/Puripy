import inspect
from unittest import TestCase

from puripy.utils.reflection_utils import params_of, return_type_of, defined_name, has_string_annotations, is_hashable


class TestReflectionUtils(TestCase):

    def test_params_of_1(self):
        """
        Tests that the ``params_of`` function correctly returns the parameters of a callable.
        """

        # arrange
        # pylint: disable=unused-argument,keyword-arg-before-vararg
        # noinspection PyUnusedLocal
        def test_function(param1, param2: str, param3=None, param4: int = 1, *args, **kwargs): ...

        # act
        result = params_of(test_function)

        # assert
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0].name, "param1")
        self.assertEqual(result[0].default, inspect.Parameter.empty)
        self.assertEqual(result[0].annotation, inspect.Parameter.empty)
        self.assertEqual(result[0].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(result[1].name, "param2")
        self.assertEqual(result[1].default, inspect.Parameter.empty)
        self.assertEqual(result[1].annotation, str)
        self.assertEqual(result[1].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(result[2].name, "param3")
        self.assertEqual(result[2].default, None)
        self.assertEqual(result[2].annotation, inspect.Parameter.empty)
        self.assertEqual(result[2].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(result[3].name, "param4")
        self.assertEqual(result[3].default, 1)
        self.assertEqual(result[3].annotation, int)
        self.assertEqual(result[3].kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        self.assertEqual(result[4].name, "args")
        self.assertEqual(result[4].default, inspect.Parameter.empty)
        self.assertEqual(result[4].annotation, inspect.Parameter.empty)
        self.assertEqual(result[4].kind, inspect.Parameter.VAR_POSITIONAL)
        self.assertEqual(result[5].name, "kwargs")
        self.assertEqual(result[5].default, inspect.Parameter.empty)
        self.assertEqual(result[5].annotation, inspect.Parameter.empty)
        self.assertEqual(result[5].kind, inspect.Parameter.VAR_KEYWORD)

    def test_params_of_2(self):
        """
        Tests that the ``params_of`` function correctly returns the parameters of a callable with no parameters.
        """

        # arrange
        def test_function(): pass

        # act
        result = params_of(test_function)

        # assert
        self.assertEqual(len(result), 0)

    def test_params_of_3(self):
        """
        Tests that the ``params_of`` function correctly returns the parameters of __init__ method
        if class provided.
        """

        # arrange
        class TestClass:
            # pylint: disable=unused-argument
            # noinspection PyUnusedLocal
            def __init__(self, param1): ...

        # act
        result = params_of(TestClass)

        # assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "param1")

    def test_params_of_4(self):
        """
        Tests that the ``params_of`` function correctly returns the parameters of __call__ method
        if instance of class provided.
        """

        # arrange
        class TestClass:
            # noinspection PyUnusedLocal
            def __call__(self, param1): ...

        test_instance = TestClass()

        # act
        result = params_of(test_instance)

        # assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "param1")

    def test_return_type_of_1(self):
        """
        Tests that `return_type_of` returns the correct return annotation of a function.
        """

        # arrange
        def test_function() -> int: ...

        # act
        result = return_type_of(test_function)

        # assert
        self.assertEqual(result, int)

    def test_return_type_of_2(self):
        """
        Tests that `return_type_of` returns the object itself if it is a class.
        """

        # arrange
        class TestClass: ...

        # act
        result = return_type_of(TestClass)

        # assert
        self.assertEqual(result, TestClass)

    def test_return_type_of_3(self):
        """
        Tests that `return_type_of` returns `inspect.Parameter.empty` if no return annotation is provided.
        """

        # arrange
        def test_function(): ...

        # act
        result = return_type_of(test_function)

        # assert
        self.assertEqual(result, inspect.Parameter.empty)

    def test_return_type_of_4(self):
        """
        Tests that `return_type_of` correctly handles callable objects.
        """

        # arrange
        class TestClass:
            def __call__(self) -> str: ...

        test_instance = TestClass()

        # act
        result = return_type_of(test_instance)

        # assert
        self.assertEqual(result, str)

    def test_defined_name_1(self):
        """
        Tests that `defined_name` returns the name of a class.
        """

        # arrange
        class TestClass: ...

        # act
        result = defined_name(TestClass)

        # assert
        self.assertEqual(result, "TestClass")

    def test_defined_name_2(self):
        """
        Tests that `defined_name` returns the name of a function.
        """

        # arrange
        def test_function(): ...

        # act
        result = defined_name(test_function)

        # assert
        self.assertEqual(result, "test_function")

    def test_defined_name_3(self):
        """
        Tests that `defined_name` returns the qualified name of a method.
        """

        # arrange
        class TestClass:
            def method(self): ...

        # act
        result = defined_name(TestClass.method)

        # assert
        self.assertEqual(result, "method")

    def test_defined_name_4(self):
        """
        Tests that `defined_name` returns the class name of an instance.
        """

        # arrange
        class TestClass: ...

        test_instance = TestClass()

        # act
        result = defined_name(test_instance)

        # assert
        self.assertEqual(result, "TestClass")

    def test_has_string_annotations_1(self):
        """
        Tests that the ``has_string_annotations`` function returns ``True``
        when the provided callable has string annotations.
        """

        # arrange
        # pylint: disable=unused-argument
        # noinspection PyUnusedLocal
        def test_function(param: "str"): ...

        # act
        result = has_string_annotations(test_function)

        # assert
        self.assertTrue(result)

    def test_has_string_annotations_2(self):
        """
        Tests that the ``has_string_annotations`` function returns ``False``
        when the provided callable does not have string annotations.
        """

        # arrange
        # pylint: disable=unused-argument
        # noinspection PyUnusedLocal
        def test_function(param: int): ...

        # act
        result = has_string_annotations(test_function)

        # assert
        self.assertFalse(result)

    def test_has_string_annotations_3(self):
        """
        Tests that the ``has_string_annotations`` function returns ``False``
        when the provided callable has no parameters.
        """

        # arrange
        def test_function(): ...

        # act
        result = has_string_annotations(test_function)

        # assert
        self.assertFalse(result)

    def test_has_string_annotations_4(self):
        """
        Tests that the ``has_string_annotations`` function returns ``True``
        when the provided callable has a mix of string and non-string annotations.
        """

        # arrange
        # pylint: disable=unused-argument
        # noinspection PyUnusedLocal
        def test_function(param1: int, param2: "str"): ...

        # act
        result = has_string_annotations(test_function)

        # assert
        self.assertTrue(result)

    def test_is_hashable_1(self):
        """
        Tests that ``is_hashable`` returns True for hashable types.
        """

        # arrange
        obj = 42  # Integer is hashable

        # act
        result = is_hashable(obj)

        # assert
        self.assertTrue(result)

    def test_is_hashable_2(self):
        """
        Tests that ``is_hashable`` returns False for unhashable types.
        """

        # arrange
        obj = [1, 2, 3]

        # act
        result = is_hashable(obj)

        # assert
        self.assertFalse(result)
