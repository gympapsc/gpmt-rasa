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

class ActionAddDrinking(Action):

    def name(self):
        return "action_add_drinking"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        date = tracker.get_slot("time")
        amount = tracker.get_slot("amount")
        drinking = tracker.get_slot("drinking")
        dispatcher.utter_message(json_message={
            "type": "ADD_DRINKING",
            "payload": {
                "user": tracker.sender_id,
                "date": date,
                "amount": amount,
                "type": drinking
            }
        })

        dispatcher.utter_message(response="utter_confirm")
        return [
            SlotSet(key="time"), 
            SlotSet(key="amount")
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
