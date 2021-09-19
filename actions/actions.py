from datetime import datetime

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from actions.store import Store

import logging

logger = logging.getLogger(__name__)

store = Store()

class ActionAddMicturition(Action):
    
    def name(self):
        return "action_add_micturition"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        date = tracker.get_slot("time")
        print(date)
        dispatcher.utter_message(json_message={
            "type": "ADD_MICTURITION",
            "payload": {
                "user": tracker.sender_id,
                "date": date
            }
        })

        dispatcher.utter_message(response="utter_confirm")
        return [SlotSet(key="time")]

class ActionAddHydration(Action):

    def name(self):
        return "action_add_hydration"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        date = tracker.get_slot("time")
        amount = tracker.get_slot("amount")
        hydration = tracker.get_slot("hydration")
        dispatcher.utter_message(json_message={
            "type": "ADD_hydration",
            "payload": {
                "user": tracker.sender_id,
                "date": date,
                "amount": amount,
                "type": hydration
            }
        })

        dispatcher.utter_message(response="utter_confirm")
        return [
            SlotSet(key="time"), 
            SlotSet(key="amount"),
            SlotSet(key="hydration")
        ]

class ActionAddNutrition(Action):

    def name(self):
        return "action_add_nutrition"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        date = tracker.get_slot("time")
        mass = tracker.get_slot("mass")
        nutrition = tracker.get_slot("nutrition")
        dispatcher.utter_message(json_message={
            "type": "ADD_NUTRITION",
            "payload": {
                "user": tracker.sender_id,
                "date": date,
                "mass": mass,
                "type": nutrition
            }
        })

        dispatcher.utter_message(response="utter_confirm")
        return [
            SlotSet(key="time"), 
            SlotSet(key="mass"),
            SlotSet(key="nutrition")
        ]

class ActionAddMedication(Action):

    def name(self):
        return "action_add_medication"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        date = tracker.get_slot("time")
        mass = tracker.get_slot("mass")
        substance = tracker.get_slot("substance")
        dispatcher.utter_message(json_message={
            "type": "ADD_MEDICATION",
            "payload": {
                "user": tracker.sender_id,
                "date": date,
                "substance": substance,
                "mass": mass
            }
        })

        dispatcher.utter_message(response="utter_confirm")
        return [
            SlotSet(key="time"), 
            SlotSet(key="mass"),
            SlotSet(key="substance")
        ]


class ActionAddStress(Action):

    def name(self):
        return "action_add_stress"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        date = datetime.now().isoformat()
        stresslevel = tracker.get_slot("stresslevel")
        dispatcher.utter_message(json_message={
            "type": "ADD_STRESS",
            "payload": {
                "user": tracker.sender_id,
                "date": date,
                "level": stresslevel
            }
        })

        dispatcher.utter_message(response="utter_confirm")
        return [
            SlotSet(key="time"),
            SlotSet(key="stresslevel")
        ]

class ActionInit(Action):

    def name(self):
        return "action_init"
    
    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        name = store.get_user_name(tracker.sender_id)

        return [
            SlotSet(key="name", value=name)
        ]

class ActionUpdateHeight(Action):

    def name(self):
        return "action_update_height"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        height = tracker.get_slot("height")

        dispatcher.utter_message(json_message={
            "type": "UPDATE_USER",
            "payload": {
                "height": height
            }
        })
        dispatcher.utter_message(response="utter_confirm")

        return [
            SlotSet(key="height")
        ]

class ActionUpdateWeight(Action):

    def name(self):
        return "action_update_weight"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        weight = tracker.get_slot("weight")

        dispatcher.utter_message(json_message={
            "type": "UPDATE_USER",
            "payload": {
                "weight": weight
            }
        })
        dispatcher.utter_message(response="utter_confirm")

        return [
            SlotSet(key="weight")
        ]

class ActionSignOut(Action):

    def name(self):
        return "action_signout"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        dispatcher.utter_message(json_message={
            "type": "SIGNOUT_USER"
        })

        return []
