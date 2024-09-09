from unittest import TestCase

from puripy.context.marker import bone


class TestBone(TestCase):
    class TestClass:
        pass

    def test_no_args_decoration(self):
        # act
        test_class = bone()(self.TestClass)

        # assert
        # TODO: assert inside __call__ calls
        self.assertEqual(self.TestClass, test_class)

    def test_no_args_uncalled_decoration(self):
        # act
        # noinspection PyTypeChecker
        test_class = bone(self.TestClass)

        # assert
        # TODO: assert inside __call__ calls
        self.assertEqual(self.TestClass, test_class)

    def test_pos_args_decoration(self):
        # act
        test_class = bone("name")(self.TestClass)

        # assert
        # TODO: assert inside __call__ calls
        # TODO: assert registration with default name
        self.assertEqual(self.TestClass, test_class)

    def test_kw_args_decoration(self):
        # act
        test_class = bone(name="name")(self.TestClass)

        # assert
        # TODO: assert inside __call__ calls
        # TODO: assert registration with name="name"
        self.assertEqual(self.TestClass, test_class)
