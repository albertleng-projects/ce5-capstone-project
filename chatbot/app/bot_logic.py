"""
This module, bot_logic.py, contains the logic for a chatbot application.

It includes functions to load and format documents, create a vector store from the documents,
generate a response based on user input, and process the user's input to generate a response.

The main functions in this module are:
- format_docs: Concatenates the content of a list of documents into a single string.
- load_documents: Loads a file from a given path, splits it into chunks, and
                  returns a list of Document objects.
- load_embeddings: Creates a vector store from a list of Document objects.
- generate_response: Generates a response for the given user input using the
                     provided vector store.
- query: Processes the user's input, loads the documents, creates a vector store,
         and generates a response.

This module uses the OpenAI API for generating responses and the Chroma vector
store for storing document embeddings.
"""

import os
import logging
from typing import List

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.schema.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import (
    CharacterTextSplitter,
)
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import Chroma
from logger_config import setup_logger

load_dotenv()

# https://python.langchain.com/docs/modules/data_connection/vectorstores/

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGUAGE_MODEL = "gpt-3.5-turbo-instruct"
LOGGING_LEVEL = (
    os.getenv("LOGGING_LEVEL") if os.getenv("LOGGING_LEVEL") else logging.DEBUG
)
script_name = os.path.splitext(os.path.basename(__file__))[0]

logger = setup_logger(script_name, LOGGING_LEVEL)

template: str = """/
    You are a customer support specialist /
    question: {question}. You assist users with general inquiries based on {context} /
    and  technical issues. /
    """
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_message_prompt = HumanMessagePromptTemplate.from_template(
    input_variables=["question", "context"],
    template="{question}",
)
chat_prompt_template = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

model = ChatOpenAI()


def format_docs(docs: List[Document]) -> str:
    """
    Concatenate the page content of a list of documents, separated by two
    newlines into a single string.

    Args:
        docs (List[Document]): A list of Document objects.

    Returns:
        str: Concatenated string of all document contents.
    """
    return "\n\n".join([d.page_content for d in docs])


def load_documents(relative_path: str) -> List[Document]:
    """
    Loads a file from the relative path, splits it into chunks, and returns a
    list of Document objects.

    Args:
        relative_path (str): Relative path to the file.

    Returns:
        List[Document]: List of Document objects.
    """
    logger.debug("Loading documents from %s", relative_path)
    script_dir = os.path.dirname(__file__)
    absolute_path = os.path.join(script_dir, relative_path)
    logger.debug("Relative path: %s converted to %s", relative_path, absolute_path)

    logger.debug("Loading documents from %s", absolute_path)
    raw_documents = TextLoader(absolute_path).load()
    logger.debug("Loaded %d documents", len(raw_documents))
    logger.info("Splitting documents")
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    return text_splitter.split_documents(raw_documents)


def load_embeddings(documents: List[Document]) -> Chroma:
    """
    Create a vector store from a list of Document objects.

    Args:
        documents (List[Document]): List of Document objects.

    Returns:
        Chroma: Vector store object.
    """
    logger.debug("Creating vector store from %d documents", len(documents))
    db = Chroma.from_documents(documents, OpenAIEmbeddings())

    return db.as_retriever()


def generate_response(retriever: Chroma, user_input: str) -> str:
    """
    Generates a response for the given user input using the provided vector
    store.

    Args:
        retriever (Chroma): Vector store object.
        user_input (str): User input.

    Returns:
        str: Generated response.
    """
    logger.info("Generating response for user input: %s", user_input)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | chat_prompt_template
        | model
        | StrOutputParser()
    )
    return chain.invoke(user_input)


def query(user_input: str) -> str:
    """
    Processes the user's input, loads the documents, creates a vector store,
    and generates a response.

    Args:
        user_input (str): User input.

    Returns:
        str: Generated response.
    """
    logger.info("User input: %s", user_input)
    logger.info("Loading documents")
    documents = load_documents("./docs/faq_albert_shoes.txt")
    logger.info("Loading embeddings")
    retriever = load_embeddings(documents)
    logger.info("Generating response")
    response = generate_response(retriever, user_input)
    return response
