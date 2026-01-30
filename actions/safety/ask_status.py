"""
Ask Status Action
Asks user about their injury/safety status and sets status_asked slot.
Prevents duplicate status questions.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionAskStatus(Action):
    """
    Ask user about their injury/safety status.
    Sets status_asked slot to prevent duplicate questions.
    """
    
    def name(self) -> Text:
        return "action_ask_status"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Check if status was already asked
        status_asked = tracker.get_slot('status_asked')
        injury_status = tracker.get_slot('injury_status')
        
        if status_asked and injury_status:
            return []
        
        # Ask status question
        dispatcher.utter_message(response="utter_ask_status")
        
        # Set status_asked to True to prevent duplicate questions
        return [SlotSet("status_asked", True)]



