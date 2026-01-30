"""
Constants for Berlin Crisis Response Chatbot.
Contains district mappings, postcodes, and emergency data.
"""

import json
import os

# ============================================================================
# DATA LOADING
# ============================================================================

# Load shelter and emergency data
# Path: actions/utils/constants.py -> .. (to actions/) -> .. (to rasa-backend/) -> data/
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'berlin_shelters.json')

def load_emergency_data() -> dict:
    """Load emergency data from JSON file."""
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"shelters": {}, "emergency_contacts": {}, "safety_instructions": {}}

EMERGENCY_DATA = load_emergency_data()

# ============================================================================
# BERLIN DISTRICT MAPPING
# ============================================================================

# Complete Berlin district list with variations
BERLIN_DISTRICTS = {
    # Mitte variations
    'mitte': 'Mitte',
    'mitt': 'Mitte',
    'center': 'Mitte',
    'zentrum': 'Mitte',
    'central': 'Mitte',
    'city centre': 'Mitte',
    'stadtmitte': 'Mitte',
    'downtown': 'Mitte',

    # Kreuzberg variations
    'kreuzberg': 'Kreuzberg',
    'kreuz': 'Kreuzberg',
    'xberg': 'Kreuzberg',
    'x-berg': 'Kreuzberg',
    'crossberg': 'Kreuzberg',
    'berg kreuz': 'Kreuzberg',

    # Prenzlauer Berg variations
    'prenzlauer berg': 'Prenzlauer Berg',
    'prenzlauer': 'Prenzlauer Berg',
    'prenzlauerberg': 'Prenzlauer Berg',
    'prenzl': 'Prenzlauer Berg',
    'prenz': 'Prenzlauer Berg',
    'prenzlauer berge': 'Prenzlauer Berg',

    # Charlottenburg variations
    'charlottenburg': 'Charlottenburg',
    'charlotten': 'Charlottenburg',
    'charlottenberg': 'Charlottenburg',
    'charlot': 'Charlottenburg',
    'charlott': 'Charlottenburg',
    'charlotten burg': 'Charlottenburg',
    'charlotten-burg': 'Charlottenburg',

    # Schöneberg variations
    'schöneberg': 'Schöneberg',
    'schoneberg': 'Schöneberg',
    'schoeneberg': 'Schöneberg',
    'schönberg': 'Schöneberg',
    'schonberg': 'Schöneberg',
    'schoen berg': 'Schöneberg',

    # Friedrichshain variations
    'friedrichshain': 'Friedrichshain',
    'friedrichs hain': 'Friedrichshain',
    'f-hain': 'Friedrichshain',
    'hain': 'Friedrichshain',
    'fhain': 'Friedrichshain',
    'friedrich': 'Friedrichshain',
    'f-shain': 'Friedrichshain',

    # Wedding variations
    'wedding': 'Wedding',
    'nordbahn': 'Wedding',
    'wed': 'Wedding',

    # Pankow variations
    'pankow': 'Pankow',
    'pankov': 'Pankow',

    # Lichtenberg variations
    'lichtenberg': 'Lichtenberg',
    'lichten berg': 'Lichtenberg',
    'lichten': 'Lichtenberg',

    # Neukölln variations
    'neukölln': 'Neukölln',
    'neukoelln': 'Neukölln',
    'neukoln': 'Neukölln',
    'neu kölln': 'Neukölln',
    'neu-koelln': 'Neukölln',
    'neukolln': 'Neukölln',
    'neuköll': 'Neukölln',

    # Steglitz variations
    'steglitz': 'Steglitz',
    'stegliz': 'Steglitz',
    'stegl': 'Steglitz',

    # Tempelhof variations
    'tempelhof': 'Tempelhof',
    'tempel hof': 'Tempelhof',
    'tempel': 'Tempelhof',

    # Spandau variations
    'spandau': 'Spandau',
    'spandow': 'Spandau',
    'spand': 'Spandau',

    # Marzahn variations
    'marzahn': 'Marzahn',
    'marzahner': 'Marzahn',
    'marz': 'Marzahn',

    # Treptow variations
    'treptow': 'Treptow',
    'treptow-koepenick': 'Treptow',
    'trept': 'Treptow',

    # Reinickendorf variations
    'reinickendorf': 'Reinickendorf',
    'reinicken dorf': 'Reinickendorf',
    'reinicken': 'Reinickendorf',

    # Hellersdorf variations
    'hellersdorf': 'Hellersdorf',
    'hellers dorf': 'Hellersdorf',
    'hellers': 'Hellersdorf',

    # Wilmersdorf variations
    'wilmersdorf': 'Wilmersdorf',
    'wilmers dorf': 'Wilmersdorf',
    'wilmers': 'Wilmersdorf',

    # Zehlendorf variations
    'zehlendorf': 'Zehlendorf',
    'zehlen dorf': 'Zehlendorf',
    'zehlen': 'Zehlendorf',

    # Köpenick variations
    'köpenick': 'Köpenick',
    'kopenick': 'Köpenick',
}

