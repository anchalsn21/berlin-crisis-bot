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
        
        # Determine emergency type from latest intent or recent events
        # Check latest intent first, then check recent events if needed
        latest_intent = tracker.latest_message.get('intent', {}).get('name', '')
        emergency_type = None
        
        if latest_intent == 'report_earthquake':
            emergency_type = 'earthquake'
        elif latest_intent == 'report_flood':
            emergency_type = 'flood'
        elif latest_intent == 'report_fire':
            emergency_type = 'fire'
        else:
            # Check recent events for emergency report intent (in case action is called from story)
            for event in reversed(tracker.events[-10:]):
                if event.get('event') == 'user':
                    intent = event.get('parse_data', {}).get('intent', {}).get('name', '')
                    if intent == 'report_earthquake':
                        emergency_type = 'earthquake'
                        break
                    elif intent == 'report_flood':
                        emergency_type = 'flood'
                        break
                    elif intent == 'report_fire':
                        emergency_type = 'fire'
                        break
        
        # Set emergency type if detected, otherwise reset to None
        # This ensures emergency_type is set correctly when a new emergency is reported
        events.append(SlotSet("emergency_type", emergency_type))
        
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
