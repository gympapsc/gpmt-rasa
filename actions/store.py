import redis
from pymongo import MongoClient
from bson.objectid import ObjectId
import json




class Store:
    def __init__(self):
        self.redis_client = redis.Redis(
            host="gpmt-redis.default.svc.cluster.local",
            port=6379
        )

        mongo_client = MongoClient(
            "mongodb://gpmt-mongodb.default.svc.cluster.local"
        )
        self.p = self.redis_client.pubsub()
        self.mongodb = mongo_client["gpmt"]

    def dispatch(self, action, data):
        fjson_data = json.dumps(data)
        self.redis_client.publish(action, fjson_data)

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
        curr_question = self.mongodb["questions"].find_one({ "_id": question_id })

        for n in curr_question.next:
            # TODO handle complex conditions
            if n.condition == answer:
                return self.mongodb["questions"].find_one({ "_id": n.question })

    def get_root_question(self):
        return self.mongodb["questions"].find_one({ "root": True })

    # def edit_micturition(self, userid="", id):
    #     pass

    # def edit_drinking(self, userid=""):
    #     pass

    # def delete_micturition(self, userid="", mictid=""):
    #     pass

    # def delete_drinking(self, userid="", drinkid=""):
    #     pass