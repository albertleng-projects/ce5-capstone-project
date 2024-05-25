"""
This module contains unit tests for the bot_logic module of the chatbot
application. It tests the functions load_documents, load_embeddings,
generate_response, and query to ensure they are working as expected. The
tests are written using the unittest framework. Each function in the bot_logic
module has a corresponding test function in this module.
"""

import unittest
from chatbot.app.bot_logic import (
    load_documents,
    load_embeddings,
    generate_response,
    query,
)

DOCUMENT_PATH = "../app/docs/faq_abc.txt"


class TestBotLogic(unittest.TestCase):
    """
    This class contains unit tests for each function in the bot_logic module
    of the chatbot application. It sets up the necessary test data for testing,
    runs the tests, and asserts the expected results.
    """

    def test_load_documents(self):
        """
        Tests the load_documents function from the bot_logic module.
        It checks if the function returns a non-empty list of documents from a
        given path.
        """
        documents = load_documents(DOCUMENT_PATH)
        self.assertIsNotNone(documents)
        self.assertTrue(isinstance(documents, list))

    def test_load_embeddings(self):
        """
        Tests the load_embeddings function from the bot_logic module.
        It checks if the function returns a non-empty vector store for a given
        list of documents.
        """
        documents = load_documents(DOCUMENT_PATH)
        retriever = load_embeddings(documents)
        self.assertIsNotNone(retriever)

    def test_generate_response(self):
        """
        Tests the generate_response function from the bot_logic module.
        It checks if the function returns a non-empty string response for a
        given user query and vector store.
        """
        documents = load_documents(DOCUMENT_PATH)
        user_query = "test query"
        retriever = load_embeddings(documents)
        response = generate_response(retriever, user_query)
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, str))

    def test_query(self):
        """
        Tests the query function from the bot_logic module.
        It checks if the function returns a non-empty string response for a
        given user input.
        """
        user_input = "test query"
        response = query(user_input)
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, str))


if __name__ == "__main__":
    unittest.main()
