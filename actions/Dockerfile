FROM rasa/rasa-sdk:latest

WORKDIR /app
USER root
COPY . .
RUN pip install -r ./requirements.txt

USER 1001
