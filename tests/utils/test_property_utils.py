import warnings
from pathlib import Path
from typing import override
from unittest import TestCase
from unittest.mock import patch

from puripy.utils.property_utils import find_property_files, get_property_file_path


class TestPropertyUtils(TestCase):

    @override
    def setUp(self):
        self.glob_patcher = patch("pathlib.Path.glob")

        self.glob_mock = self.glob_patcher.start()

    @override
    def tearDown(self):
        self.glob_patcher.stop()

    def test_find_property_files_1(self):
        """
        Tests that the ``find_property_files`` function correctly finds all property files in the current directory.
        """

        # arrange
        paths = [Path("properties.txt"), Path("properties.json")]
        self.glob_mock.return_value = iter(paths)

        # act
        result = find_property_files()

        # assert
        self.assertEqual(result, paths)

    def test_get_property_file_path_1(self):
        """
        Tests that the ``get_property_file_path`` function correctly returns the single property file found.
        """

        # arrange
        paths = [Path("properties.txt")]
        self.glob_mock.return_value = iter(paths)

        # act
        result = get_property_file_path()

        # assert
        self.assertEqual(result, paths[0])

    def test_get_property_file_path_2(self):
        """
        Tests that the ``get_property_file_path`` function correctly returns the first property file found
        and issues a warning when more than one property file is found.
        """

        # arrange
        paths = [Path("properties.txt"), Path("properties.json")]
        self.glob_mock.return_value = iter(paths)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # act
            result = get_property_file_path()

            # assert
            self.assertEqual(result, paths[0])
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))
            self.assertIn("More than one default property file found", str(w[-1].message))

    def test_get_property_file_path_3(self):
        """
        Tests that the ``get_property_file_path`` function raises a FileNotFoundError
        when no property file is found.
        """

        # arrange
        self.glob_mock.return_value = iter([])

        # act & assert
        with self.assertRaises(FileNotFoundError) as error:
            get_property_file_path()

        self.assertEqual(str(error.exception), "No default property file found")
