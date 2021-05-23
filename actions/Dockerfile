FROM rasa/rasa-sdk:latest

WORKDIR /app/actions
USER root
COPY . .
RUN pip install -r ./requirements.txt

WORKDIR /app
USER 1001
