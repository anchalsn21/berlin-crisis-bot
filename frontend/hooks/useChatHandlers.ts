/**
 * useChatHandlers Hook
 * Handles all chat interaction logic (submit, quick reply, GPS, district)
 */

import { useCallback } from 'react';
import { Message, MessageMetadata } from '@/types/chat';
import { getCurrentPosition } from '@/lib/location';
import { ERROR_MESSAGES } from '@/constants/messages';

interface UseChatHandlersProps {
  sendMessage: (message: string, showInChat?: boolean, metadata?: MessageMetadata) => Promise<Message[]>;
  addUserMessage: (text: string) => void;
  enqueueMessages: (messages: Message[]) => void;
  processQueue: (onMessage: (message: Message) => void) => Promise<void>;
  addBotMessage: (message: Message) => void;
}

interface UseChatHandlersReturn {
  handleSubmit: (userInput: string) => Promise<void>;
  handleQuickReply: (title: string, payload: string) => Promise<void>;
  handleDistrictSelect: (district: string) => Promise<void>;
  handleGPSSelect: () => Promise<void>;
}

export function useChatHandlers({
  sendMessage,
  addUserMessage,
  enqueueMessages,
  processQueue,
  addBotMessage,
}: UseChatHandlersProps): UseChatHandlersReturn {
  /**
   * Display bot messages with delay
   */
  const displayBotMessages = useCallback(async (messages: Message[]) => {
    if (messages.length > 0) {
      enqueueMessages(messages);
      await processQueue(addBotMessage);
    }
  }, [enqueueMessages, processQueue, addBotMessage]);

  /**
   * Handle form submission
   */
  const handleSubmit = useCallback(async (userInput: string) => {
    const botMessages = await sendMessage(userInput, true);
    await displayBotMessages(botMessages);
  }, [sendMessage, displayBotMessages]);

  /**
   * Handle quick reply button click
   */
  const handleQuickReply = useCallback(async (title: string, payload: string) => {
    // Add user's selection to chat (remove emoji prefix if present)
    const displayText = title.replace(/^[^\s]+\s/, '');
    addUserMessage(displayText);

    const botMessages = await sendMessage(payload);
    await displayBotMessages(botMessages);
  }, [sendMessage, addUserMessage, displayBotMessages]);

  /**
   * Handle district selection
   */
  const handleDistrictSelect = useCallback(async (district: string) => {
    addUserMessage(`📍 ${district}`);
    const botMessages = await sendMessage(district);
    await displayBotMessages(botMessages);
  }, [sendMessage, addUserMessage, displayBotMessages]);

  /**
   * Handle GPS location sharing
   */
  const handleGPSSelect = useCallback(async () => {
    try {
      addUserMessage('📍 Sharing GPS location...');
      
      const position = await getCurrentPosition();
      const { latitude, longitude } = position.coords;
      
      const botMessages = await sendMessage(
        'sharing my gps location',
        true,
        {
          location_coords: {
            lat: latitude,
            lng: longitude,
          },
        }
      );
      
      await displayBotMessages(botMessages);
    } catch (error: any) {
      const errorText = error.message || ERROR_MESSAGES.GPS_ERROR;
      const botMessages = await sendMessage(`⚠️ ${errorText}`, true);
      await displayBotMessages(botMessages);
    }
  }, [sendMessage, addUserMessage, displayBotMessages]);

  return {
    handleSubmit,
    handleQuickReply,
    handleDistrictSelect,
    handleGPSSelect,
  };
}

