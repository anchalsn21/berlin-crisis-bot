/**
 * Location Utilities
 * Helper functions for location-related logic
 */

import { Message } from '@/types/chat';

/**
 * Check if the latest bot message is asking for location
 */
export function isLocationNeeded(messages: Message[]): boolean {
  const latestBotMessage = messages
    .slice()
    .reverse()
    .find(m => !m.isUser);

  if (!latestBotMessage) return false;

  const text = latestBotMessage.text?.toLowerCase() || '';
  const hasLocationKeywords = 
    text.includes('which area') || 
    text.includes('location') ||
    text.includes('district');
  
  const hasLocationButtons = latestBotMessage.buttons?.some(
    (b: { title: string; payload: string }) => b.title.includes('📍')
  );

  return hasLocationKeywords || hasLocationButtons || false;
}

/**
 * Get the latest buttons from bot messages
 */
export function getLatestButtons(messages: Message[]) {
  return messages
    .slice()
    .reverse()
    .find(m => !m.isUser && m.buttons && m.buttons.length > 0)?.buttons;
}












