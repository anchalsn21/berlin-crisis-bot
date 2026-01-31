from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from ..utils.constants import EMERGENCY_DATA
from ..templates.messages import format_shelter_info, format_emergency_contacts
from ..templates.buttons import get_safe_user_buttons


class ActionFindNearestShelters(Action):
    
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
                from rasa_sdk.events import FollowupAction
                dispatcher.utter_message(text="📍 I need your location to find nearby shelters.")
                return [FollowupAction("utter_ask_location")]
            
            shelters = EMERGENCY_DATA.get('shelters', {}).get(district, [])
            
            if not shelters:
                dispatcher.utter_message(text=f"⚠️ No specific shelters listed for {district}. Please call **112** for the nearest emergency shelter or evacuation point.")
                dispatcher.utter_message(text=format_emergency_contacts())
                dispatcher.utter_message(text="**What would you like to do next?**", buttons=get_safe_user_buttons())
                from rasa_sdk.events import SlotSet
                return [SlotSet("shelters_shown", True)]
            
            message = format_shelter_info(district, shelters)
            dispatcher.utter_message(text=message)
            dispatcher.utter_message(text="**What would you like to do next?**", buttons=get_safe_user_buttons())
            
            from rasa_sdk.events import SlotSet
            events = [SlotSet("shelters_shown", True)]
            
            return events
        except Exception as e:
            dispatcher.utter_message(text="⚠️ Unable to retrieve shelter information. Please call **112** for emergency assistance.")
            return []

