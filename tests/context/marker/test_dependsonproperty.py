import re
from typing import override
from unittest import TestCase
from unittest.mock import patch

from puripy.context.decorator import DecoratableType
from puripy.marker import dependsonproperty
from puripy.context.metadata import DependsonpropertyMetadata


class TestParticle(TestCase):

    @override
    def setUp(self):
        self.is_valid_decoratable_patcher = patch("puripy.marker.marker.is_valid_decoratable")
        self.append_metadata_patcher = patch("puripy.marker.marker.append_metadata")

        self.is_valid_decoratable_mock = self.is_valid_decoratable_patcher.start()
        self.append_metadata_mock = self.append_metadata_patcher.start()

        self.is_valid_decoratable_mock.return_value = True

    @override
    def tearDown(self):
        self.is_valid_decoratable_patcher.stop()
        self.append_metadata_patcher.stop()

    def test_only_mandatory_args(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = DependsonpropertyMetadata(key="key", value="value", match_on_missing=False, path="")

        # act
        decorated_test_class = dependsonproperty(key="key", value="value")(test_class)

        # assert
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertIs(test_class, decorated_test_class)

    def test_pos_args_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        exception_regex_message = re.compile(".* missing 2 required positional arguments: 'key' and 'value'")

        # act & assert
        self.assertRaisesRegex(TypeError,
                               exception_regex_message,
                               lambda: dependsonproperty("key", "value")(test_class))

    def test_kw_args_decoration(self):
        # arrange
        test_class = type("TestClass", (), {})
        metadata = DependsonpropertyMetadata(key="key", value="value", match_on_missing=True, path="path")

        # act
        decorator = dependsonproperty(key="key", value="value", match_on_missing=True, path="path")
        decorated_test_class = decorator(test_class)

        # assert
        self.append_metadata_mock.assert_called_once_with(test_class, metadata)
        self.assertEqual(test_class, decorated_test_class)

    def test_as_class_and_function_decorator(self):
        # arrange
        test_class = type("TestClass", (), {})

        # act
        dependsonproperty(key="key", value="value")(test_class)

        # assert
        self.is_valid_decoratable_mock.assert_called_once_with(
            test_class,
            [DecoratableType.CLASS, DecoratableType.FUNCTION, DecoratableType.METHOD]
        )
