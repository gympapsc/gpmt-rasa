FROM rasa/rasa

RUN mkdir channels
COPY ./channels ./channels
