from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from actions.store import Store

# store = Store()


# class ActionQuestionnaire(Action):

#     def name(self):
#         return "action_questionnaire"
    
#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ):

#         question_id = tracker.get_slot("question_id")
#         if question_id is None:
#             question = store.get_root_question()
#             return [
#                 FollowupAction(name=question["name"]),
#                 SlotSet("questionnaire", True)
#             ]

#         answer = tracker.get_slot("answer")
#         store.save_answer(tracker.sender_id, answer, question_id)
#         question = store.get_next_question(question_id, answer)

#         if question is None:
#             dispatcher.utter_message(response="utter_questionnaire_finished")
#             return [
#                 SlotSet("questionnaire", False)
#             ]
#         return [
#             FollowupAction(name=question["name"]), 
#             SlotSet("question_id", question["_id"])
#         ]


# class ActionQuestionnaire(Action):

#     def name(self):
#         return "action_questionnaire"
    
#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ):

#         question_id = tracker.get_slot("question_id")
#         if question_id is None:
#             question = store.get_root_question()
#             return [
#                 FollowupAction(name=question["name"]),
#                 SlotSet("questionnaire", True),
#                 SlotSet("question_id", str(question["_id"])),
#                 SlotSet("answer")
#             ]

#         answer = tracker.get_slot("answer")
#         store.save_answer(tracker.sender_id, question_id, answer)
#         question = store.get_next_question(question_id, answer)

#         if question is None:
#             dispatcher.utter_message(response="utter_questionnaire_finished")
#             return [
#                 SlotSet("questionnaire", False),
#                 SlotSet("question_id"),
#                 SlotSet("answer")
#             ]
#         return [
#             FollowupAction(name=question["name"]), 
#             SlotSet("question_id", str(question["_id"])),
#             SlotSet("answer")
#         ]