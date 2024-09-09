from unittest import TestCase

from puripy.context.metadata import AfterinitMetadata


class TestAfterinitMetadata(TestCase):

    def test_constructor(self):
        # act
        first = AfterinitMetadata()
        second = AfterinitMetadata()

        # assert
        self.assertNotEqual(first, second)

    def test_instance(self):
        # act
        first = AfterinitMetadata.instance()
        second = AfterinitMetadata.instance()

        # assert
        self.assertEqual(first, second)
