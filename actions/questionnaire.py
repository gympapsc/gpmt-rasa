from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, AllSlotsReset
from rasa_sdk.forms import FormValidationAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher

from actions.store import Store

import logging

logger = logging.getLogger(__name__)
store = Store()

class ValidateQuestionnaireForm(FormValidationAction):

    def name(self):
        return "validate_form_questionnaire"
    
    async def run(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ):
        validation_events = await self.validate(dispatcher, tracker, domain)

        question_id = tracker.get_slot("question_id")
        logger.info("QUESTION ID %s", question_id)
        if question_id is None:
            question = store.get_root_question()
            logger.info("QUESTION %s", question["name"])
        else:
            last_question = store.get_question(question_id)
            logger.info("LAST QUESTION %s", last_question["name"])
            answer = tracker.get_slot(str(last_question["name"]))
            if answer is None:
                question = last_question
            else:
                logger.info("LAST ANSWER %s", answer)
                if last_question["type"] == "bool":
                    if answer.lower() == "ja":
                        answer = True
                    else:
                        answer = False


                dispatcher.utter_message(json_message={
                    "type": "ANSWER_QUESTION",
                    "payload": {
                        "user": tracker.sender_id,
                        "question": question_id,
                        "answer": answer
                    }
                })
                
                question = store.get_next_question(question_id, answer)

                if question is None:
                    return [
                        SlotSet(REQUESTED_SLOT, None)
                    ]
                    
                logger.info("NEXT QUESTION %s", question["name"])

        logger.info("ADD SLOT %s", str(question["_id"]))

        if question["type"] == "radio":
            dispatcher.utter_message(buttons=[
                { "payload": option["text"], "title": option["text"] } 
                for option in question["options"]
            ])
        elif question["type"] == "bool":
            dispatcher.utter_message(buttons=[
                { "payload": "Ja", "title": "Ja" }, { "payload": "Nein", "title": "Nein" }
            ])
        
        return validation_events + [
            SlotSet("question_id", str(question["_id"])),
            SlotSet(REQUESTED_SLOT, question["name"])
        ]
    
    def validate_disease(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        logger.info("SLOT VALUE %s", slot_value)
        return {"disease": slot_value}

class ActionExitQuestionnaire(Action):

    def name(self):
        return "action_exit_questionnaire"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        return [ SlotSet("questionnaire", False) ]
