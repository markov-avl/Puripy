import re
from abc import ABC, abstractmethod
from typing import override
from unittest import TestCase
from unittest.mock import patch

from puripy.context.decorator import DecoratableType
from puripy.marker import particle
from puripy.context.metadata import ParticleMetadata


class TestParticle(TestCase):

    @override
    def setUp(self):
        self.is_valid_decoratable_patcher = patch("puripy.marker.marker.is_valid_decoratable")
        self.append_metadata_patcher = patch("puripy.marker.marker.append_metadata")
        self.has_string_annotations_patcher = patch("puripy.marker.particle.has_string_annotations")

        self.is_valid_decoratable_mock = self.is_valid_decoratable_patcher.start()
        self.append_metadata_mock = self.append_metadata_patcher.start()
        self.has_string_annotations_mock = self.has_string_annotations_patcher.start()

        self.is_valid_decoratable_mock.return_value = True
        self.has_string_annotations_mock.return_value = False

    @override
    def tearDown(self):
        self.is_valid_decoratable_patcher.stop()
        self.append_metadata_patcher.stop()
        self.has_string_annotations_patcher.stop()

    def test_no_args_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = ParticleMetadata(name="")

        # act
        decorated_test_class = particle()(test_class)

        # assert
        self.has_string_annotations_mock.assert_called_once_with(test_class)
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertIs(test_class, decorated_test_class)

    def test_no_args_uncalled_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = ParticleMetadata(name="")

        # act
        # noinspection PyTypeChecker
        decorated_test_class = particle(test_class)

        # assert
        self.has_string_annotations_mock.assert_called_once_with(test_class)
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertEqual(test_class, decorated_test_class)

    def test_pos_args_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = ParticleMetadata(name="name")

        # act
        decorated_test_class = particle("name")(test_class)

        # assert
        self.has_string_annotations_mock.assert_called_once_with(test_class)
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertEqual(test_class, decorated_test_class)

    def test_kw_args_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = ParticleMetadata(name="name")

        # act
        decorated_test_class = particle(name="name")(test_class)

        # assert
        self.has_string_annotations_mock.assert_called_once_with(test_class)
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertEqual(test_class, decorated_test_class)

    def test_raises_on_has_string_annotations(self):
        # arrange
        self.has_string_annotations_mock.return_value = True
        test_class = type("TestClass", (), {})
        exception_message_regex = re.compile(r"Particle .* has string-annotated dependencies")

        # act & assert
        self.assertRaisesRegex(RuntimeError, exception_message_regex, lambda: particle()(test_class))
        self.has_string_annotations_mock.assert_called_once_with(test_class)

    def test_raises_on_abstract_class(self):
        # arrange
        test_class = type("TestClass", (ABC,), {"abstract_test_method": abstractmethod(lambda: ...)})
        exception_message_regex = re.compile(r"Abstract class cannot be a particle")

        # act & assert
        self.assertRaisesRegex(RuntimeError, exception_message_regex, lambda: particle()(test_class))

    def test_as_class_and_function_decorator(self):
        # arrange
        test_class = type("TestClass", (), {})

        # act
        particle()(test_class)

        # assert
        self.is_valid_decoratable_mock.assert_called_once_with(
            test_class,
            [DecoratableType.CLASS, DecoratableType.FUNCTION]
        )
