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
                
                # Check if this is an independent request (not part of main emergency flow)
                status_asked = tracker.get_slot('status_asked')
                instructions_provided = tracker.get_slot('instructions_provided')
                location_validated = tracker.get_slot('location_validated')
                is_main_flow = (status_asked and location_validated) or (instructions_provided and location_validated)
                
                if not is_main_flow:
                    dispatcher.utter_message(text="**What would you like to do next?**", buttons=get_safe_user_buttons())
                
                from rasa_sdk.events import SlotSet
                return [SlotSet("shelters_shown", True)]
            
            message = format_shelter_info(district, shelters)
            dispatcher.utter_message(text=message)
            
            # Check if this is an independent request (not part of main emergency flow)
            # Main flow indicators: status_asked is True (earthquake flow) or instructions_provided is True (flood/fire flow)
            status_asked = tracker.get_slot('status_asked')
            instructions_provided = tracker.get_slot('instructions_provided')
            location_validated = tracker.get_slot('location_validated')
            
            # If this is an independent request (not part of main flow), show conclusion
            # Main flow will call utter_anything_else separately, so we skip here to avoid duplicates
            is_main_flow = (status_asked and location_validated) or (instructions_provided and location_validated)
            
            if not is_main_flow:
                dispatcher.utter_message(text="**What would you like to do next?**", buttons=get_safe_user_buttons())
            
            from rasa_sdk.events import SlotSet
            events = [SlotSet("shelters_shown", True)]
            
            return events
        except Exception as e:
            dispatcher.utter_message(text="⚠️ Unable to retrieve shelter information. Please call **112** for emergency assistance.")
            return []

