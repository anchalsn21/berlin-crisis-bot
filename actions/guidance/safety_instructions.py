from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from ..utils.emergency_helpers import get_emergency_type
from ..utils.constants import EMERGENCY_DATA
from ..templates.messages import (
    format_safety_instructions,
    format_earthquake_instructions_immediate,
)
from ..templates.buttons import get_safe_user_buttons


class ActionProvideSafetyInstructions(Action):
    
    def name(self) -> Text:
        return "action_provide_safety_instructions"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        emergency_type = get_emergency_type(tracker)
        district = tracker.get_slot('district') or "your area"

        if not emergency_type:
            dispatcher.utter_message(text="⚠️ Please tell me what type of emergency you're experiencing (earthquake, flood, or fire).")
            return []
        
        instructions_provided = tracker.get_slot('instructions_provided')
        if instructions_provided:
            return []
        
        message = format_safety_instructions(emergency_type, district)
        dispatcher.utter_message(text=message)
        
        # Show buttons if this is an independent request (not part of main emergency flow)
        # In the main flow, shelters will be shown next with buttons, so we skip buttons here
        # Check if location was just validated (indicating main flow) vs independent request
        location_validated = tracker.get_slot('location_validated')
        shelters_shown = tracker.get_slot('shelters_shown')
        
        # Only show buttons if this is likely an independent request
        # (location not recently validated, or shelters already shown)
        if not location_validated or shelters_shown:
            dispatcher.utter_message(text="**What would you like to do next?**", buttons=get_safe_user_buttons())
        
        events = [SlotSet("instructions_provided", True)]
        
        return events


class ActionProvideEarthquakeInstructionsImmediate(Action):
    
    def name(self) -> Text:
        return "action_provide_earthquake_instructions_immediate"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            instructions_provided = tracker.get_slot('instructions_provided')
            if instructions_provided:
                return []
            
            message = format_earthquake_instructions_immediate()
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("instructions_provided", True),
                SlotSet("emergency_type", "earthquake")
            ]
        except Exception as e:
            dispatcher.utter_message(text="🏗️ **EARTHQUAKE EMERGENCY**\n\n🚨 **IMMEDIATE ACTIONS:**\n1. Drop, Cover, and Hold On\n2. Stay away from windows\n3. If outdoors, move to open area\n4. If in vehicle, pull over and stay inside\n\n**📋 AFTER:**\n1. Check for injuries\n2. Be prepared for aftershocks\n3. Listen to emergency broadcasts")
            return [
                SlotSet("instructions_provided", True),
                SlotSet("emergency_type", "earthquake")
            ]

