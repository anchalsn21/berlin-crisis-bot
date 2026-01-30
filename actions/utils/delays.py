"""
Delay Utilities
Helper functions for adding natural delays between messages.
"""

import time


def add_message_delay(seconds: float = 0.8) -> None:
    """
    Add a delay between messages for natural conversation flow.
    
    Args:
        seconds: Delay in seconds (default: 0.8)
    """
    time.sleep(seconds)


def add_short_delay(seconds: float = 0.5) -> None:
    """
    Add a short delay for quick responses.
    
    Args:
        seconds: Delay in seconds (default: 0.5)
    """
    time.sleep(seconds)


def add_long_delay(seconds: float = 1.2) -> None:
    """
    Add a longer delay for important messages.
    
    Args:
        seconds: Delay in seconds (default: 1.2)
    """
    time.sleep(seconds)









