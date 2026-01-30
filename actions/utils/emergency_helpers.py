from typing import Optional, Tuple, List
from difflib import SequenceMatcher

from rasa_sdk import Tracker

from .constants import BERLIN_DISTRICTS, BERLIN_POSTCODES, STANDARD_DISTRICTS


def fuzzy_match_district(input_text: str, threshold: float = 0.7) -> Tuple[Optional[str], float, List[str]]:
    input_lower = input_text.lower().strip()

    if input_lower in BERLIN_DISTRICTS:
        return BERLIN_DISTRICTS[input_lower], 1.0, []

    for district in STANDARD_DISTRICTS:
        if input_lower == district.lower():
            return district, 1.0, []

    if input_lower.isdigit() and len(input_lower) == 5:
        if input_lower in BERLIN_POSTCODES:
            return BERLIN_POSTCODES[input_lower], 1.0, []

    best_match = None
    best_score = 0
    suggestions = []

    for variation, district in BERLIN_DISTRICTS.items():
        ratio_score = SequenceMatcher(None, input_lower, variation).ratio()
        partial_score = SequenceMatcher(None, input_lower, variation).quick_ratio()

        score = max(ratio_score, partial_score)

        if score >= threshold:
            if score > best_score:
                best_score = score
                best_match = district
                suggestions = [district]
            elif score == best_score and district not in suggestions:
                suggestions.append(district)

    return best_match, best_score, suggestions


def get_emergency_type(tracker: Tracker) -> Optional[str]:
    emergency_type = tracker.get_slot('emergency_type')
    if emergency_type:
        emergency_lower = emergency_type.lower()
        if emergency_lower in ['fire', 'wildfire']:
            return 'fire'
        return emergency_lower

    for event in reversed(tracker.events):
        if event.get('event') == 'user':
            intent = event.get('parse_data', {}).get('intent', {}).get('name', '')
            if intent == 'report_earthquake':
                return 'earthquake'
            elif intent == 'report_flood':
                return 'flood'
            elif intent == 'report_fire':
                return 'fire'

            entities = event.get('parse_data', {}).get('entities', [])
            for entity in entities:
                if entity.get('entity') == 'emergency_type':
                    entity_value = entity.get('value', '').lower()
                    if entity_value in ['fire', 'wildfire']:
                        return 'fire'
                    elif entity_value in ['earthquake', 'flood', 'fire']:
                        return entity_value

    return None

