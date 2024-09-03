from unittest import TestCase

from puripy.context.annotation import afterinit


class TestAfterinit(TestCase):
    @staticmethod
    def function():
        pass

    def test_no_args_decoration(self):
        # act
        # noinspection PyTypeChecker
        test_function = afterinit()(self.function)

        # assert
        # TODO: assert inside __call__ calls
        self.assertEqual(self.function, test_function)

    def test_no_args_uncalled_decoration(self):
        # act
        test_function = afterinit(self.function)

        # assert
        # TODO: assert inside __call__ calls
        self.assertEqual(self.function, test_function)
