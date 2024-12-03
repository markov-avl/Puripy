from unittest import TestCase

from puripy.context.metadata import (AfterinitMetadata,
                                     BeforedelMetadata,
                                     ConfiguratorMetadata,
                                     ParticleMetadata,
                                     PropertiesMetadata)
from puripy.utils.metadata_utils import (ATTRIBUTE_NAME,
                                         append_metadata,
                                         find_metadata,
                                         find_metadata_of_type,
                                         get_exactly_one_metadata_of_type,
                                         has_metadata_of_type,
                                         is_afterinit,
                                         is_beforedel,
                                         is_configurator,
                                         is_particle,
                                         is_properties,
                                         is_containerized)


class TestMetadataUtils(TestCase):

    def test_append_metadata_1(self):
        """
        Tests that the ``append_metadata`` function correctly appends metadata to an object.
        """

        # arrange
        obj = type("TestClass", (), {})
        metadata = AfterinitMetadata()

        # act
        append_metadata(obj, metadata)

        # assert
        self.assertEqual([metadata], getattr(obj, ATTRIBUTE_NAME))

    def test_append_metadata_2(self):
        """
        Tests that the ``append_metadata`` function correctly appends metadata to an object
        even if the object already has metadata.
        """

        # arrange
        obj = type("TestClass", (), {})
        metadata1 = AfterinitMetadata()
        metadata2 = BeforedelMetadata()

        # act
        append_metadata(obj, metadata1)
        append_metadata(obj, metadata2)

        # assert
        self.assertEqual([metadata1, metadata2], getattr(obj, ATTRIBUTE_NAME))

    def test_find_metadata_1(self):
        """
        Tests that the ``find_metadata`` function correctly retrieves metadata from an object.
        """

        # arrange
        obj = type("TestClass", (), {})
        metadata1 = AfterinitMetadata()
        metadata2 = BeforedelMetadata()
        setattr(obj, ATTRIBUTE_NAME, [metadata1, metadata2])

        # act
        result = find_metadata(obj)

        # assert
        self.assertEqual([metadata1, metadata2], result)

    def test_find_metadata_2(self):
        """
        Tests that the ``find_metadata`` function correctly retrieves metadata from an object
        even if there are no metadata.
        """

        # arrange
        obj = type("TestClass", (), {})

        # act
        result = find_metadata(obj)

        # assert
        self.assertEqual([], result)

    def test_find_metadata_of_type_1(self):
        """
        Tests that the ``find_metadata_of_type`` function correctly retrieves metadata
        of a specific type from an object.
        """

        # arrange
        obj = type("TestClass", (), {})
        metadata1 = AfterinitMetadata()
        metadata2 = BeforedelMetadata()
        setattr(obj, ATTRIBUTE_NAME, [metadata1, metadata2])

        # act
        result = find_metadata_of_type(obj, AfterinitMetadata)

        # assert
        self.assertEqual(result, [metadata1])

    def test_find_metadata_of_type_2(self):
        """
        Tests that the ``find_metadata_of_type`` function correctly retrieves metadata
        of a specific type from an object even if there are no metadata.
        """

        # arrange
        obj = type("TestClass", (), {})

        # act
        result = find_metadata_of_type(obj, AfterinitMetadata)

        # assert
        self.assertEqual(result, [])

    def test_get_exactly_one_metadata_of_type_1(self):
        """
        Tests that the ``get_exactly_one_metadata_of_type`` function correctly retrieves
        exactly one metadata of a specific type from an object.
        """

        # arrange
        obj = type("TestClass", (), {})
        metadata = AfterinitMetadata()
        setattr(obj, ATTRIBUTE_NAME, [metadata])

        # act
        result = get_exactly_one_metadata_of_type(obj, AfterinitMetadata)

        # assert
        self.assertEqual(result, metadata)

    def test_get_exactly_one_metadata_of_type_2(self):
        """
        Tests that the ``get_exactly_one_metadata_of_type`` function raises a ValueError
        if no metadata is found.
        """

        # arrange
        obj = type("TestClass", (), {})

        # act & assert
        with self.assertRaises(ValueError):
            get_exactly_one_metadata_of_type(obj, AfterinitMetadata)

    def test_get_exactly_one_metadata_of_type_3(self):
        """
        Tests that the ``get_exactly_one_metadata_of_type`` function raises a ValueError
        if no metadata of the specified type is found.
        """

        # arrange
        obj = type("TestClass", (), {})
        setattr(obj, ATTRIBUTE_NAME, [AfterinitMetadata()])

        # act & assert
        with self.assertRaises(ValueError):
            get_exactly_one_metadata_of_type(obj, BeforedelMetadata)

    def test_get_exactly_one_metadata_of_type_4(self):
        """
        Tests that the ``get_exactly_one_metadata_of_type`` function raises a ValueError
        if more than one metadata of the specified type is found.
        """

        # arrange
        obj = type("TestClass", (), {})
        setattr(obj, ATTRIBUTE_NAME, [AfterinitMetadata(), AfterinitMetadata()])

        # act & assert
        with self.assertRaises(ValueError):
            get_exactly_one_metadata_of_type(obj, AfterinitMetadata)

    def test_has_metadata_of_type_1(self):
        """
        Tests that the ``has_metadata_of_type`` function correctly checks
        if an object has metadata of a specific type.
        """

        # arrange
        obj = type("TestClass", (), {})
        setattr(obj, ATTRIBUTE_NAME, [AfterinitMetadata()])

        # act
        result = has_metadata_of_type(obj, AfterinitMetadata)

        # assert
        self.assertTrue(result)

    def test_has_metadata_of_type_2(self):
        """
        Tests that the ``has_metadata_of_type`` function correctly checks
        if an object has metadata of a specific type even if there are no metadata of that type.
        """

        # arrange
        obj = type("TestClass", (), {})
        setattr(obj, ATTRIBUTE_NAME, [AfterinitMetadata()])

        # act
        result = has_metadata_of_type(obj, BeforedelMetadata)

        # assert
        self.assertFalse(result)

    def test_has_metadata_of_type_3(self):
        """
        Tests that the ``has_metadata_of_type`` function correctly checks
        if an object has metadata of a specific type even if there are no metadata.
        """

        # arrange
        obj = type("TestClass", (), {})

        # act
        result = has_metadata_of_type(obj, AfterinitMetadata)

        # assert
        self.assertFalse(result)

    def test_is_metadata_of_type_1(self):
        """
        Tests that the metadata check functions (``is_afterinit``, ``is_beforedel``,
        ``is_configurator``, ``is_particle``, ``is_properties``, ``is_containerized``)
        correctly identify the presence of their respective metadata types in an object.
        """

        # arrange
        test_cases = {
            (AfterinitMetadata, ()): [is_afterinit],
            (BeforedelMetadata, ()): [is_beforedel],
            (ConfiguratorMetadata, ()): [is_configurator],
            (ParticleMetadata, ("",)): [is_particle, is_containerized],
            (PropertiesMetadata, ("", "", "")): [is_properties, is_containerized]
        }

        for (metadata_type, args), is_metadata_checkers in test_cases.items():
            obj = type("TestClass", (), {})
            metadata = metadata_type(*args)
            setattr(obj, ATTRIBUTE_NAME, [metadata])

            for is_metadata in is_metadata_checkers:
                with self.subTest(metadata_type=metadata_type.__name__, is_metadata=is_metadata.__name__):
                    # act
                    result = is_metadata(obj)

                    # assert
                    self.assertTrue(result)

    def test_is_metadata_of_type_2(self):
        """
        Tests that the metadata check functions (``is_afterinit``, ``is_beforedel``,
        ``is_configurator``, ``is_particle``, ``is_properties``, ``is_containerized``)
        correctly identify the presence of their respective metadata types in an object
        even if there are no metadata.
        """

        # arrange
        obj = type("TestClass", (), {})
        is_metadata_checkers = [
            is_afterinit,
            is_beforedel,
            is_configurator,
            is_particle,
            is_properties,
            is_containerized
        ]

        for is_metadata in is_metadata_checkers:
            with self.subTest(is_metadata=is_metadata.__name__):
                # act
                result = is_metadata(obj)

                # assert
                self.assertFalse(result)

    def test_is_metadata_of_type_3(self):
        """
        Tests that the metadata check functions (``is_afterinit``, ``is_beforedel``,
        ``is_configurator``, ``is_particle``, ``is_properties``, ``is_containerized``)
        correctly identify the presence of their respective metadata types in an object
        even if there are multiple types of metadata.
        """

        # arrange
        obj = type("TestClass", (), {})
        metadata = [
            AfterinitMetadata(),
            BeforedelMetadata(),
            ConfiguratorMetadata(),
            ParticleMetadata(name=""),
            PropertiesMetadata(name="", path="", prefix="")
        ]
        setattr(obj, ATTRIBUTE_NAME, metadata)
        is_metadata_checkers = [
            is_afterinit,
            is_beforedel,
            is_configurator,
            is_particle,
            is_properties,
            is_containerized
        ]

        for is_metadata in is_metadata_checkers:
            with self.subTest(is_metadata=is_metadata.__name__):
                # act
                result = is_metadata(obj)

                # assert
                self.assertTrue(result)
