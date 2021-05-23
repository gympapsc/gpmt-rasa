import asyncio
import inspect
import json
import threading
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Optional, Callable, Awaitable, NoReturn
import redis

import rasa.utils.endpoints
from rasa.core.channels.channel import (
    InputChannel,
    OutputChannel,
    CollectingOutputChannel,
    UserMessage,
)



class RedisStream:

    def __init__(self, name, groupname, consumername):
        self.streamname = name
        self.groupname = groupname
        self.consumername = consumername

        self.r = redis.Redis(host="gpmt-redis.default.svc.cluster.local")
        try:
            self.r.xgroup_create(name, groupname, id="$", mkstream=True)
        except:
            pass


    def on(self, fn):
        def worker(r, streamname, groupname, consumername, fn):
            while True:
                messages = dict(
                    r.xreadgroup(
                        groupname, 
                        consumername, 
                        { streamname: ">", }, 
                        block=0, 
                        noack=True
                    )
                )[bytes(streamname, "utf-8")]
                for message in messages:
                    fn(message[0], message[1])
                    r.xack(streamname, groupname, message[0])

        x = threading.Thread(target=worker, args=(
            self.r,
            self.streamname,
            self.groupname,
            self.consumername,
            fn
        ), daemon=True)
        x.start()

        return fn

    def add(self, message):
        self.r.xadd(self.streamname, message)


redisStream = RedisStream("rasa", "gpmt-rasa", "0")

class RedisInputChannel(InputChannel):

    @staticmethod
    def name() -> Text:
        """Name of your custom channel."""
        return "redisInput"

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:

        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        
        @redisStream.on
        def on_message(id, message):
            output_channel = RedisOutputChannel()

            on_new_message(
                UserMessage(
                    message[b'text'].decode("utf-8"),
                    output_channel,
                    "hakim",
                    # m["sender_id"],
                    input_channel=self.name(),
                    metadata={},
                )
            )

        return custom_webhook

class RedisOutputChannel(OutputChannel):
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host="gpmt-redis.default.svc.cluster.local",
            port=6379
        )
        self.p = self.redis_client.pubsub()
    
    @staticmethod
    def name() -> Text:
        return "redisOutput"
    
    def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ):
        redisStream.add({"message": text, "recipient_id": recipient_id})
