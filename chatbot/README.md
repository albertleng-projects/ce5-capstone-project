## Project : A Custom Q&A Chatbot built with OpenAI, LangChain, Chroma and Streamlit

## 💻 Project Overview

Welcome to our custom Q&A chatbot, a sophisticated tool powered by OpenAI, LangChain, and Chroma. This chatbot is designed to provide accurate and contextually relevant responses to user queries.

- **OpenAI**: Our chatbot utilizes the OpenAI API to generate intelligent and relevant answers to a wide range of questions.
- **LangChain**: With the help of LangChain, our chatbot supports multilingual interactions, translating user queries and responses between English and other languages.
- **Chroma**: To enhance the user experience, our chatbot employs Chroma to convert text responses into speech, providing an auditory response to user queries.
- **Streamlit**: Our chatbot is deployed as a web application using Streamlit, hosted in AWS. It allows users to interact with the chatbot through a user-friendly interface.

## 🛠️ Requirements : Installation & Setup

### [Python 3.10.0](https://www.python.org/downloads/release/python-3100/)

### packages

- **LangChain** :[LangChain](https://www.langchain.com/) is a Python library
  that translates text to and from any language. It uses the Google Translate
  API to translate text. It also uses the Google Cloud Text-to-Speech API to
  convert text to speech.
- **Chroma** : [Chroma](https://www.trychroma.com/) is a Python library that
  converts text to speech. It uses the Google Cloud Text-to-Speech API to
  convert text to speech.
- **OpenAI** : [OpenAI](https://python.langchain.com/docs/integrations/platforms/openai)
  is a Python library that provides a simple interface to the OpenAI API. It
  also provides a command-line interface (CLI) for interacting with the API.
- **python-dotenv** : [python-dotenv](https://pypi.org/project/python-dotenv/)
  is a Python library that loads environment variables from a .env file. It is
  used to load the OpenAI API key from the .env file.
- **Streamlit** : [Streamlit](https://streamlit.io/) is a Python library that
  makes it easy to create and share beautiful, custom web apps for machine
  learning and data science. It is used to create the web app.

## 🌐 Create a virtual environment & activate the virtual environment (Optional) :

```
python -m venv env
source env/bin/activate

```

## 🏗️ Installation:

### Install [Python 3.10](https://www.python.org/downloads/release/python-3100/) (preferable)
`Note: This project was developed and tested using Python 3.10.0.` 


```
pip install -r requirements.txt
pip install --upgrade langchain
```

## [🔑 Get an API key](https://platform.openai.com/account/api-keys)
### Set the key as an environment variable:

`export OPENAI_API_KEY='your_openai_api_key'`

.env file:

```
OPENAI_API_KEY=[your_openai_api_key]
```

## 📝 Run unit tests:

`pytest tests/`

or run by ignoring warnings

`pytest -p no:warnings tests/`

## ▶️ start streamlit app on localhost:8501:

`streamlit run app/app.py`

## 🌐 Access App:

After starting the app, visit `http://localhost:8501`  
  

This opens the app in your browser. Have fun! 😎  
<img src="chatbot.gif" width="50%" height="50%">

## 🐳 Alternatively, using Docker:
### Build the container image:

```
docker build -t my-app .
```

### Run the container:

```
docker run -p 8501:8501 -e OPENAI_API_KEY=<openai_api_key> my-app
```   