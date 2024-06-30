import unittest
from unittest.mock import patch, mock_open
from src.manage_env_service.manage_env import check_env_correctness, env_write_customer_service, get_data_from_api

class TestManageEnvService(unittest.TestCase):

    @patch('src.manage_env_service.manage_env.config')
    def test_check_env_correctness(self, mock_config):
        # Mock environment variable values
        mock_config.side_effect = ['12345', 'user@example.com', 'subdomain', '1', '2', 'True', '["Monday", "Tuesday"]', '[("08:00:00", "18:00:00")]']
        
        # Act
        results = check_env_correctness()
        
        # Assert
        self.assertEqual(results, [True, True, True, True, True, True, True, True])

    @patch('src.manage_env_service.manage_env.open', new_callable=mock_open, read_data="CUSTOMERS_ID=123")
    @patch('src.manage_env_service.manage_env.get_data_from_api', return_value=456)
    def test_env_write_customer_service(self, mock_get_data_from_api, mock_file):
        # Act
        env_write_customer_service('.env', 'customers', 'CUSTOMERS_ID')

        # Assert
        mock_file.assert_called_with('.env', 'r')
        handle = mock_file()
        handle.write.assert_called_once_with('CUSTOMERS_ID=456')

    @patch('src.manage_env_service.manage_env.fetch_data')
    @patch('src.manage_env_service.manage_env.map_json', return_value=[{'id': 1, 'name': 'Service A'}, {'id': 2, 'name': 'Service B'}])
    @patch('src.manage_env_service.manage_env.input', side_effect=['3', '2'])
    @patch('src.manage_env_service.manage_env.is_user_input_within_range', side_effect=[False, True])
    def test_get_data_from_api(self, mock_range_check, mock_input, mock_map_json, mock_fetch_data):
        # Arrange
        mock_fetch_data.return_value = {'services': [{'id': 1, 'name': 'Service A'}, {'id': 2, 'name': 'Service B'}]}
        
        # Act
        result = get_data_from_api('services')

        # Assert
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
