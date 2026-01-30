from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionSessionStart(Action):
    
    def name(self) -> Text:
        return "action_session_start"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            SlotSet("location_validated", False),
            SlotSet("escalation_required", False),
            SlotSet("instructions_provided", False),
            SlotSet("shelters_shown", False),
            SlotSet("district", None),
            SlotSet("emergency_type", None),
            SlotSet("injury_status", None),
            SlotSet("status_asked", False),
            SlotSet("postcode", None),
            SlotSet("location_coords", None),
            SlotSet("location_retry_count", 0),
        ]

