from unittest import TestCase

from puripy.context.metadata import BeforedelMetadata


class TestBeforedelMetadataMetadata(TestCase):

    def test_constructor(self):
        # act
        first = BeforedelMetadata()
        second = BeforedelMetadata()

        # assert
        self.assertNotEqual(first, second)

    def test_instance(self):
        # act
        first = BeforedelMetadata.instance()
        second = BeforedelMetadata.instance()

        # assert
        self.assertEqual(first, second)
