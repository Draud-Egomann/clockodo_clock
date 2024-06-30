import unittest
from src.clockodo_mapping_service.mapping import map_json, map_timer_json

class TestMapJson(unittest.TestCase):
    def test_map_json_empty_list(self):
        """Test that an empty list returns an empty list."""

        # act
        result = map_json([])

        # assert
        self.assertEqual(result, [])

    def test_map_json_valid_input(self):
        """Test that the function correctly maps a list of dictionaries."""
        # arrange
        input_data = [
            {'id': 1, 'name': 'Alice', 'extra': 'unused'},
            {'id': 2, 'name': 'Bob'}
        ]
        expected_output = [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'}
        ]

        # act
        result = map_json(input_data)

        # assert
        self.assertEqual(result, expected_output)

    def test_map_json_missing_keys(self):
        """Test that the function raises a KeyError when required keys are missing."""

        with self.assertRaises(KeyError):
            map_json([{'id': 1}, {'name': 'Bob'}])

class TestMapTimerJson(unittest.TestCase):
    def test_map_timer_json(self):
        """Test that the function correctly creates a dictionary with the provided integer."""
        # arrange
        expected_output = {'your_timer_id': 123}

        # act
        result = map_timer_json(123)

        # assert
        self.assertEqual(result, expected_output)

    def test_map_timer_json_non_int_input(self):
        """Test behavior with non-integer inputs."""
        # arrange
        expected_output = {'your_timer_id': '123'}

        # act
        result = map_timer_json('123')

        # assert
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()