from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionResetEmergencySlots(Action):
    
    def name(self) -> Text:
        return "action_reset_emergency_slots"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        events = []
        
        events.append(SlotSet("instructions_provided", False))
        events.append(SlotSet("shelters_shown", False))
        events.append(SlotSet("escalation_required", False))
        events.append(SlotSet("injury_status", None))
        events.append(SlotSet("status_asked", False))
        # Reset location slots when starting a new emergency
        events.append(SlotSet("district", None))
        events.append(SlotSet("location_validated", False))
        events.append(SlotSet("location_retry_count", 0))
        events.append(SlotSet("postcode", None))
        
        return events
