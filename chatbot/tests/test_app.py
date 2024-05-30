"""
This module contains unit tests for the `call_sentiment_analysis_api` function
in the `chatbot.app.app` module.

The `TestApp` class contains two test cases:
- `test_successful_api_call`: This test case mocks a successful API response and
  checks if the `call_sentiment_analysis_api` function returns the correct
  response.
- `test_failed_api_call`: This test case mocks a failed API response by raising
  a `RequestException`. It checks if the `call_sentiment_analysis_api` function
  handles the exception correctly and returns `None`.

Each test case uses the `unittest.mock.patch` decorator to mock the
`requests.post` method and the logger used in the `call_sentiment_analysis_api`
function. This allows us to simulate different API responses and check how
the function handles them.
"""

import unittest
from unittest.mock import patch, Mock
from requests.exceptions import RequestException
from chatbot.app.app import call_sentiment_analysis_api


class TestApp(unittest.TestCase):
    """
    This class contains unit tests for the `call_sentiment_analysis_api` function
    in the `chatbot.app.app` module.

    The class contains two test cases:
    - `test_successful_api_call`: This test case mocks a successful API response and
      checks if the `call_sentiment_analysis_api` function returns the correct response.
    - `test_failed_api_call`: This test case mocks a failed API response by raising a
      `RequestException`. It checks if the `call_sentiment_analysis_api` function
      handles the exception correctly and returns `None`.

    Each test case uses the `unittest.mock.patch` decorator to mock the `requests.post`
    method and the logger used in the `call_sentiment_analysis_api` function. This allows
    us to simulate different API responses and check how the function handles them.
    """

    @patch("chatbot.app.app.requests.post")
    @patch("chatbot.app.app.logger")
    def test_successful_api_call(self, mock_logger, mock_post):
        """
        Test case for a successful API call to the sentiment analysis API.

        This test case mocks a successful API response and checks if the
        `call_sentiment_analysis_api` function returns the correct response.
        It also checks if the `requests.post` method and the logger methods
        were called with the correct arguments.

        Args:
            mock_logger (Mock): A mock for the logger used in the
            `call_sentiment_analysis_api` function.
            mock_post (Mock): A mock for the `requests.post` method.

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "Success"}
        mock_post.return_value = mock_response

        prompt = "I love this product!"
        response = call_sentiment_analysis_api(prompt)

        self.assertEqual(response, {"status": "Success"})
        mock_post.assert_called_once()
        mock_logger.info.assert_called_with(
            "Making a request to the sentiment analysis API"
        )
        mock_logger.debug.assert_called_with(
            "Request URL: %s and user_query: %s", mock_post.call_args[0][0], prompt
        )

    @patch("chatbot.app.app.requests.post")
    @patch("chatbot.app.app.logger")
    def test_failed_api_call(self, mock_logger, mock_post):
        """
        Test case for a failed API call to the sentiment analysis API.

        This test case mocks a failed API response by raising a `RequestException` and
        checks if the `call_sentiment_analysis_api` function handles the exception
        correctly and returns `None`. It also checks if the `requests.post` method and
        the logger methods were called with the correct arguments.

        Args:
            mock_logger (Mock): A mock for the logger used in the
                `call_sentiment_analysis_api` function.
            mock_post (Mock): A mock for the `requests.post` method.

        Returns:
            None
        """
        mock_post.side_effect = RequestException

        prompt = "I love this product!"
        response = call_sentiment_analysis_api(prompt)

        self.assertIsNone(response)
        mock_post.assert_called_once()
        mock_logger.info.assert_called_with(
            "Making a request to the sentiment analysis API"
        )
        mock_logger.debug.assert_called_with(
            "Request URL: %s and user_query: %s", mock_post.call_args[0][0], prompt
        )
        mock_logger.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
