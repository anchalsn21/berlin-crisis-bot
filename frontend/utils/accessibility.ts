/**
 * Accessibility Utilities
 * Helper functions for accessibility features
 */

/**
 * Detects if a message is an emergency/critical message that requires assertive announcement
 * Emergency messages typically contain keywords indicating immediate action or critical situations
 */
export function isEmergencyMessage(text: string): boolean {
  const emergencyKeywords = [
    'critical',
    'immediate action',
    'immediate assistance',
    'trapped',
    'injured',
    'evacuate',
    'evacuation',
    'life-threatening',
    'call 112',
    'emergency services',
    'help is on the way',
    'requires rescue',
    '🚨', // Critical alert emoji
    '🆘', // Emergency emoji
  ];

  const lowerText = text.toLowerCase();
  return emergencyKeywords.some(keyword => lowerText.includes(keyword.toLowerCase()));
}

/**
 * Generates an accessible label for a message based on sender and content
 */
export function getMessageAriaLabel(text: string, isUser: boolean): string {
  const sender = isUser ? 'You' : 'Crisis Bot';
  const preview = text.length > 50 ? `${text.substring(0, 50)}...` : text;
  return `${sender}: ${preview}`;
}

/**
 * Generates a unique ID for ARIA live regions
 */
export function getLiveRegionId(messageId: string): string {
  return `live-region-${messageId}`;
}
