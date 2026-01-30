"""
Handle Greet Action
Responds to greeting and asks for emergency type.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHandleGreet(Action):
    """Handles greeting intent."""
    
    def name(self) -> Text:
        return "action_handle_greet"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_ask_emergency_type")
        
        return []

