from datetime import datetime

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

from actions.store import Store

import logging

logger = logging.getLogger(__name__)

logger.info("TEST")

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
        logger.info("QUESTION ID %s", question_id)
        if question_id is None:
            question = store.get_root_question()
            logger.info("QUESTION %s", question["name"])
        else:
            last_question = store.get_question(question_id)
            logger.info("LAST QUESTION %s", last_question["name"])
            answer = tracker.get_slot(str(last_question["name"]))
            if not answer is None:
                logger.info("LAST ANSWER %s", answer)
                store.save_answer(tracker.sender_id, question_id, answer)
                question = store.get_next_question(question_id, answer)
                if question is None:
                    return slots_mapped_in_domain
                logger.info("NEXT QUESTION %s", question["name"])
            else:
                question = last_question

        logger.info("ADD SLOT %s", str(question["_id"]))
        tracker.add_slots([SlotSet("question_id", str(question["_id"]))])
        slots_mapped_in_domain.append(question["name"])
        return slots_mapped_in_domain
    
    def entity_is_desired(
        slot_mapping: Dict[Text, Any],
        slot: Text,
        entity_type_of_slot_to_fill: Text, 
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> bool:
        logger.info("IS ENTITY TYPE %s of SLOT %s desired", slot, entity_type_of_slot_to_fill)
        return True

    # async def extract_disease(
    #     self, 
    #     dispatcher: CollectingDispatcher, 
    #     tracker: Tracker, 
    #     domain: Dict
    # ):
    #     text_of_last_user_message = tracker.latest_message.get("text")
    #     logger.info("USER MESSAGE %s", text_of_last_user_message)
    #     return { "disease": text_of_last_user_message }