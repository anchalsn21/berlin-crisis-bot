"""
Templates for reusable messages, buttons, and formatting.
Centralizes repeated UI elements to reduce duplication.
"""

from .buttons import (
    get_status_buttons,
    get_emergency_type_buttons,
    get_main_menu_buttons,
    get_shelter_menu_buttons,
)
from .messages import (
    format_emergency_contacts,
    format_shelter_info,
    get_emergency_emoji,
)

__all__ = [
    'get_status_buttons',
    'get_emergency_type_buttons',
    'get_main_menu_buttons',
    'get_shelter_menu_buttons',
    'format_emergency_contacts',
    'format_shelter_info',
    'get_emergency_emoji',
]












