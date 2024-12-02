import inspect
from unittest import TestCase

from puripy.utils.reflection_utils import is_defined_in_any, params_of


class TestReflectionUtils(TestCase):

    def test_is_defined_in_any_1(self):
        """
        Tests that the ``is_defined_in_any`` function returns ``True``
        when the module name starts with any of the packages.
        """

        # arrange
        module_name = "package1.subpackage.module"
        packages = {"package1", "package2"}

        # act
        result = is_defined_in_any(module_name, packages)

        # assert
        self.assertTrue(result)

    def test_is_defined_in_any_2(self):
        """
        Tests that the ``is_defined_in_any`` function returns ``False``
        when the module name does not start with any of the packages.
        """

        # arrange
        module_name = "package3.subpackage.module"
        packages = {"package1", "package2"}

        # act
        result = is_defined_in_any(module_name, packages)

        # assert
        self.assertFalse(result)

    def test_params_of_1(self):
        """
        Tests that the ``params_of`` function correctly returns the parameters of a callable.
        """

        # arrange
        # pylint: disable=unused-argument,keyword-arg-before-vararg
        def test_function(param1, param2: str, param3=None, param4: int = 1, *args, **kwargs): pass

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
            def __call__(self, param1): ...

        test_instance = TestClass()

        # act
        result = params_of(test_instance)

        # assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "param1")
