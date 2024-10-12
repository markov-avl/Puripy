from unittest import TestCase

from puripy.context.metadata import AfterinitMetadata


class TestAfterinitMetadata(TestCase):

    def test_constructor(self):
        """
        Tests the constructor returns a new instance every single time
        """

        # act
        first = AfterinitMetadata()
        second = AfterinitMetadata()

        # assert
        self.assertNotEqual(first, second)

    def test_instance(self):
        """
        Tests the instance method returns the same instance every single time
        """

        # act
        first = AfterinitMetadata.instance()
        second = AfterinitMetadata.instance()

        # assert
        self.assertEqual(first, second)

    def test_constructor_after_instance(self):
        """
        Tests the constructor returns a new instance after creating a singleton
        """

        # act
        instanced = AfterinitMetadata.instance()
        constructed_first = AfterinitMetadata()
        constructed_second = AfterinitMetadata()

        # assert
        self.assertNotEqual(instanced, constructed_first)
        self.assertNotEqual(instanced, constructed_second)
        self.assertNotEqual(constructed_first, constructed_second)

    # TODO: disabled because the test only works in the newly created context
    def disabled_test_instance_after_constructor(self):
        """
        Tests the instance method returns the same instance after using the constructor
        """

        # act
        constructed = AfterinitMetadata()
        instanced = AfterinitMetadata.instance()

        # assert
        self.assertEqual(constructed, instanced)
