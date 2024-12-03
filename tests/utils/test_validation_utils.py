from unittest import TestCase

from puripy.context.decorator import DecoratableType
from puripy.utils.validation_utils import is_valid_decoratable


class TestValidationUtils(TestCase):

    def test_is_valid_decoratable_1(self):
        """
        Tests that the ``is_valid_decoratable`` function returns ``True`` for a class
        if class decoratable types are valid.
        """

        # arrange
        class Decoratable: pass

        # act
        result = is_valid_decoratable(Decoratable, [DecoratableType.CLASS])

        # assert
        self.assertTrue(result)

    def test_is_valid_decoratable_2(self):
        """
        Tests that the ``is_valid_decoratable`` function returns ``True`` for a function
        if function decoratable types are valid.
        """

        # arrange
        def decoratable(): pass

        # act
        result = is_valid_decoratable(decoratable, [DecoratableType.FUNCTION])

        # assert
        self.assertTrue(result)

    def test_is_valid_decoratable_3(self):
        """
        Tests that the ``is_valid_decoratable`` function returns ``False``
        for an invalid decoratable type.
        """

        # arrange
        class Decoratable: pass

        def decoratable(): pass

        # act
        result_1 = is_valid_decoratable(Decoratable, [DecoratableType.FUNCTION])
        result_2 = is_valid_decoratable(decoratable, [DecoratableType.CLASS])

        # assert
        self.assertFalse(result_1)
        self.assertFalse(result_2)

    def test_is_valid_decoratable_4(self):
        """
        Tests that the ``is_valid_decoratable`` function returns ``True``
        for a class and function if both are valid.
        """

        # arrange
        class Decoratable: pass

        def decoratable(): pass

        # act
        result_1 = is_valid_decoratable(Decoratable, [DecoratableType.CLASS, DecoratableType.FUNCTION])
        result_2 = is_valid_decoratable(decoratable, [DecoratableType.CLASS, DecoratableType.FUNCTION])

        # assert
        self.assertTrue(result_1)
        self.assertTrue(result_2)

    def test_is_valid_decoratable_5(self):
        """
        Tests that the ``is_valid_decoratable`` function returns ``False``
        for a class and function if no types are valid.
        """

        # arrange
        class Decoratable: pass

        def decoratable(): pass

        # act
        result_1 = is_valid_decoratable(Decoratable, [])
        result_2 = is_valid_decoratable(decoratable, [])

        # assert
        self.assertFalse(result_1)
        self.assertFalse(result_2)
