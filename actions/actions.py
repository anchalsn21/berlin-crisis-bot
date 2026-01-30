"""
Berlin Crisis Response Chatbot - Custom Actions
REFACTORED: This file now imports from the modular structure.

All actions are now organized in separate modules for better maintainability.
This file serves as a compatibility layer for Rasa.

The actual implementation is in:
- session/ - Session management
- safety/ - Status assessment & escalation  
- location/ - Location validation & processing
- shelters/ - Shelter finding
- guidance/ - Contextual guidance & instructions
- fallback/ - Default fallback
- templates/ - Reusable buttons & messages
- utils/ - Constants & helpers
"""

# Import all actions from the modular structure
# Only actions actually used in stories.yml and rules.yml are included

from .session.session_start import ActionSessionStart

from .safety.assess_status import ActionAssessStatus
from .safety.escalate_emergency import ActionEscalateEmergency
from .safety.ask_status import ActionAskStatus

from .location.validate_location import ActionValidateLocation

from .shelters.find_nearest_shelters import ActionFindNearestShelters

from .guidance.safety_instructions import (
    ActionProvideSafetyInstructions,
    ActionProvideEarthquakeInstructionsImmediate,
)
from .guidance.handle_greet import ActionHandleGreet

# Export all actions for Rasa
__all__ = [
    'ActionSessionStart',
    'ActionAssessStatus',
    'ActionEscalateEmergency',
    'ActionAskStatus',
    'ActionValidateLocation',
    'ActionFindNearestShelters',
    'ActionProvideSafetyInstructions',
    'ActionProvideEarthquakeInstructionsImmediate',
    'ActionHandleGreet',
]
