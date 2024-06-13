"""
This module contains the sentiment analysis API for a chatbot application.

The API is built using Flask and provides endpoints for posting user queries and
retrieving user queries. The sentiment of the user queries is analyzed using
AWS Comprehend and the results are stored in a DynamoDB table.

The API also includes logging functionalities. The logger is set up with a
console handler and a file handler. The file handler writes logs to a file in a
'logs' directory and rotates the log file at midnight every day, keeping a
backup of the last 14 days. The console handler writes logs to the console.
Both handlers use a formatter that includes the time of logging, the name of
the logger, the logging level, and the log message.

This module can be run as a standalone script to start the Flask development
server.

Environment variables:
    AWS_REGION: The AWS region where the DynamoDB table is located.
        Defaults to 'us-east-1'.
    DYNAMODB_TABLE: The name of the DynamoDB table where user queries are stored.
        Defaults to 'ce5-group6-user-queries'.
    AWS_ACCESS_KEY_ID: The AWS access key ID for accessing AWS services.
    AWS_SECRET_ACCESS_KEY: The AWS secret access key for accessing AWS services.
    LOGGING_LEVEL: The logging level for the logger. Defaults to logging.DEBUG.
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)


def setup_logger(name: str,
                 logging_level: int = logging.DEBUG) -> logging.Logger:
    """
    Sets up a logger with the specified name and logging level.

    The logger is set up with a console handler and a file handler. The console
    handler writes logs to the console, and the file handler writes logs to a
    file in a 'logs' directory. The file handler rotates the log file at
    midnight every day, keeping a backup of the last 14 days. Both handlers use
    a formatter that includes the time of logging, the name of the logger, the
    logging level, and the log message.

    If the 'logs' directory does not exist, it is created.

    Args:
        name (str): The name of the logger.
        logging_level (int, optional): The logging level of the logger. Defaults
        to logging.DEBUG.

    Returns:
        logging.Logger: The set-up logger.
    """
    log = logging.getLogger(name)
    log.setLevel(logging_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)

    if not os.path.exists("logs"):
        os.makedirs("logs")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = TimedRotatingFileHandler(
        f"logs/{name}_{current_time}.log", when="midnight", backupCount=14
    )
    file_handler.setLevel(logging_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    log.addHandler(console_handler)
    log.addHandler(file_handler)

    return log


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "ce5-group6-user-queries")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
LOGGING_LEVEL = (
    os.getenv("LOGGING_LEVEL") if os.getenv("LOGGING_LEVEL") else logging.DEBUG
)
DEBUG = os.getenv("DEBUG", "False") == "True"

script_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(script_name, logging.DEBUG)

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

comprehend = session.client(service_name="comprehend")
dynamodb = session.resource("dynamodb")
table = dynamodb.Table(DYNAMODB_TABLE)

try:
    table.load()
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceNotFoundException":
        table = dynamodb.create_table(
            TableName=DYNAMODB_TABLE,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            # Partition key
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5,
                                   "WriteCapacityUnits": 5},
        )
    else:
        raise


# TODO: Add test for 'health' endpoint
@app.route("/health")
def health():
    """
    Health check endpoint for the application.

    This endpoint returns a simple response indicating the health of the application.
    It's typically used by infrastructure services to determine the health of the application.

    Returns:
        tuple: A tuple containing a string indicating the status of the
        application and an HTTP status code.
    """
    return "OK", 200


@app.route("/api/v1/user_query", methods=["POST"])
def post_user_query():
    """
    Handles POST requests to the /api/v1/user_query endpoint.

    This function receives a user query in the request body, analyzes the
    sentiment and dominant language of the query using AWS Comprehend, and
    stores the query, sentiment, language, and a timestamp in a DynamoDB table.
    It also logs these activities.

    The request body should be a JSON object with a 'text' field containing the
    user query. For example:
    {
        "text": "I love this product!"
    }

    The function returns a JSON object with the status, user query, sentiment,
    language, and timestamp. For example:
    {
        "status": "Success",
        "user_query": "I love this product!",
        "sentiment": "POSITIVE",
        "language": "en",
        "timestamp": "2022-01-01T12:00:00"
    }

    Returns:
        A tuple containing a Flask Response object and an HTTP status code. The
        Response object contains a JSON object with the status, user query,
        sentiment, language, and timestamp.

    TODO: Add error handling
    """
    logger.info("Received user query")
    text = request.json.get("text")
    logger.debug("Received user query: %s", text)
    sentiment_response = comprehend.detect_sentiment(Text=text,
                                                     LanguageCode="en")
    logger.debug("Sentiment response: %s", sentiment_response)
    sentiment = sentiment_response["Sentiment"]

    language_response = comprehend.detect_dominant_language(Text=text)
    logger.debug("Language response: %s", language_response)
    language = language_response["Languages"][0]["LanguageCode"]

    user_query_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()  # Get the current date and time

    logger.debug("Adding user query to DynamoDB: %s", user_query_id)
    table.put_item(
        Item={
            "id": user_query_id,
            "user_query": text,
            "sentiment": sentiment,
            "language": language,
            "timestamp": timestamp,
        }
    )

    return (
        jsonify(
            {
                "status": "Success",
                "user_query": text,
                "sentiment": sentiment,
                "language": language,
                "timestamp": timestamp,
            }
        ),
        200,
    )


@app.route("/api/v1/user_queries", methods=["GET"])
def get_user_queries():
    """
    Handles GET requests to the /api/v1/user_queries endpoint.

    This function retrieves all user queries from the DynamoDB table and returns
    them in a JSON object. It also logs these activities.

    The function returns a JSON object with the user queries and the total
    number of queries. For example:
    {
        "user_queries": [
            {
                "id": "123",
                "user_query": "I love this product!",
                "sentiment": "POSITIVE",
                "language": "en",
                "timestamp": "2022-01-01T12:00:00"
            },
            ...
        ],
        "total": 10
    }

    Returns:
        A tuple containing a Flask Response object and an HTTP status code. The
        Response object contains a JSON object with the user queries and the
        total number of queries.

    TODO: Add error handling
    """
    logger.info("Retrieving user queries")
    response = table.scan()
    logger.debug("User queries response: %s", response)
    user_queries = response["Items"]
    total = len(user_queries)
    logger.debug("Total user queries: %s", total)
    return jsonify({"user_queries": user_queries, "total": total}), 200


@app.route("/api/v1/user_queries/<user_query_id>", methods=["GET"])
def get_user_query(user_query_id):
    """
    Handles GET requests to the /api/v1/user_queries/<user_query_id> endpoint.

    This function retrieves a specific user query from the DynamoDB table using
    the provided user_query_id and returns it in a JSON object. It also logs
    these activities.

    The function returns a JSON object with the user query. For example:
    {
        "id": "123",
        "user_query": "I love this product!",
        "sentiment": "POSITIVE",
        "language": "en",
        "timestamp": "2022-01-01T12:00:00"
    }

    If the user query is not found, the function returns a JSON object with an
    error message and a 404 status code. For example:
    {
        "error": "User query not found"
    }

    Returns:
        A tuple containing a Flask Response object and an HTTP status code. The
        Response object contains a JSON object with the user query or an error
        message.
    """
    logger.info("Retrieving user query")
    logger.debug("Retrieving user query: %s", user_query_id)
    response = table.get_item(Key={"id": user_query_id})
    logger.debug("User query response: %s", response)
    if "Item" not in response:
        return jsonify({"error": "User query not found"}), 404
    return jsonify(response["Item"]), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=DEBUG)
