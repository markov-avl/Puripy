from unittest import TestCase

from puripy.context.annotation import component


class TestComponent(TestCase):
    class TestClass:
        pass

    def test_no_args_decoration(self):
        # act
        test_class = component()(self.TestClass)

        # assert
        # TODO: assert inside __call__ calls
        self.assertEqual(self.TestClass, test_class)

    def test_no_args_parentless_decoration(self):
        # act
        # noinspection PyTypeChecker
        test_class = component(self.TestClass)

        # assert
        # TODO: assert inside __call__ calls
        self.assertEqual(self.TestClass, test_class)

    def test_pos_args_decoration(self):
        # act
        test_class = component("name")(self.TestClass)

        # assert
        # TODO: assert inside __call__ calls
        # TODO: assert registration with default name
        self.assertEqual(self.TestClass, test_class)

    def test_kw_args_decoration(self):
        # act
        test_class = component(name="name")(self.TestClass)

        # assert
        # TODO: assert inside __call__ calls
        # TODO: assert registration with name="name"
        self.assertEqual(self.TestClass, test_class)