FROM rasa/rasa:latest

COPY /data ./data
COPY config.yml .
COPY credentials.yml .
COPY domain.yml .
COPY endpoints.yml .

RUN rasa train

EXPOSE 5005

CMD ["run"]
