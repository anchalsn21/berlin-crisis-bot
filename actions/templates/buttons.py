from typing import List, Dict


def get_status_buttons() -> List[Dict[str, str]]:
    return [
        {"title": "✅ I'm safe", "payload": "i'm safe"},
        {"title": "🤕 I'm injured", "payload": "i'm injured"},
        {"title": "🆘 I'm trapped", "payload": "i'm trapped"}
    ]


def get_emergency_type_buttons() -> List[Dict[str, str]]:
    return [
        {"title": "🏗️ Earthquake", "payload": "/report_earthquake"},
        {"title": "🌊 Flood", "payload": "/report_flood"},
        {"title": "🔥 Fire", "payload": "/report_fire"}
    ]


def get_main_menu_buttons() -> List[Dict[str, str]]:
    return [
        {"title": "🏥 Show Shelters", "payload": "/request_shelter_info"},
        {"title": "📞 Emergency Contacts", "payload": "/request_emergency_contacts"},
        {"title": "✅ I'm all set", "payload": "/goodbye"}
    ]


def get_shelter_menu_buttons() -> List[Dict[str, str]]:
    return [
        {"title": "🏥 Show Shelters", "payload": "/request_shelter_info"},
        {"title": "📞 Emergency Contacts", "payload": "/request_emergency_contacts"},
        {"title": "📋 Safety Instructions", "payload": "/request_safety_instructions"},
        {"title": "✅ I'm all set", "payload": "/goodbye"}
    ]


def get_location_help_button() -> List[Dict[str, str]]:
    return [
        {"title": "📍 Provide Location", "payload": "/request_location_help"}
    ]


def get_safe_user_buttons() -> List[Dict[str, str]]:
    return [
        {"title": "🚨 Report Emergency", "payload": "/request_emergency_type"},
        {"title": "🏥 Show Shelters", "payload": "/request_shelter_info"},
        {"title": "📞 Emergency Contacts", "payload": "/request_emergency_contacts"},
        {"title": "📋 Safety Instructions", "payload": "/request_safety_instructions"},
        {"title": "✅ I'm all set", "payload": "/goodbye"}
    ]

