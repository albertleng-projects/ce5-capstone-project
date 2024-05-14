import os
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
from typing import List

load_dotenv()

# https://python.langchain.com/docs/modules/data_connection/vectorstores/

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGUAGE_MODEL = "gpt-3.5-turbo-instruct"

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
    return "\n\n".join([d.page_content for d in docs])


def load_documents(relative_path: str) -> List[Document]:
    """Load a file from path, split it into chunks, embed each chunk and load it into the vector store."""
    script_dir = os.path.dirname(__file__)
    absolute_path = os.path.join(script_dir, relative_path)
    raw_documents = TextLoader(absolute_path).load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    return text_splitter.split_documents(raw_documents)


def load_embeddings(documents: List[Document], user_query: str) -> Chroma:
    """Create a vector store from a set of documents."""
    db = Chroma.from_documents(documents, OpenAIEmbeddings())
    # TODO: Fix the following line - unused 'docs'
    docs = db.similarity_search(user_query)
    return db.as_retriever()


def generate_response(retriever: Chroma, user_input: str) -> str:
    # Create a prompt template using a template from the config module and input variables
    # representing the context and question.
    # create the prompt
    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | chat_prompt_template
            | model
            | StrOutputParser()
    )
    return chain.invoke(user_input)


def query(user_input: str) -> str:
    documents = load_documents("./docs/faq_abc.txt")
    retriever = load_embeddings(documents, user_input)
    response = generate_response(retriever, user_input)
    return response
