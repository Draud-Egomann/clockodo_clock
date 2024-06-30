# import unittest
# from unittest.mock import patch, mock_open
# from src.clockodo_service.clock import (
#     get_current_timer_id,
#     reset_current_timer_id,
#     save_current_timer_id,
#     start_timer,
#     stop_timer,
# )


# class TestClockService(unittest.TestCase):

#     @patch("json.load")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_get_current_timer_id(self, mock_open, mock_load):
#         # Set up the mock to return a specific dictionary
#         mock_load.return_value = {"your_timer_id": 123}

#         # Act
#         timer_id = get_current_timer_id()

#         # Assert
#         self.assertEqual(timer_id, 123)

#     @patch("src.clockodo_service.clock.open", new_callable=mock_open)
#     @patch(
#         "src.clockodo_service.clock.map_timer_json", return_value={"your_timer_id": 0}
#     )
#     @patch("src.clockodo_service.clock.save_json")
#     def test_reset_current_timer_id(
#         self, mock_save_json, mock_map_timer_json, mock_open
#     ):
#         # Act
#         reset_current_timer_id()

#         # Assert
#         mock_save_json.assert_called_once_with({"your_timer_id": 0}, "tmp", "data")

#     @patch("src.clockodo_service.clock.requests.get")
#     @patch(
#         "src.clockodo_service.clock.map_timer_json", return_value={"your_timer_id": 321}
#     )
#     @patch("src.clockodo_service.clock.save_json")
#     def test_save_current_timer_id(self, mock_save_json, mock_map_timer_json, mock_get):
#         # Setup
#         mock_response = mock_get.return_value
#         mock_response.status_code = 200
#         mock_response.json.return_value = {"running": {"id": 321}}

#         # Act
#         result = save_current_timer_id()

#         # Assert
#         self.assertIsNone(result)
#         mock_save_json.assert_called_once_with({"your_timer_id": 321}, "tmp", "data")

#     @patch("src.clockodo_service.clock.requests.post")
#     def test_start_timer(self, mock_post):
#         # Setup
#         mock_response = mock_post.return_value
#         mock_response.status_code = 200

#         # Act
#         start_timer()

#         # Assert
#         mock_post.assert_called_once()

#     @patch("src.clockodo_service.clock.get_current_timer_id", return_value=123)
#     @patch("src.clockodo_service.clock.requests.delete")
#     def test_stop_timer(self, mock_delete, mock_get_current_timer_id):
#         # Setup
#         mock_response = mock_delete.return_value
#         mock_response.status_code = 200

#         # Act
#         stop_timer()

#         # Assert
#         mock_delete.assert_called_once_with(
#             "https://subdomain.clockodo.com/api/v2/clock/123",
#             headers={
#                 "X-ClockodoApiKey": "API_KEY",
#                 "X-ClockodoApiUser": "EMAIL",
#                 "X-Clockodo-External-Application": "Clockodo;EMAIL",
#             },
#         )


# if __name__ == "__main__":
#     unittest.main()
