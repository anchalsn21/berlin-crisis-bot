from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction


class ActionEscalateEmergency(Action):
    
    def name(self) -> Text:
        return "action_escalate_emergency"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        events = [SlotSet("escalation_required", True)]
        
        district = tracker.get_slot('district')
        emergency_type = tracker.get_slot('emergency_type')
        
        if emergency_type == 'earthquake' and not district:
            events.append(FollowupAction("utter_ask_location"))
        
        return events




