from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction


class ActionEscalateEmergency(Action):
    
    def name(self) -> Text:
        return "action_escalate_emergency"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Just set the escalation flag - let stories/rules control the flow explicitly
        # This prevents FollowupAction from executing before critical instructions are shown
        return [SlotSet("escalation_required", True)]




