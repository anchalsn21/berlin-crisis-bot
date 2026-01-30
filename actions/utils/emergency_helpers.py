"""
Emergency helper functions for Berlin Crisis Response Chatbot.
Contains utility functions for emergency type detection and district matching.
"""

from typing import Optional, Tuple, List
from difflib import SequenceMatcher

from rasa_sdk import Tracker

from .constants import BERLIN_DISTRICTS, BERLIN_POSTCODES, STANDARD_DISTRICTS


def fuzzy_match_district(input_text: str, threshold: float = 0.7) -> Tuple[Optional[str], float, List[str]]:
    """
    Enhanced fuzzy match user input to Berlin district names.
    
    Args:
        input_text: User input text to match
        threshold: Minimum confidence score (default: 0.7)
    
    Returns:
        Tuple of (best_match, confidence_score, suggestions_list)
    """
    input_lower = input_text.lower().strip()

    # Direct match in variations dictionary
    if input_lower in BERLIN_DISTRICTS:
        return BERLIN_DISTRICTS[input_lower], 1.0, []

    # Check exact match against standard district names (case-insensitive)
    for district in STANDARD_DISTRICTS:
        if input_lower == district.lower():
            return district, 1.0, []

    # Check if it's a postcode
    if input_lower.isdigit() and len(input_lower) == 5:
        if input_lower in BERLIN_POSTCODES:
            return BERLIN_POSTCODES[input_lower], 1.0, []

    # Fuzzy match with multiple algorithms
    best_match = None
    best_score = 0
    suggestions = []

    for variation, district in BERLIN_DISTRICTS.items():
        # Try different matching algorithms
        ratio_score = SequenceMatcher(None, input_lower, variation).ratio()
        partial_score = SequenceMatcher(None, input_lower, variation).quick_ratio()

        # Use the best score
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
    """
    Get the current emergency type from slots or recent intents.
    
    Args:
        tracker: Rasa tracker instance
    
    Returns:
        Emergency type string ('earthquake', 'flood', 'fire') or None
    """
    # Check slot first
    emergency_type = tracker.get_slot('emergency_type')
    if emergency_type:
        # Handle aliases
        emergency_lower = emergency_type.lower()
        # Normalize fire/wildfire to 'fire'
        if emergency_lower in ['fire', 'wildfire']:
            return 'fire'
        return emergency_lower

    # Check recent intents
    for event in reversed(tracker.events):
        if event.get('event') == 'user':
            intent = event.get('parse_data', {}).get('intent', {}).get('name', '')
            if intent == 'report_earthquake':
                return 'earthquake'
            elif intent == 'report_flood':
                return 'flood'
            elif intent == 'report_fire':
                return 'fire'

            # Also check entities for emergency type
            entities = event.get('parse_data', {}).get('entities', [])
            for entity in entities:
                if entity.get('entity') == 'emergency_type':
                    entity_value = entity.get('value', '').lower()
                    # Normalize fire/wildfire to 'fire'
                    if entity_value in ['fire', 'wildfire']:
                        return 'fire'
                    elif entity_value in ['earthquake', 'flood', 'fire']:
                        return entity_value

    return None

