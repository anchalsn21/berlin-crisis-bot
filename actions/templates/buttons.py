"""
Reusable button templates for Berlin Crisis Response Chatbot.
Centralizes button definitions to reduce duplication.
"""

from typing import List, Dict


def get_status_buttons() -> List[Dict[str, str]]:
    """
    Get standard status assessment buttons.
    
    Returns:
        List of button dictionaries for safe/injured/trapped status
    """
    return [
        {"title": "✅ I'm safe", "payload": "i'm safe"},
        {"title": "🤕 I'm injured", "payload": "i'm injured"},
        {"title": "🆘 I'm trapped", "payload": "i'm trapped"}
    ]


def get_emergency_type_buttons() -> List[Dict[str, str]]:
    """
    Get emergency type selection buttons.
    
    Returns:
        List of button dictionaries for earthquake/flood/fire
    """
    return [
        {"title": "🏗️ Earthquake", "payload": "/report_earthquake"},
        {"title": "🌊 Flood", "payload": "/report_flood"},
        {"title": "🔥 Fire", "payload": "/report_fire"}
    ]


def get_main_menu_buttons() -> List[Dict[str, str]]:
    """
    Get main menu buttons for general actions.
    
    Returns:
        List of button dictionaries for main menu options
    """
    return [
        {"title": "🏥 Show Shelters", "payload": "/request_shelter_info"},
        {"title": "📞 Emergency Contacts", "payload": "/request_emergency_contacts"},
        {"title": "✅ I'm all set", "payload": "/goodbye"}
    ]


def get_shelter_menu_buttons() -> List[Dict[str, str]]:
    """
    Get extended menu buttons including safety instructions.
    
    Returns:
        List of button dictionaries with shelter, contacts, and safety options
    """
    return [
        {"title": "🏥 Show Shelters", "payload": "/request_shelter_info"},
        {"title": "📞 Emergency Contacts", "payload": "/request_emergency_contacts"},
        {"title": "📋 Safety Instructions", "payload": "/request_safety_instructions"},
        {"title": "✅ I'm all set", "payload": "/goodbye"}
    ]


def get_location_help_button() -> List[Dict[str, str]]:
    """
    Get button for location help request.
    
    Returns:
        List with single location help button
    """
    return [
        {"title": "📍 Provide Location", "payload": "/request_location_help"}
    ]


def get_safe_user_buttons() -> List[Dict[str, str]]:
    """
    Get buttons for safe users to continue the conversation.
    Includes options to report emergency, show shelters, contacts, etc.
    
    Returns:
        List of button dictionaries for safe users to continue interaction
    """
    return [
        {"title": "🚨 Report Emergency", "payload": "/request_emergency_type"},
        {"title": "🏥 Show Shelters", "payload": "/request_shelter_info"},
        {"title": "📞 Emergency Contacts", "payload": "/request_emergency_contacts"},
        {"title": "📋 Safety Instructions", "payload": "/request_safety_instructions"},
        {"title": "✅ I'm all set", "payload": "/goodbye"}
    ]

