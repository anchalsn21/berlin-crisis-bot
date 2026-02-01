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
            
            # Check if this is an explicit request to show shelters (via request_shelter_info intent)
            # or if action_handle_shelter_request was just called (which resets shelters_shown)
            # If so, allow showing shelters again even if they were shown before
            latest_intent = tracker.latest_message.get('intent', {}).get('name', '')
            is_explicit_request = latest_intent == 'request_shelter_info'
            
            # Also check if action_handle_shelter_request was just called (indicates explicit request)
            was_handle_shelter_request_called = False
            for event in reversed(tracker.events[-5:]):
                if event.get('event') == 'action' and event.get('name') == 'action_handle_shelter_request':
                    was_handle_shelter_request_called = True
                    break
            
            # Only skip if shelters were shown AND this is not an explicit request
            if shelters_shown and not is_explicit_request and not was_handle_shelter_request_called:
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

