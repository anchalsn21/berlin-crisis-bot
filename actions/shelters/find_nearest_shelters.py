"""
Find Nearest Shelters Action
Finds and displays nearest emergency shelters for user's district.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from ..utils.constants import EMERGENCY_DATA
from ..utils.delays import add_message_delay
from ..templates.messages import format_shelter_info, format_emergency_contacts


class ActionFindNearestShelters(Action):
    """Finds and displays nearest emergency shelters."""
    
    def name(self) -> Text:
        return "action_find_nearest_shelters"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            district = tracker.get_slot('district')
            shelters_shown = tracker.get_slot('shelters_shown')
            emergency_type = tracker.get_slot('emergency_type')
            
            if shelters_shown:
                return []

            if not district:
                dispatcher.utter_message(text="I need your location to find nearby shelters. Please tell me your Berlin district.")
                return []
            
            shelters = EMERGENCY_DATA.get('shelters', {}).get(district, [])
            
            if not shelters:
                dispatcher.utter_message(text=f"⚠️ No specific shelters listed for {district}. Please call **112** for the nearest emergency shelter or evacuation point.")
                dispatcher.utter_message(text=format_emergency_contacts())
                from rasa_sdk.events import SlotSet
                return [SlotSet("shelters_shown", True)]
            
            message = format_shelter_info(district, shelters)
            dispatcher.utter_message(text=message)
            add_message_delay(1.0)
            
            from rasa_sdk.events import SlotSet
            events = [SlotSet("shelters_shown", True)]
            
            return events
        except Exception as e:
            dispatcher.utter_message(text="⚠️ Unable to retrieve shelter information. Please call **112** for emergency assistance.")
            return []

