"""
This module contains unit tests for the sentiment_analysis_api module.
It tests the API endpoints to ensure they are working as expected.
"""

import unittest
from unittest.mock import patch
import api.app.sentiment_analysis_api as api


class TestSentimentAnalysisAPI(unittest.TestCase):
    """
    This class contains unit tests for each function in the
    sentiment_analysis_api module of the API application. It sets up the
    necessary test data for testing, runs the tests, and asserts the expected
    results.
    """

    def setUp(self):
        self.app = api.app
        self.client = self.app.test_client()

    @patch("api.app.sentiment_analysis_api.comprehend.detect_sentiment")
    @patch("api.app.sentiment_analysis_api.comprehend.detect_dominant_language")
    @patch("api.app.sentiment_analysis_api.table.put_item")
    def test_post_user_query(
        self,
        mock_put_item,
        mock_detect_dominant_language,  # noqa
        mock_detect_sentiment,
    ):
        """
        Tests the post_user_query function from the sentiment_analysis_api
        module. It checks if the function returns a status code of 200 and a
        status of "Success" when a user query is posted. The function is
        tested with a mock sentiment of "POSITIVE" and a mock dominant
        language of "en".
        """
        mock_detect_sentiment.return_value = {"Sentiment": "POSITIVE"}
        mock_detect_dominant_language.return_value = {
            "Languages": [{"LanguageCode": "en"}]
        }
        response = self.client.post(
            "/api/v1/user_query", json={"text": "I love this product!"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "Success")

    @patch("api.app.sentiment_analysis_api.table.scan")
    def test_get_user_queries(self, mock_scan):
        """
        Tests the get_user_queries function from the sentiment_analysis_api
        module. It checks if the function returns a status code of 200 and a
        total of 0 when there are no user queries in the DynamoDB table.
        """
        mock_scan.return_value = {"Items": []}
        response = self.client.get("/api/v1/user_queries")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["total"], 0)

    @patch("api.app.sentiment_analysis_api.table.get_item")
    def test_get_user_query_found(self, mock_get_item):
        """
        Tests the get_user_query function from the sentiment_analysis_api module.
        It checks if the function returns a status code of 200 and the correct
        user query when a user query is found in the DynamoDB table. The
        function is tested with a mock user query with id "123", user_query
        "I love this product!", sentiment "POSITIVE", language "en",
        and timestamp "2022-01-01T12:00:00".
        """
        mock_get_item.return_value = {
            "Item": {
                "id": "123",
                "user_query": "I love this product!",
                "sentiment": "POSITIVE",
                "language": "en",
                "timestamp": "2022-01-01T12:00:00",
            }
        }
        response = self.client.get("/api/v1/user_queries/123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], "123")

    @patch("api.app.sentiment_analysis_api.table.get_item")
    def test_get_user_query_not_found(self, mock_get_item):
        """
        Tests the get_user_query function from the sentiment_analysis_api module.
        It checks if the function returns a status code of 404 and an error
        message when a user query is not found in the DynamoDB table. The
        function is tested with a mock response that does not contain the
        "Item" key.
        """
        mock_get_item.return_value = {}
        response = self.client.get("/api/v1/user_queries/123")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "User query not found")


if __name__ == "__main__":
    unittest.main()
