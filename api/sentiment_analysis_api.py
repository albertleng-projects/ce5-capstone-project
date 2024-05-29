import os
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime

app = Flask(__name__)

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE', 'ce5-group6-user-queries')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

comprehend = session.client(service_name='comprehend')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE)

try:
    table.load()
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        table = dynamodb.create_table(
            TableName=DYNAMODB_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    else:
        raise


@app.route('/user_query', methods=['POST'])
def post_user_query():
    text = request.json.get('text')
    sentiment_response = comprehend.detect_sentiment(Text=text,
                                                     LanguageCode='en')
    sentiment = sentiment_response['Sentiment']

    language_response = comprehend.detect_dominant_language(Text=text)
    language = language_response['Languages'][0]['LanguageCode']

    user_query_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()  # Get the current date and time

    table.put_item(
        Item={
            'id': user_query_id,
            'user_query': text,
            'sentiment': sentiment,
            'language': language,
            'timestamp': timestamp  # Store the timestamp in the table
        }
    )

    return jsonify(
        {'status': 'Success', 'user_query': text, 'sentiment': sentiment,
         'language': language, 'timestamp': timestamp}), 200


@app.route('/user_queries', methods=['GET'])
def get_user_queries():
    response = table.scan()
    user_queries = response['Items']
    total = len(user_queries)
    return jsonify({"user_queries": user_queries, "total": total}), 200


if __name__ == '__main__':
    app.run(debug=True)


# TODOs
# 1. Add logging
# 2. Add unit tests
# 3. Add containerizations
#  - dockerfile
#  - dockerignore
# 4. Add CI/CD
# 5. Add calls from Chatbot app
# 6. Find out proper practise for production server, i.e.
#    - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
#  * Running on http://127.0.0.1:5000
# 7. Add README.md