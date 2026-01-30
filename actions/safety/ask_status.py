from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionAskStatus(Action):
    
    def name(self) -> Text:
        return "action_ask_status"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        status_asked = tracker.get_slot('status_asked')
        injury_status = tracker.get_slot('injury_status')
        
        if status_asked and injury_status:
            return []
        
        dispatcher.utter_message(response="utter_ask_status")
        
        return [SlotSet("status_asked", True)]



