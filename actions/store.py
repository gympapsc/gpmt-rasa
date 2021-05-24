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
        # fjson_data = json.dumps(data)
        # self.redis_client.publish(action, fjson_data)
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

    def create_micturition(self, userid, date):
        self.dispatch("ADD_MICTURITION", {
            "user": userid,
            "date": date
        })

    def create_drinking(self, userid, date, amount):
        self.dispatch("ADD_DRINKING", {
            "user": userid,
            "date": date,
            "amount": amount
        })
    
    def save_answer(self, userid, question_id, answer):
        self.dispatch("ANSWER_QUESTION", {
            "user": userid,
            "answer": answer,
            "question": question_id
        })

    def get_next_question(self, question_id, answer):
        # curr_question = self.mongodb["questionnaire"].find_one({ "_id": ObjectId(question_id)})

        # logger.debug(list(curr_question["next"]))

        # for n in curr_question["next"]:
        #     # TODO handle complex conditions
        #     if n["condition"] == answer:
        #         return self.mongodb["questionnaire"].find_one({ "_id": n["question"] })
        pass

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
