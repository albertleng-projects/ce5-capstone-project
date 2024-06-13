FROM python:3.10.14-slim-bookworm

RUN apt-get update && apt-get install -y curl

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app/app.py"]