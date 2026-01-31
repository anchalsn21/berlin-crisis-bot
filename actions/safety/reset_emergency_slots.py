from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionResetEmergencySlots(Action):
    
    def name(self) -> Text:
        return "action_reset_emergency_slots"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Reset all emergency-related slots when user explicitly reports a new emergency
        # This is called when:
        # 1. User reports earthquake/flood/fire (via rules/stories)
        # 2. User clicks "Report Emergency" button (via request_emergency_type rule)
        # Slots persist across other interactions (Show Shelters, Safety Instructions, etc.)
        # until user explicitly starts a new emergency
        
        events = []
        
        # Reset emergency type - user is starting a new emergency
        events.append(SlotSet("emergency_type", None))
        
        # Reset flow state slots
        events.append(SlotSet("instructions_provided", False))
        events.append(SlotSet("shelters_shown", False))
        events.append(SlotSet("escalation_required", False))
        events.append(SlotSet("injury_status", None))
        events.append(SlotSet("status_asked", False))
        
        # Reset location slots when starting a new emergency
        events.append(SlotSet("district", None))
        events.append(SlotSet("location_validated", False))
        events.append(SlotSet("location_retry_count", 0))
        events.append(SlotSet("postcode", None))
        
        return events
