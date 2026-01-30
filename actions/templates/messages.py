"""
Reusable message templates for Berlin Crisis Response Chatbot.
Centralizes message formatting to reduce duplication.
"""

from typing import Dict, List, Optional

from ..utils.constants import EMERGENCY_DATA


def get_emergency_emoji(emergency_type: Optional[str]) -> str:
    """
    Get emoji for emergency type.
    
    Args:
        emergency_type: Emergency type string
    
    Returns:
        Emoji string for the emergency type
    """
    emoji_map = {
        'earthquake': '🏗️',
        'flood': '🌊',
        'fire': '🔥'
    }
    return emoji_map.get(emergency_type, '⚠️')


def format_emergency_contacts() -> str:
    """
    Format emergency contact information message.
    
    Returns:
        Formatted string with emergency contacts
    """
    contacts = EMERGENCY_DATA.get('emergency_contacts', {})
    message = "**📞 EMERGENCY CONTACTS:**\n"
    message += f"🚨 Emergency Services: **{contacts.get('emergency', '112')}**\n"
    message += f"🚓 Police: **{contacts.get('police', '110')}**\n"
    message += f"❤️ Red Cross Berlin: **{contacts.get('red_cross_berlin', '+49 30 600 300')}**\n"
    return message


def format_shelter_info(district: str, shelters: List[Dict]) -> str:
    """
    Format shelter information message for a district.
    
    Args:
        district: District name
        shelters: List of shelter dictionaries
    
    Returns:
        Formatted string with shelter information
    """
    message = f"🏥 **EMERGENCY SHELTERS IN {district.upper()}:**\n\n"
    
    for i, shelter in enumerate(shelters, 1):
        message += f"**{i}. {shelter.get('name', 'Shelter')}**\n"
        message += f"📍 {shelter.get('address', 'Address not available')}\n"
        message += f"📞 {shelter.get('phone', 'N/A')}\n"
        if shelter.get('capacity'):
            message += f"👥 Capacity: {shelter['capacity']} people\n"
        if shelter.get('facilities'):
            message += f"🔧 Facilities: {', '.join(shelter['facilities'])}\n"
        message += "\n"
    
    # Add emergency contacts
    message += format_emergency_contacts()
    message += "\n**Please head to the nearest shelter if it's safe to travel.**"
    
    return message


def format_safety_instructions(emergency_type: str, district: str = "your area") -> str:
    """
    Format safety instructions message for an emergency type.
    
    Args:
        emergency_type: Type of emergency
        district: District name (default: "your area")
    
    Returns:
        Formatted string with safety instructions
    """
    instructions = EMERGENCY_DATA.get('safety_instructions', {}).get(emergency_type, {})
    during = instructions.get('during', [])
    after = instructions.get('after', [])
    
    emoji = get_emergency_emoji(emergency_type)
    message = f"{emoji} **{emergency_type.upper()} SAFETY INSTRUCTIONS for {district}**\n\n"
    
    if during:
        message += "**🚨 IMMEDIATE ACTIONS:**\n"
        for i, step in enumerate(during, 1):
            message += f"{i}. {step}\n"
        message += "\n"
    
    if after:
        message += "**📋 AFTER THE EMERGENCY:**\n"
        for i, step in enumerate(after, 1):
            message += f"{i}. {step}\n"
    
    return message


def format_earthquake_instructions_immediate() -> str:
    """
    Format immediate earthquake safety instructions (without location).
    
    Returns:
        Formatted string with immediate earthquake instructions
    """
    instructions = EMERGENCY_DATA.get('safety_instructions', {}).get('earthquake', {})
    during = instructions.get('during', [])
    after = instructions.get('after', [])
    
    message = "🏗️ **EARTHQUAKE EMERGENCY - IMMEDIATE SAFETY INSTRUCTIONS**\n\n"
    message += "🚨 **Stay calm and follow these steps immediately:**\n\n"
    
    if during:
        message += "**🚨 IMMEDIATE ACTIONS:**\n"
        for i, step in enumerate(during, 1):
            message += f"{i}. {step}\n"
        message += "\n"
    else:
        message += "**🚨 IMMEDIATE ACTIONS:**\n"
        message += "1. Drop, Cover, and Hold On - Get under a sturdy table or desk\n"
        message += "2. Stay away from windows, glass, and heavy objects\n"
        message += "3. If outdoors, move to an open area away from buildings\n"
        message += "4. If in a vehicle, pull over and stay inside\n\n"
    
    if after:
        message += "**📋 AFTER THE EMERGENCY:**\n"
        for i, step in enumerate(after, 1):
            message += f"{i}. {step}\n"
    else:
        message += "**📋 AFTER THE EMERGENCY:**\n"
        message += "1. Check yourself and others for injuries\n"
        message += "2. Be prepared for aftershocks\n"
        message += "3. Listen to emergency broadcasts\n"
        message += "4. Evacuate if your building is damaged\n"
    
    return message

