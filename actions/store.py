from pymongo import MongoClient
from bson.objectid import ObjectId
import json

import logging

logger = logging.getLogger(__name__)


class Store:
    def __init__(self):
        mongo_client = MongoClient(
            "mongodb://gpmtdb:aD3OP3ay1EXrS8NfT5Qs5kyZlb9FXMK9jcMfaefv48h84pT9RHrQjoFgSTnu9Fh8niMUNTysETPQTbzQThUADg==@gpmtdb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@gpmtdb@"
        )
        self.mongodb = mongo_client["gpmt"]

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
