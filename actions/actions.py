from datetime import datetime

from typing import Any, Text, Dict, List
from bson.codec_options import CodecOptions

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

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

class ValidateQuestionnaireForm(FormValidationAction):

    def name(self):
        return "validate_form_questionnaire"
    
    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        question_id = tracker.get_slot("question_id")
        if question_id is None:
            question = store.get_root_question()
        else:
            last_question = store.get_question(question_id)
            answer = tracker.get_slot(str(last_question["name"]))
            store.save_answer(tracker.sender_id, question_id, answer)
            question = store.get_next_question(question_id, answer)
            if question is None:
                return slots_mapped_in_domain
        
        tracker.add_slots(SlotSet("question_id", str(question["_id"])))
        return slots_mapped_in_domain.append(question["name"])