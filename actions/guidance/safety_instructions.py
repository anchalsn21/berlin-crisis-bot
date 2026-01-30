"""
Safety Instructions Actions
Provide emergency-specific safety instructions.
"""

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


class ActionProvideSafetyInstructions(Action):
    """Provides emergency-specific safety instructions."""
    
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
        
        events = [SlotSet("instructions_provided", True)]
        
        return events


class ActionProvideEarthquakeInstructionsImmediate(Action):
    """Provides earthquake safety instructions immediately."""
    
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

