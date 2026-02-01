/**
 * Message Constants
 * Configuration values for message display and timing
 */

// Delay between messages when displaying multiple responses (in milliseconds)
export const MESSAGE_DELAY = 800; // 0.8 seconds

// Emergency contact number
export const EMERGENCY_NUMBER = '112';

// Error messages
export const ERROR_MESSAGES = {
  NO_RESPONSE: '⚠️ No response received. Please try again or call **112** if this is an emergency.',
  CONNECTION_ERROR: '⚠️ Unable to connect to the emergency response system. Please call **112** if this is an emergency.',
  GPS_ERROR: 'Unable to get GPS location. Please select a district manually.',
} as const;






