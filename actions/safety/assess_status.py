from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from ..templates.buttons import get_status_buttons, get_safe_user_buttons
from ..utils.emergency_helpers import get_emergency_type


class ActionAssessStatus(Action):
    
    def name(self) -> Text:
        return "action_assess_status"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            events = []

            injury_status = tracker.get_slot('injury_status')
            status_asked = tracker.get_slot('status_asked')
            latest_intent = tracker.latest_message.get('intent', {}).get('name', '')
            latest_text = tracker.latest_message.get('text', '').lower()

            status_intents = ['report_safe', 'report_injured', 'report_trapped', 'inform_status', 'affirm', 'deny']
            
            # If status was asked and we got nlu_fallback, try to extract status from text
            if latest_intent == 'nlu_fallback' and status_asked:
                # Try to extract status from text even if NLU didn't classify it correctly
                negations = ['not', 'no', "n't", "aren't", "isn't", "don't", 'never']
                safe_indicators = ['safe', 'fine', 'okay', 'ok', 'good', 'well', 'alright', "i'm all set"]
                injury_indicators = ['injured', 'hurt', 'bleeding', 'wounded', 'broken', 'i\'m injured', 'i am injured']
                trapped_indicators = ['trapped', 'i\'m trapped', 'we\'re trapped', 'i am trapped', 'we are trapped', 'stuck', 'can\'t get out']

                has_negation = any(word in latest_text for word in negations)
                has_safe = any(word in latest_text for word in safe_indicators)
                has_injury = any(word in latest_text for word in injury_indicators)
                has_trapped = any(phrase in latest_text for phrase in trapped_indicators)

                if has_trapped:
                    injury_status = 'trapped'
                elif has_negation and has_injury:
                    injury_status = 'safe'
                elif has_negation and has_safe:
                    injury_status = 'injured'
                elif has_injury:
                    injury_status = 'injured'
                elif has_safe:
                    injury_status = 'safe'
                else:
                    # Can't determine status, return empty to trigger fallback
                    return []
            
            if latest_intent not in status_intents and latest_intent != 'nlu_fallback':
                return []

            if latest_intent == 'report_safe' or latest_intent == 'deny':
                injury_status = 'safe'
            elif latest_intent == 'report_injured':
                injury_status = 'injured'
            elif latest_intent == 'report_trapped':
                injury_status = 'trapped'
            elif latest_intent == 'affirm':
                if status_asked:
                    recent_bot_messages = [e.get('text', '').lower() for e in tracker.events if e.get('event') == 'bot' and e.get('text')]
                    if any('injured' in msg or 'danger' in msg for msg in recent_bot_messages[-3:]):
                        injury_status = 'injured'
                    else:
                        injury_status = 'safe'
                else:
                    injury_status = 'safe'
            
            if not injury_status and latest_intent in status_intents:
                negations = ['not', 'no', "n't", "aren't", "isn't", "don't", 'never']
                safe_indicators = ['safe', 'fine', 'okay', 'ok', 'good', 'well', 'alright']
                injury_indicators = ['injured', 'hurt', 'bleeding', 'wounded', 'broken']
                trapped_indicators = ['trapped', 'i\'m trapped', 'we\'re trapped', 'i am trapped', 'we are trapped']

                has_negation = any(word in latest_text for word in negations)
                has_safe = any(word in latest_text for word in safe_indicators)
                has_injury = any(word in latest_text for word in injury_indicators)
                has_trapped = any(phrase in latest_text for phrase in trapped_indicators)

                if has_trapped:
                    injury_status = 'trapped'
                elif has_negation and has_injury:
                    injury_status = 'safe'
                elif has_negation and has_safe:
                    injury_status = 'injured'
                elif has_injury:
                    injury_status = 'injured'
                elif has_safe:
                    injury_status = 'safe'
                else:
                    injury_status = 'unclear'
            elif not injury_status:
                return []
            
            events.append(SlotSet("injury_status", injury_status))

            if injury_status in ['injured', 'trapped']:
                events.append(SlotSet("escalation_required", True))
            elif injury_status == 'unclear':
                events.append(SlotSet("escalation_required", False))
                message = "🤔 **I need to clarify your status**\n\n"
                message += "I couldn't determine if you're safe, injured, or trapped.\n\n"
                message += "**Please select one of the options below so I can provide the right assistance:**\n\n"
                message += "⚠️ **If you're in immediate danger, select 'I'm injured' or 'I'm trapped'**"
                dispatcher.utter_message(text=message, buttons=get_status_buttons())
            else:
                events.append(SlotSet("escalation_required", False))
                emergency_type = get_emergency_type(tracker)
                district = tracker.get_slot('district')
                
                safe_message = (
                    "✅ **Good, you're safe!**\n\n"
                    "Please follow the safety instructions provided above. Call **112** if your situation changes.\n\n"
                    "**What would you like to do next?**"
                )
                dispatcher.utter_message(text=safe_message, buttons=get_safe_user_buttons())
                
                # For earthquake, if user is safe, go directly to conclusion (no location needed)
                # Location is only needed for injured/trapped users

        except Exception as e:
            return []

        return events

