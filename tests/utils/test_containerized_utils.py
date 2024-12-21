from unittest import TestCase

from puripy.utils.containerized_utils import get_name


# pylint: disable=unused-argument
class TestContainerizedUtils(TestCase):

    def test_get_name_1(self):
        """
        Tests that the ``get_name`` function correctly returns the class name in snake_case format
        when provided with a class object.
        """

        # arrange
        test_class = type("TestClass", (), {})

        # act
        name = get_name(test_class)

        # assert
        self.assertEqual(name, "test_class")

    def test_get_name_2(self):
        """
        Tests that the ``get_name`` function correctly returns the class name in snake_case format
        when provided with an instance of a class.
        """

        # arrange
        test_class = type("TestClass", (), {})
        test_instance = test_class()

        # act
        name = get_name(test_instance)

        # assert
        self.assertEqual(name, "test_class")

    def test_get_name_3(self):
        """
        Tests the ``get_name`` function with various naming conventions (PascalCase, camelCase, snake_case,
        protected, and private names) to ensure it correctly converts them to snake_case format.
        """

        # arrange
        test_cases = {
            "PascalCasedName": "pascal_cased_name",
            "camelCasedName": "camel_cased_name",
            "snake_cased_name": "snake_cased_name",
            "_ProtectedName": "_protected_name",
            "__PrivateName": "__private_name",
            "Mixed_casedName": "mixed_cased_name"
        }

        for test_name, expected_convention in test_cases.items():
            with self.subTest(test_name=test_name, expected_convention=expected_convention):
                test_class = type(test_name, (), {})

                # act
                name = get_name(test_class)

                # assert
                self.assertEqual(expected_convention, name)

    def test_get_name_4(self):
        """
        Tests that the ``get_name`` function returns a custom name provided as an argument
        instead of the default class name when both a class and a custom name are given.
        """

        # arrange
        test_class = type("TestClass", (), {})
        test_name = "test"

        # act
        name = get_name(test_class, test_name)

        # assert
        self.assertEqual(name, test_name)
