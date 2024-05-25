"""
This module contains the main application logic for the chatbot. It initializes
the chat history, starts the chat, and handles user input and assistant
responses. It uses the OpenAI API for generating responses and Streamlit for
the user interface. Logging is also set up in this module to track the
application's activities.
"""

import os
import logging
import streamlit as st
import openai
from dotenv import load_dotenv
from bot_logic import query
from logger_config import setup_logger

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
MODEL_ENGINE = "gpt-3.5-turbo"
LOGGING_LEVEL = (
    os.getenv("LOGGING_LEVEL") if os.getenv("LOGGING_LEVEL") else logging.DEBUG
)
script_name = os.path.splitext(os.path.basename(__file__))[0]

logger = setup_logger(script_name, LOGGING_LEVEL)

st.title("👠 ABC Shoes Chatbot App")
chat_placeholder = st.empty()


def init_chat_history() -> None:
    """
    Initializes the chat history in the Streamlit session state. If the chat
    history does not exist, it creates a new list and adds a system message.

    Returns:
        None
    """
    logger.info("Initializing chat history: %s", st.session_state)
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        logger.debug("Updated session state: %s", st.session_state)
    logger.info("Chat history initialized")


def start_chat() -> None:
    """
    Starts the chat interface in the Streamlit app. It loads the chat history,
    accepts user input, generates a response using the query function from
    bot_logic, and updates the chat history with the user input and assistant
    response.

    Returns:
         None
    """
    logger.info("Starting chat")
    with chat_placeholder.container():
        logger.info("Loading session_state.messages: %s", st.session_state.messages)
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    logger.debug(
                        "Adding message via st.markdown: %s", message["content"]
                    )
                    st.markdown(message["content"])

    if prompt := st.chat_input("👟 Need shoe advice? Ask away!"):
        logger.info("User input: %s", prompt)
        logger.debug("Adding %s to session_state.messages", prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            logger.debug("Adding user message via st.markdown: %s", prompt)
            st.markdown(prompt)

        response = query(prompt)
        logger.info("Assistant response: %s", response)

        with st.chat_message("assistant"):
            logger.debug("Adding assistant response via st.markdown: %s", response)
            st.markdown(response)

        logger.debug("Adding assistant response %s to session_state.messages", response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    logger.info("Chat started")


if __name__ == "__main__":
    init_chat_history()
    start_chat()
