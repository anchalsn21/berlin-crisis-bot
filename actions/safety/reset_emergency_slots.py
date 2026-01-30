"""
Reset Emergency Slots Action
Resets emergency-related slots when a new emergency is reported.
Preserves location information while clearing emergency-specific data.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionResetEmergencySlots(Action):
    """
    Reset emergency-related slots when a new emergency is reported.
    Preserves location information (district, postcode, location_validated, etc.)
    while clearing emergency-specific slots.
    """
    
    def name(self) -> Text:
        return "action_reset_emergency_slots"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        events = []
        
        # Reset emergency-related slots
        # Keep location information intact
        events.append(SlotSet("instructions_provided", False))
        events.append(SlotSet("shelters_shown", False))
        events.append(SlotSet("escalation_required", False))
        events.append(SlotSet("injury_status", None))
        events.append(SlotSet("status_asked", False))
        
        # Note: emergency_type will be set automatically by domain mappings
        # based on the new intent (report_earthquake, report_flood, report_fire)
        
        return events
