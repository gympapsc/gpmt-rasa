import redis
import os
import threading
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

import logging

logger = logging.getLogger(__name__)


class Store:
    def __init__(self):
        self.actionStream = RedisStream(
            "actions",
            "gpmt-rasa-actions",
            os.environ["HOSTNAME"]
        )

        mongo_client = MongoClient(
            "mongodb://gpmt-mongodb.default.svc.cluster.local"
        )
        self.mongodb = mongo_client["gpmt"]

    def dispatch(self, action, data):
        self.actionStream.add(action, data)

    def get_micturition(self, userid):
        entry = self.mongodb["micturition"].find({
            "user": ObjectId(userid)
        })
        return entry

    def get_drinking(self, userid):
        entry = self.mongodb["micturition"].find({
            "user": ObjectId(userid)
        })
        return entry

    def get_next_question(self, question_id, answer):
        curr_question = self.mongodb["questionnaire"].find_one({ "_id": ObjectId(question_id)})
        
        if curr_question["type"] == "number":
            answer = int(answer)

        logger.debug(list(curr_question["next"]))

        for n in curr_question["next"]:
            question = self.mongodb["questionnaire"].find_one({ "_id": ObjectId(n) })
            
            if len(list(question["condition"])) == 0:
                return question

            for c in question["condition"]:
                if c["type"] == "true" and answer:
                    return question
                if c["type"] == "false" and not answer:
                    return question
                if c["type"] == "eq" and c["value"] == answer:
                    return question
                if c["type"] == "gt" and int(c["value"]) < answer:
                    return question
                if c["type"] == "lt" and int(c["value"]) > answer:
                    return question
                    

    def get_root_question(self):
        return self.mongodb["questionnaire"].find_one({ "root": True })

    def get_question(self, question_id):
        return self.mongodb["questionnaire"].find_one({ "_id": ObjectId(question_id)})

    def get_user_name(self, sender_id):
        return self.mongodb["users"].find_one({ "_id": ObjectId(sender_id) })["firstname"]

    # def edit_micturition(self, userid="", id):
    #     pass

    # def edit_drinking(self, userid=""):
    #     pass

    # def delete_micturition(self, userid="", mictid=""):
    #     pass

    # def delete_drinking(self, userid="", drinkid=""):
    #     pass

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

    def add(self, event, message):
        self.r.xadd(self.streamname, { 
            "type": event,
            "payload": json.dumps(message)
        })
