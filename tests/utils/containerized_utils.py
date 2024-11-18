from unittest import TestCase

from puripy.utils.containerized_utils import (get_name,
                                              has_incorrect_annotations,
                                              has_string_annotations,
                                              has_empty_annotations)


class TestScanUtils(TestCase):

    def test_get_name_provide_class(self):
        # arrange
        test_class = type("TestClass", (), {})

        # act
        name = get_name(test_class)

        # assert
        self.assertEqual(name, "test_class")

    def test_get_name_provide_instance(self):
        # arrange
        test_class = type("TestClass", (), {})
        test_instance = test_class()

        # act
        name = get_name(test_instance)

        # assert
        self.assertEqual(name, "test_class")

    def test_get_name_provide_name_cases(self):
        # arrange
        name_cases = {
            "PascalCasedName": "pascal_cased_name",
            "camelCasedName": "camel_cased_name",
            "snake_cased_name": "snake_cased_name",
            "_ProtectedName": "_protected_name",
            "__PrivateName": "__private_name",
            "Mixed_casedName": "mixed_cased_name"
        }

        for test_name, expect in name_cases.items():
            with self.subTest(test_name=test_name, expect=expect):
                test_class = type(test_name, (), {})

                # act
                name = get_name(test_class)

                # assert
                self.assertEqual(expect, name)

    def test_get_name_provide_own_name(self):
        # arrange
        test_class = type("TestClass", (), {})
        test_name = "test"

        # act
        name = get_name(test_class, test_name)

        # assert
        self.assertEqual(name, test_name)
