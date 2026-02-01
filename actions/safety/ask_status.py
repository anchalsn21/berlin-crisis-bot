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
        
        # Send status question directly instead of using utterance response
        # This avoids the "utter_ask_status not used" warning from Rasa validator
        message = "**Are you injured or in immediate danger?**"
        buttons = [
            {"title": "✅ I'm safe", "payload": "I'm safe"},
            {"title": "🤕 I'm injured", "payload": "I'm injured"},
            {"title": "🆘 I'm trapped", "payload": "I'm trapped"}
        ]
        dispatcher.utter_message(text=message, buttons=buttons)
        
        return [SlotSet("status_asked", True)]



