import unittest
from unittest.mock import patch
from Main import MasterWindow, existing_languages


class MasterWindowTest(MasterWindow):
    @staticmethod
    def load_data():
        # Simulate loading data with an incorrect list of existing languages
        return ['English', 'Spanish', 'French']

class TestLanguages(unittest.TestCase):
    def setUp(self):
        self.master_window = MasterWindow()

    def tearDown(self):
        self.master_window.destroy()

    @patch('Main.MasterWindow', MasterWindowTest)
    def test_existing_languages(self):
        languages = existing_languages()

        expected_languages = ['English', 'Francais', 'Hindi', 'Polski', 'Slovensky', 'Tagalog', 'Ελληνικά']
        self.assertListEqual(languages, expected_languages)

    def test_get_language_valid(self):
        # Set a valid language and call the get_language method
        self.master_window.language = 'Polski'
        language = self.master_window.get_language()

        self.assertEqual(language, 'Polski')

    def test_get_language_invalid(self):
        # Set an invalid language and call the get_language method
        self.master_window.language = 'NonExistentLanguage'
        with patch('Main.existing_languages', return_value=['English', 'Hindi']):
            language = self.master_window.get_language()

        self.assertEqual(language, 'English')


class TestMasterWindowLoadData(unittest.TestCase):
    def setUp(self):
        self.master_window = MasterWindow()

    @patch('builtins.open', create=True)
    def test_load_data(self, mock_open):
        # Stub the built-in open function to return fake data when reading from 'config.txt'
        mock_open.return_value.__enter__.return_value.read.return_value = 'John Smith\n/path/to/directory\nEnglish'

        self.master_window.load_data()

        self.assertEqual(self.master_window.username, 'John Smith')
        self.assertEqual(self.master_window.directory, '/path/to/directory')
        self.assertEqual(self.master_window.language, 'English')


class TestMasterWindow(unittest.TestCase):

    def setUp(self):
        self.master_window = MasterWindow()
        # Disable GUI updates during tests
        self.master_window.update_idletasks = lambda: None

    def tearDown(self):
        self.master_window.destroy()

    @patch('builtins.input', side_effect=['John Smith', '/path/to/directory', 'English'])
    def test_update_data(self, mock_input):
        # Check if update_data sets the user data correctly
        self.master_window.update_data('John Smith', '/path/to/directory', 'English')
        self.assertEqual(self.master_window.username, 'John Smith')
        self.assertEqual(self.master_window.directory, '/path/to/directory')
        self.assertEqual(self.master_window.language, 'English')

    @patch('builtins.input', side_effect=['Janko Hrasko', '/cesta/do/adresara', 'Slovensky'])
    def test_update_data_multiple(self, mock_input):
        # Check if update_data sets the user data correctly after multiple updates
        self.master_window.update_data('John Smith', '/path/to/directory', 'English')
        self.master_window.update_data('Jean Pierre', '/french/path/to/directory', 'Francais')
        self.master_window.update_data('Singh Smith', '/path/to/directory', 'Hindi')
        self.master_window.update_data('Jerzy Smith', '/path/to/directory', 'Polski')
        self.master_window.update_data('Janko Hrasko', '/cesta/do/adresara', 'Slovensky')
        self.master_window.update_data('Tagalog Smith', '/path/to/directory', 'Tagalog')
        self.master_window.update_data('Greek Smith', '/path/to/directory', 'Ελληνικά')
        self.assertEqual(self.master_window.username, 'Janko Hrasko')
        self.assertEqual(self.master_window.directory, '/cesta/do/adresara')
        self.assertEqual(self.master_window.language, 'Slovensky')


class TestGetDirectory(unittest.TestCase):
    def setUp(self):
        self.master_window = MasterWindow()
        self.master_window.update_data('John Smith', '/path/to/directory', 'English')

    def tearDown(self):
        self.master_window.destroy()

    def test_get_directory_valid(self):
        # Set a valid directory and call the get_directory method
        self.master_window.directory = '/path/to/valid/directory'
        directory = self.master_window.get_directory()

        # Assert that the returned directory is the same as the set directory
        self.assertEqual(directory, '/path/to/valid/directory')

    def test_get_directory_whitespace(self):
        # Set a whitespace directory and call the get_directory method
        self.master_window.directory = '   '
        directory = self.master_window.get_directory()

        # Assert that the returned directory is the default directory message
        self.assertEqual(directory, 'None selected')


if __name__ == '__main__':
    unittest.main()
