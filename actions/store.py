from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os

import logging

logger = logging.getLogger(__name__)


class Store:
    def __init__(self):
        mongo_client = MongoClient(
            os.environ["MONGO_URL"]
        )
        self.mongodb = mongo_client["gpmt"]

    def get_micturition(self, userid):
        entry = self.mongodb["Micturition"].find({
            "user": ObjectId(userid)
        })
        return entry

    def get_drinking(self, userid):
        entry = self.mongodb["Micturition"].find({
            "user": ObjectId(userid)
        })
        return entry

    def get_next_question(self, question_id, answer):
        curr_question = self.mongodb["Questionnaire"].find_one({ "_id": ObjectId(question_id)})
        
        if curr_question["type"] == "number":
            answer = int(answer)

        logger.debug(list(curr_question["next"]))

        for n in curr_question["next"]:
            question = self.mongodb["Questionnaire"].find_one({ "_id": ObjectId(n) })
            
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
        return self.mongodb["Questionnaire"].find_one({ "root": True })

    def get_question(self, question_id):
        return self.mongodb["Questionnaire"].find_one({ "_id": ObjectId(question_id)})

    def get_user_name(self, sender_id):
        return self.mongodb["Users"].find_one({ "_id": ObjectId(sender_id) })["firstname"]

    # def edit_micturition(self, userid="", id):
    #     pass

    # def edit_drinking(self, userid=""):
    #     pass

    # def delete_micturition(self, userid="", mictid=""):
    #     pass

    # def delete_drinking(self, userid="", drinkid=""):
    #     pass
