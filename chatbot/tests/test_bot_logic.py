import unittest
from chatbot.app.bot_logic import (
    load_documents,
    load_embeddings,
    generate_response,
    query,
)

DOCUMENT_PATH = "../app/docs/faq_abc.txt"


class TestBotLogic(unittest.TestCase):

    def test_load_documents(self):
        documents = load_documents(DOCUMENT_PATH)
        self.assertIsNotNone(documents)
        self.assertTrue(isinstance(documents, list))

    def test_load_embeddings(self):
        documents = load_documents(DOCUMENT_PATH)
        user_query = "test query"
        retriever = load_embeddings(documents, user_query)
        self.assertIsNotNone(retriever)

    def test_generate_response(self):
        documents = load_documents(DOCUMENT_PATH)
        user_query = "test query"
        retriever = load_embeddings(documents, user_query)
        response = generate_response(retriever, user_query)
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, str))

    def test_query(self):
        user_input = "test query"
        response = query(user_input)
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, str))


if __name__ == "__main__":
    unittest.main()
