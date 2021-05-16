from datetime import datetime

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from actions.store import Store

from actions.questionnaire import ActionQuestionnaire

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
        store.create_micturition(tracker.sender_id, date)

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
        store.create_drinking(tracker.sender_id, date, amount)

        dispatcher.utter_message(response="utter_confirm")
        return [
            SlotSet(key="time"), 
            SlotSet(key="amount")
        ]

