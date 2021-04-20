# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hallo Welt!")

        return []


class ActionAddMicturition(Action):
    
    def name(self):
        return "action_add_micturition"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        r = requests.post(
            "gpmt-api.default.svc.cluster.local/micturition",
            data= {
                'date': '2021-01-01',
                'user': tracker.sender_id
            }
        )
        if r.status_code == 200:
            dispatcher.utter_message(text="Habs gespeichert")
        else:
            dispatcher.utter_message(text="Upps. Ein Fehler.")