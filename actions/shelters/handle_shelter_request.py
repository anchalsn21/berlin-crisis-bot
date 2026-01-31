from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet

from .find_nearest_shelters import ActionFindNearestShelters


class ActionHandleShelterRequest(Action):
    
    def name(self) -> Text:
        return "action_handle_shelter_request"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        district = tracker.get_slot('district')
        emergency_type = tracker.get_slot('emergency_type')
        
        if not emergency_type:
            return [FollowupAction("utter_ask_emergency_type")]
        
        if not district:
            return [FollowupAction("utter_ask_location")]
        
        find_shelters_action = ActionFindNearestShelters()
        return find_shelters_action.run(dispatcher, tracker, domain)
