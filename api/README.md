# 📖 Sentiment Analysis API

This is a sentiment analysis API for a chatbot application. The API is built
using Flask and provides endpoints for posting user queries and retrieving user
queries. The sentiment of the user queries is analyzed using AWS Comprehend and
the results are stored in a DynamoDB table.

## 📝 Description

The API receives a user query, analyzes the sentiment and dominant language of
the query using AWS Comprehend, and stores the query, sentiment, language, and a
timestamp in a DynamoDB table. It also logs these activities.

## 📚 Requirements

- [Python 3.10.0](https://www.python.org/downloads/release/python-3100/)
- Flask
- boto3
- AWS Comprehend
- AWS DynamoDB

## ⚙️ Installation

Before you can run the Sentiment Analysis API, you need to install the necessary
dependencies. Here are the steps:

1. **Install Python**

   This project requires Python 3.10.0. If you don't have it installed, you can
   download it from
   the [official website](https://www.python.org/downloads/release/python-3100/).


2. **Create a virtual environment (Optional)**

   It's recommended to create a virtual environment to keep the dependencies
   required by this project separate from your other Python projects. Here's how
   to create a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Install the dependencies**

   The dependencies for this project are listed in a `requirements.txt` file.
   You can install them with the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variables**

   This project requires several environment variables to run. You can set them
   up in a `.env` file in the root directory of the project. Here's an example
   of what the `.env` file should look like:

   ```bash
   AWS_REGION=your_aws_region
   DYNAMODB_TABLE=your_dynamodb_table
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   LOGGING_LEVEL=your_logging_level
   ```

   Replace `your_aws_region`, `your_dynamodb_table`, `your_aws_access_key_id`, `your_aws_secret_access_key`,
   and `your_logging_level` with your actual values.


5. **Run the API**

   Now you're ready to run the API! You can do this with the following command:

   ```bash
   python sentiment_analysis_api.py
   ```

## 🌍 Environment Variables

- **AWS_REGION**: The AWS region where the DynamoDB table is located. Defaults
  to `us-east-1`.
- **DYNAMODB_TABLE**: The name of the DynamoDB table where user queries are
  stored.
  Defaults to `ce5-group6-user-queries`.
- **AWS_ACCESS_KEY_ID**: The AWS access key ID for accessing AWS services.
- **AWS_SECRET_ACCESS_KEY**: The AWS secret access key for accessing AWS
  services.
- **LOGGING_LEVEL**: The logging level for the logger. Defaults to
  `logging.DEBUG`.

## 🚀 Usage

To run the API, execute the following command:

```bash
python sentiment_analysis_api.py
```

The API will start on http://localhost:5000 and provides the following
endpoints:

### POST /api/v1/user_query

This endpoint accepts a POST request with a JSON body containing a text field
with the user query.

Sample request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"I love this product!"}' http://localhost:5000/api/v1/user_query
```

Sample response:

```json
{
  "message": "User query stored successfully.",
  "query": "I love this product!",
  "sentiment": "POSITIVE",
  "language": "en",
  "timestamp": "2022-02-22T12:00:00"
}
```

### GET /api/v1/user_queries

This endpoint returns all user queries from the database.

Sample request:

```bash
curl -X GET http://localhost:5000/api/v1/user_queries
```

Sample response:

```json
{
  "user_queries": [
    {
      "id": "dec7bfe9-cfe6-475a-9fbb-bb1127aa2db4",
      "user_query": "I love this product!",
      "sentiment": "POSITIVE",
      "language": "en",
      "timestamp": "2022-01-01T12:00:00"
    },
    {
      "id": "dec7bfe9-cfe6-475a-9fbb-bb1127aa2db5",
      "user_query": "I hate this product!",
      "sentiment": "NEGATIVE",
      "language": "en",
      "timestamp": "2022-01-01T12:00:01"
    }
  ],
  "total": 2
}

```

### GET /api/v1/user_queries/<user_query_id>

This endpoint returns a specific user query from the database using the
provided `user_query_id`.

Sample request:

```bash
curl -X GET http://localhost:5000/api/v1/user_queries/dec7bfe9-cfe6-475a-9fbb-bb1127aa2db4
```

Sample response:

```json
{
  "id": "dec7bfe9-cfe6-475a-9fbb-bb1127aa2db4",
  "user_query": "I love this product!",
  "sentiment": "POSITIVE",
  "language": "en",
  "timestamp": "2022-01-01T12:00:00"
}
```

## 🐳 Docker Usage

To containerize the application, you can use Docker. First, build the Docker
image with the following command:

```bash
docker build -t sentiment_analysis_api .
```

Then, run the Docker container with the following command:

```bash
docker run -p 5000:5000 \
-e AWS_REGION=<your_aws_region> \
-e DYNAMODB_TABLE=<your_dynamodb_table> \
-e AWS_ACCESS_KEY_ID=<your_aws_access_key_id> \
-e AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key> \
-e LOGGING_LEVEL=<your_logging_level> \
sentiment_analysis_api
```

This will start the sentiment analysis API on port 5000.