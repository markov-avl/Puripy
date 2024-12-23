from unittest import TestCase

from puripy.context.metadata import BeforeDelMetadata


class TestBeforedelMetadata(TestCase):

    def test_constructor(self):
        """
        Test the constructor returns a new instance every single time
        """

        # act
        first = BeforeDelMetadata()
        second = BeforeDelMetadata()

        # assert
        self.assertNotEqual(first, second)

    def test_instance(self):
        """
        Test the instance method returns the same instance every single time
        """

        # act
        first = BeforeDelMetadata.instance()
        second = BeforeDelMetadata.instance()

        # assert
        self.assertEqual(first, second)

    def test_constructor_after_instance(self):
        """
        Tests the constructor returns a new instance after creating a singleton
        """

        # act
        instanced = BeforeDelMetadata.instance()
        constructed_first = BeforeDelMetadata()
        constructed_second = BeforeDelMetadata()

        # assert
        self.assertNotEqual(instanced, constructed_first)
        self.assertNotEqual(instanced, constructed_second)
        self.assertNotEqual(constructed_first, constructed_second)

    # FIXME: disabled because the test only works in the newly created context
    def disabled_test_instance_after_constructor(self):
        """
        Tests the instance method returns the same instance after using the constructor
        """

        # act
        constructed = BeforeDelMetadata()
        instanced = BeforeDelMetadata.instance()

        # assert
        self.assertEqual(constructed, instanced)
