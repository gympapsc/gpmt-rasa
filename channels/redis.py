import asyncio
import inspect
import json
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

class RedisInputChannel(InputChannel):

    def __init__(self):
        self.redis_client = redis.Redis(
            host="gpmt-redis.default.svc.cluster.local",
            port=6379
        )
        self.p = self.redis_client.pubsub()

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

        async def on_message(message):
            m = json.loads(message["data"])
            output_channel = RedisOutputChannel()

            await on_new_message(
                UserMessage(
                    m["text"],
                    output_channel,
                    m["sender_id"],
                    input_channel=self.name(),
                    metadata={},
                )
            )

        self.p.subscribe(**{
            "ADD_USER_MESSAGE": on_message 
        })
        thread = self.p.run_in_thread(sleep_time=0.001)

        return custom_webhook

class RedisOutputChannel(OutputChannel):
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host="gpmt-redis.default.svc.cluster.local",
            port=6379
        )
        self.p = self.redis_client.pubsub()
    
    def name() -> Text:
        return "redisOutput"
    
    def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ):
        fjson_data = json.dumps({
            "sender_id": recipient_id,
            "text": text
        })
        self.redis_client.publish("ADD_BOT_MESSAGE", fjson_data)