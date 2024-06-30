import unittest
import datetime
import os
from unittest.mock import patch, mock_open
from src.helper_service.helper import (
  calculate_sleep_time, convert_seconds_to_hhmmss, get_sleep_statement, randomize_schedule_time, is_valid_regex, is_user_input_within_range, is_today_a_working_day,
  save_json, create_folder, is_folder_existent
)

class TestHelperFunctions(unittest.TestCase):

    def test_calculate_sleep_time_same_day(self):
        # arrange
        current_time = datetime.time(14, 30)
        event_time = datetime.time(15, 30)

        # act
        result = calculate_sleep_time(current_time, event_time)

        # assert
        self.assertEqual(result, 3600)  # 1 hour later

    def test_calculate_sleep_time_next_day(self):
        # arrange
        current_time = datetime.time(23, 50)
        event_time = datetime.time(0, 20)

        # act
        result = calculate_sleep_time(current_time, event_time)

        # assert
        self.assertEqual(result, 1800)  # 30 minutes into the next day

    # Testing convert_seconds_to_hhmmss
    def test_convert_seconds_to_hhmmss(self):
        # arrange
        seconds_diff = 3661  # 1 hour, 1 minute, 1 second

        # act
        result = convert_seconds_to_hhmmss(seconds_diff)

        # assert
        self.assertEqual(result, (1, 1, 1))

    # Testing get_sleep_statement
    def test_get_sleep_statement_full_time(self):
        # arrange
        hours, minutes, seconds = 2, 30, 45

        # act
        statement = get_sleep_statement(hours, minutes, seconds)

        # assert
        self.assertEqual(statement, "Sleeping for 2 hours, 30 minutes, and 45 seconds.")

    def test_get_sleep_statement_seconds_only(self):
        # arrange
        hours, minutes, seconds = 0, 0, 5

        # act
        statement = get_sleep_statement(hours, minutes, seconds)

        # assert
        self.assertEqual(statement, "Sleeping for and 5 seconds.")

    @patch('random.randint')
    def test_randomize_schedule_time(self, mock_randint):
        # arrange
        mock_randint.side_effect = [120, 240]  # 2 minutes, 4 minutes
        start_time = "08:00:00"
        stop_time = "18:00:00"
        expected_start = "08:02:00"
        expected_stop = "18:04:00"

        # act
        randomized_start, randomized_stop = randomize_schedule_time(start_time, stop_time)

        # assert
        self.assertEqual(randomized_start, expected_start)
        self.assertEqual(randomized_stop, expected_stop)

    def test_is_valid_regex(self):
        # arrange
        pattern = r'\d+'  # Regex for one or more digits
        valid_string = "123"
        invalid_string = "abc"

        # act & assert
        self.assertTrue(is_valid_regex(pattern, valid_string))
        self.assertFalse(is_valid_regex(pattern, invalid_string))

    def test_is_user_input_within_range_valid(self):
        # arrange
        user_input = "3"
        data_list = [10, 20, 30, 40]

        # act
        result = is_user_input_within_range(user_input, data_list)

        # assert
        self.assertTrue(result)

    def test_is_user_input_within_range_invalid(self):
        # arrange
        user_input = "5"  # Only 4 items in the list
        data_list = [10, 20, 30, 40]

        # act
        result = is_user_input_within_range(user_input, data_list)

        # assert
        self.assertFalse(result)

    @patch('datetime.datetime')
    def test_is_today_a_working_day(self, mock_datetime):
        # arrange
        mock_datetime.today.return_value.strftime.return_value = 'Monday'
        working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # act
        is_working_day = is_today_a_working_day(working_days)

        # assert
        self.assertTrue(is_working_day)
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("src.helper_service.helper.create_folder")
    def test_save_json(self, mock_create_folder, mock_makedirs, mock_file):
        # arrange
        data = {"key": "value"}
        file_name = "test"
        path = "/fake/path"

        # act
        save_json(data, file_name, path)

        # assert
        mock_create_folder.assert_called_once_with(path)
        mock_file.assert_called_once_with(os.path.join(path, "test.json"), 'w', encoding='utf-8')
        mock_file().write.assert_called()

    @patch("os.makedirs")
    @patch("src.helper_service.helper.is_folder_existent", return_value=False)
    def test_create_folder_not_exist(self, mock_is_folder_existent, mock_makedirs):
        # arrange
        path = "/fake/path"

        # act
        create_folder(path)

        # assert
        mock_is_folder_existent.assert_called_once_with(path)
        mock_makedirs.assert_called_once_with(path)

    @patch("os.makedirs")
    @patch("src.helper_service.helper.is_folder_existent", return_value=True)
    def test_create_folder_already_exist(self, mock_is_folder_existent, mock_makedirs):
        # arrange
        path = "/fake/path"

        # act
        create_folder(path)

        # assert
        mock_is_folder_existent.assert_called_once_with(path)
        mock_makedirs.assert_not_called()

    @patch("os.path.exists", return_value=True)
    def test_is_folder_existent_true(self, mock_exists):
        # arrange
        path = "/fake/path"

        # act
        result = is_folder_existent(path)

        # assert
        mock_exists.assert_called_once_with(path)
        self.assertTrue(result)

    @patch("os.path.exists", return_value=False)
    def test_is_folder_existent_false(self, mock_exists):
        # arrange
        path = "/fake/path"

        # act
        result = is_folder_existent(path)

        # assert
        mock_exists.assert_called_once_with(path)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
