import re
import requests
from typing import Any, Dict, List, Text, Optional, Tuple

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

from ..utils.constants import BERLIN_DISTRICTS, BERLIN_POSTCODES, EMERGENCY_DATA, STANDARD_DISTRICTS
from ..utils.emergency_helpers import fuzzy_match_district, get_emergency_type
from ..templates.messages import format_emergency_contacts


class ActionValidateLocation(Action):
    
    def name(self) -> Text:
        return "action_validate_location"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        events = []
        
        latest_intent = tracker.latest_message.get('intent', {}).get('name', '')
        latest_intent_confidence = tracker.latest_message.get('intent', {}).get('confidence', 0.0)
        
        try:
            location_validated = tracker.get_slot('location_validated')
            district = tracker.get_slot('district')
            
            location_just_validated = False
            for event in reversed(tracker.events[-10:]):
                if event.get('event') == 'slot':
                    if event.get('name') == 'location_validated' and event.get('value') is True:
                        location_just_validated = True
                        break
                elif event.get('event') == 'bot':
                    text = event.get('text', '')
                    if 'Location confirmed' in text or 'location confirmed' in text.lower():
                        location_just_validated = True
                        break
            
            if (location_validated and district) or location_just_validated:
                return []
            
            latest_message_lower = tracker.latest_message.get('text', '').strip().lower()
            status_was_asked = tracker.get_slot('status_asked')
            location_was_asked = False
            entities = tracker.latest_message.get('entities', [])
            has_location_entity = any(e.get('entity') in ['district', 'postcode'] for e in entities)
            
            for event in reversed(tracker.events[-15:]):
                if event.get('event') == 'action':
                    if event.get('name', '') == 'utter_ask_location':
                        location_was_asked = True
                        break
                elif event.get('event') == 'bot':
                    text = event.get('text', '').lower()
                    if any(phrase in text for phrase in ['which area', 'which district', 'your location', 'where are you', 'berlin district', 'postcode', 'select your district', 'i need to know your location']):
                        location_was_asked = True
                        break
            
            if latest_intent not in ['inform_location', 'share_gps_location']:
                if not location_was_asked:
                    return []
                
                if not has_location_entity:
                    is_known_district = False
                    for std_district in STANDARD_DISTRICTS:
                        if latest_message_lower == std_district.lower():
                            is_known_district = True
                            break
                    
                    if not is_known_district:
                        postcode_match = re.search(r'\b(1[0-4]\d{3})\b', latest_message_lower)
                        if not postcode_match:
                            return []
            
            if status_was_asked and not location_was_asked and not has_location_entity:
                return []
            
            escalation_required = tracker.get_slot('escalation_required')
            if escalation_required:
                return []
            
            latest_message_lower = tracker.latest_message.get('text', '').strip().lower()
            status_indicators = ['i\'m safe', 'i am safe', 'we are safe', 'everyone is safe', 'i\'m injured', 'i am injured', 'i\'m trapped', 'i am trapped', 'i\'m okay', 'i\'m fine', 'we\'re safe', 'not injured', 'not hurt', 'no injuries']
            
            if status_was_asked and any(indicator in latest_message_lower for indicator in status_indicators):
                return []
            
            acknowledgment_words = ['ok', 'okay', 'got it', 'understood', 'i understand', 'alright', 'all right', 'fine', 'sure', 'yes', 'yeah']
            if any(word == latest_message_lower for word in acknowledgment_words):
                return []
            
            if not location_was_asked and not has_location_entity:
                if any(indicator in latest_message_lower for indicator in status_indicators):
                    return []
                
                non_location_phrases = [
                    'help', 'what should i do', 'what do i do', 'i need help',
                    'i don\'t know', 'not sure', 'maybe', 'i think',
                    'how are you', 'are you there', 'hello', 'hi',
                    'thanks', 'thank you', 'appreciate it'
                ]
                if any(phrase in latest_message_lower for phrase in non_location_phrases):
                    return []
                
                if len(latest_message_lower.split()) <= 2 and not any(char.isdigit() for char in latest_message_lower):
                    is_known_district = False
                    for std_district in STANDARD_DISTRICTS:
                        if latest_message_lower == std_district.lower():
                            is_known_district = True
                            break
                    
                    if not is_known_district:
                        return []
            
            latest_message = tracker.latest_message.get('text', '').strip()
            
            extracted_district = self._process_gps_coordinates(tracker, dispatcher, latest_intent)
            
            if not extracted_district:
                extracted_district, postcode = self._extract_location_from_message(tracker, latest_message, entities)
            else:
                postcode = None
            
            if postcode and not extracted_district:
                extracted_district = BERLIN_POSTCODES.get(postcode)
            
            if location_validated and district and extracted_district:
                if extracted_district.lower() == district.lower():
                    return []
            
            if extracted_district:
                validated_district, confidence = self._validate_and_fuzzy_match(extracted_district, dispatcher)
                if not validated_district:
                    return self._handle_invalid_location(dispatcher, tracker, events)
                
                events.append(SlotSet("location_retry_count", 0))
                events.append(SlotSet("district", validated_district))
                events.append(SlotSet("location_validated", True))
                
                confidence_emoji = "✅" if confidence >= 0.9 else "🤔"
                dispatcher.utter_message(text=f"{confidence_emoji} Location confirmed: **{validated_district}**")
                
                self._trigger_shelter_finding(tracker, events, validated_district)
            else:
                if location_validated and district:
                    return []
                return self._handle_invalid_location(dispatcher, tracker, events)
                
        except Exception as e:
            dispatcher.utter_message(text="⚠️ There was an error processing your location. Please try again with a Berlin district name or postcode.")
            events.append(SlotSet("location_validated", False))
        
        if not events and latest_intent in ['inform_location', 'share_gps_location']:
            events.append(SlotSet("location_validated", False))
        
        return events
    
    def _process_gps_coordinates(self, tracker: Tracker, dispatcher: CollectingDispatcher, latest_intent: str):
        """Process GPS coordinates from metadata."""
        if latest_intent != 'share_gps_location':
            return None
        
        metadata = tracker.latest_message.get('metadata', {})
        location_coords = metadata.get('location_coords') if metadata else None
        
        if not location_coords:
            return None
        
        try:
            lat = location_coords.get('lat')
            lng = location_coords.get('lng')
            if not lat or not lng:
                return None
            
            nominatim_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&addressdetails=1&accept-language=en"
            headers = {'User-Agent': 'Berlin-Emergency-Chatbot/1.0'}
            response = requests.get(nominatim_url, headers=headers, timeout=5)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            address = data.get('address', {})
            city = address.get('city') or address.get('town') or ''
            
            if 'berlin' not in city.lower():
                dispatcher.utter_message(text="⚠️ Your GPS location appears to be outside Berlin. Please provide a Berlin district manually.")
                return None
            
            suburb = address.get('suburb') or address.get('neighbourhood') or address.get('city_district') or ''
            district = None
            
            if suburb:
                matched_district, conf, _ = fuzzy_match_district(suburb)
                if matched_district and conf >= 0.6:
                    district = matched_district
                else:
                    suburb_lower = suburb.lower()
                    for std_district in STANDARD_DISTRICTS:
                        if suburb_lower in std_district.lower() or std_district.lower() in suburb_lower:
                            district = std_district
                            break
            
            if not district:
                postcode_str = address.get('postcode', '')
                if postcode_str and len(postcode_str) == 5:
                    district = BERLIN_POSTCODES.get(postcode_str)
            
            if not district:
                district = 'Mitte'
            
            return district
            
        except Exception as e:
            return None
    
    def _extract_location_from_message(self, tracker: Tracker, latest_message: str, entities: List[Dict]):
        """Extract district and postcode from message."""
        district = None
        postcode = None
        
        for entity in entities:
            if entity.get('entity') == 'district':
                district = entity.get('value')
            elif entity.get('entity') == 'postcode':
                postcode = entity.get('value')
        
        if not district:
            district = tracker.get_slot('district')
        if not postcode:
            postcode = tracker.get_slot('postcode')
        
        if not district and not postcode:
            postcode_match = re.search(r'\b(1[0-4]\d{3})\b', latest_message)
            if postcode_match:
                postcode = postcode_match.group(1)
            else:
                matched_district, confidence, suggestions = fuzzy_match_district(latest_message)
                if matched_district and confidence >= 0.6:
                    district = matched_district
                elif suggestions:
                    district = suggestions[0]
                else:
                    latest_lower = latest_message.lower().strip()
                    if latest_lower in BERLIN_DISTRICTS:
                        district = BERLIN_DISTRICTS[latest_lower]
                    else:
                        for std_district in STANDARD_DISTRICTS:
                            if latest_lower == std_district.lower():
                                district = std_district
                                break
        
        return district, postcode
    
    def _validate_and_fuzzy_match(self, district: str, dispatcher: CollectingDispatcher):
        """Validate and fuzzy match district name."""
        matched_district, conf, suggestions = fuzzy_match_district(district)
        
        if matched_district and conf >= 0.8:
            return matched_district, conf
        elif matched_district and conf >= 0.6:
            dispatcher.utter_message(text=f"🤔 Did you mean **{matched_district}**?")
            return matched_district, conf
        elif suggestions:
            suggestions_text = ", ".join(suggestions[:3])
            dispatcher.utter_message(text=f"⚠️ Location not recognized. Did you mean: {suggestions_text}?")
            return None, 0.0
        
        return district, 1.0
    
    def _handle_invalid_location(self, dispatcher: CollectingDispatcher, tracker: Tracker, events: List):
        """Handle invalid location input."""
        retry_count = tracker.get_slot('location_retry_count') or 0
        max_retries = 3
        
        if retry_count >= max_retries:
            events.append(SlotSet("location_validated", False))
            events.append(SlotSet("location_retry_count", 0))
            
            message = "⚠️ **I couldn't recognize your location after multiple attempts.**\n\n"
            message += "**Please try one of these options:**\n\n"
            message += "1. **Call 112** for immediate emergency assistance - they can help you directly\n"
            message += "2. **Use GPS location** if available (click 'Share GPS Location' button)\n"
            message += "3. **Type a Berlin district name** (e.g., Mitte, Kreuzberg, Charlottenburg)\n"
            message += "4. **Type a Berlin postcode** (e.g., 10115, 10961)\n\n"
            message += "**Emergency Contacts:**\n"
            message += format_emergency_contacts()
            
            dispatcher.utter_message(text=message)
            return events
        else:
            new_retry_count = retry_count + 1
            events.append(SlotSet("location_retry_count", new_retry_count))
            events.append(SlotSet("location_validated", False))
            
            message = f"⚠️ I couldn't recognize that location (attempt {new_retry_count}/{max_retries}).\n\n"
            message += "**Please provide:**\n"
            message += "• A Berlin district name (e.g., Mitte, Kreuzberg, Charlottenburg)\n"
            message += "• A Berlin postcode (e.g., 10115, 10961)\n"
            message += "• Or use the 'Share GPS Location' button if available"
            
            dispatcher.utter_message(text=message)
            dispatcher.utter_message(response="utter_ask_location")
            return events
    
    def _trigger_shelter_finding(self, tracker: Tracker, events: List, district: str):
        emergency_type = get_emergency_type(tracker)
        instructions_provided = tracker.get_slot('instructions_provided')
        status_asked = tracker.get_slot('status_asked')
        injury_status = tracker.get_slot('injury_status')
        
        if not emergency_type:
            events.append(FollowupAction("utter_ask_emergency_type"))
            return
        
        if emergency_type == 'earthquake':
            if status_asked and injury_status == 'safe':
                events.append(FollowupAction("action_find_nearest_shelters"))
        elif emergency_type in ['flood', 'fire']:
            if not instructions_provided:
                events.append(FollowupAction("action_provide_safety_instructions"))
            else:
                events.append(FollowupAction("action_find_nearest_shelters"))

