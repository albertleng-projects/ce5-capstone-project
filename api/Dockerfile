FROM python:3.10.14-slim-bullseye

RUN apt-get update && apt-get install -y curl

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app/sentiment_analysis_api.py"]