# Berlin postcode to district mapping
BERLIN_POSTCODES = {
    '10115': 'Mitte', '10117': 'Mitte', '10119': 'Mitte', '10178': 'Mitte', '10179': 'Mitte',
    '10405': 'Prenzlauer Berg', '10435': 'Prenzlauer Berg', '10437': 'Prenzlauer Berg',
    '10243': 'Friedrichshain', '10245': 'Friedrichshain', '10247': 'Friedrichshain',
    '10961': 'Kreuzberg', '10963': 'Kreuzberg', '10965': 'Kreuzberg', '10967': 'Kreuzberg', '10969': 'Kreuzberg',
    '10551': 'Charlottenburg', '10553': 'Charlottenburg', '10555': 'Charlottenburg', '10585': 'Charlottenburg',
    '10623': 'Charlottenburg', '10625': 'Charlottenburg', '10627': 'Charlottenburg',
    '10777': 'Schöneberg', '10779': 'Schöneberg', '10781': 'Schöneberg', '10783': 'Schöneberg',
    '13347': 'Wedding', '13349': 'Wedding', '13351': 'Wedding', '13353': 'Wedding',
    '13125': 'Pankow', '13127': 'Pankow', '13129': 'Pankow', '13156': 'Pankow',
    '10315': 'Lichtenberg', '10317': 'Lichtenberg', '10318': 'Lichtenberg',
    '12043': 'Neukölln', '12045': 'Neukölln', '12047': 'Neukölln', '12049': 'Neukölln',
    '12157': 'Steglitz', '12159': 'Steglitz', '12161': 'Steglitz',
    '12099': 'Tempelhof', '12101': 'Tempelhof', '12103': 'Tempelhof',
    '13581': 'Spandau', '13583': 'Spandau', '13585': 'Spandau',
    '12679': 'Marzahn', '12681': 'Marzahn', '12683': 'Marzahn',
    '12435': 'Treptow', '12437': 'Treptow', '12439': 'Treptow',
    '13403': 'Reinickendorf', '13405': 'Reinickendorf', '13407': 'Reinickendorf',
    '12619': 'Hellersdorf', '12621': 'Hellersdorf', '12623': 'Hellersdorf',
    '10707': 'Wilmersdorf', '10709': 'Wilmersdorf', '10711': 'Wilmersdorf',
    '14163': 'Zehlendorf', '14165': 'Zehlendorf', '14167': 'Zehlendorf',
    '12555': 'Köpenick', '12557': 'Köpenick', '12559': 'Köpenick',
}

# Standard district names for validation
STANDARD_DISTRICTS = [
    'Mitte', 'Kreuzberg', 'Prenzlauer Berg', 'Charlottenburg',
    'Friedrichshain', 'Schöneberg', 'Neukölln', 'Wedding',
    'Pankow', 'Lichtenberg', 'Steglitz', 'Tempelhof', 'Spandau',
    'Marzahn', 'Treptow', 'Reinickendorf', 'Hellersdorf',
    'Wilmersdorf', 'Zehlendorf', 'Köpenick'
]

