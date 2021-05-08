import redis
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

redis_client = redis.Redis(
    host="gpmt-redis.default.svc.cluster.local"
)

mongo_client = MongoClient(
    "mongodb://gpmt-mongodb.default.svc.cluster.local"
)


class Store:
    def __init__(self):
        self.p = redis_client.pubsub()
        self.mongodb = mongo_client["gpmt"]

    def dispatch(self, action="", data=None):
        fjson_data = json.dumps(data)
        redis_client.publish(action, fjson_data)

    def get_micturition(self, userid=""):
        entry = self.mongodb["micturition"].find({
            "user": ObjectId(userid)
        })
        return entry

    def get_drinking(self, userid=""):
        entry = self.mongodb["micturition"].find({
            "user": ObjectId(userid)
        })
        return entry

    def create_micturition(self, userid, date):
        self.dispatch("ADD_MICURITION", {
            "user": userid,
            "date": date
        })

    def create_drinking(self, userid, date, amount):
        self.dispatch("ADD_DRINKING", {
            "user": userid,
            "date": date,
            "amount": amount
        })

    # def edit_micturition(self, userid="", id):
    #     pass

    # def edit_drinking(self, userid=""):
    #     pass

    # def delete_micturition(self, userid="", mictid=""):
    #     pass

    # def delete_drinking(self, userid="", drinkid=""):
    #     pass