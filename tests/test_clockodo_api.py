import unittest
from unittest.mock import patch
from src.clockodo_service.api import get_api_data, retrieve_data

class TestClockodoAPI(unittest.TestCase):
    @patch('src.clockodo_service.api.requests.get')
    def test_retrieve_data_success(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': 'some data'}
        endpoint = 'customers/'

        # Act
        result = retrieve_data(endpoint)

        # Assert
        self.assertEqual(result, {'data': 'some data'})

    @patch('src.clockodo_service.api.requests.get')
    def test_retrieve_data_failure(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = 'Not found'
        endpoint = 'customers/'

        # Act
        result = retrieve_data(endpoint)

        # Assert
        self.assertEqual(result, 0)
        mock_get.assert_called_once()

    @patch('src.clockodo_service.api.retrieve_data')
    def test_get_api_data_success(self, mock_retrieve_data):
        # Arrange
        mock_retrieve_data.return_value = {'data': 'valid data'}
        endpoint = 'services/'

        # Act
        result = get_api_data(endpoint)

        # Assert
        self.assertEqual(result, {'data': 'valid data'})
        mock_retrieve_data.assert_called_once_with('services/')

    @patch('src.clockodo_service.api.retrieve_data')
    def test_get_api_data_failure(self, mock_retrieve_data):
        # Arrange
        mock_retrieve_data.return_value = 0
        endpoint = 'services/'

        # Act
        result = get_api_data(endpoint)

        # Assert
        self.assertEqual(result, 0)
        mock_retrieve_data.assert_called_once_with('services/')

if __name__ == '__main__':
    unittest.main()
