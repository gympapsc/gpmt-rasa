FROM rasa/rasa-sdk:2.4.0

WORKDIR /app/actions
USER root
COPY . .
RUN pip install -r ./requirements.txt

WORKDIR /app
USER 1001
