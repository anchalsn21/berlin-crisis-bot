/**
 * useChatMessages Hook
 * Manages chat messages and Rasa communication
 */

import { useState, useRef, useEffect, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { sendToRasa, RasaMessage } from '@/lib/rasa';
import { Message, MessageMetadata } from '@/types/chat';
import { ERROR_MESSAGES } from '@/constants/messages';

export function useChatMessages(sessionId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  /**
   * Create a message object
   */
  const createMessage = useCallback((
    text: string,
    isUser: boolean,
    buttons?: Array<{ title: string; payload: string }>
  ): Message => ({
    id: uuidv4(),
    text,
    isUser,
    timestamp: new Date(),
    buttons,
  }), []);

  /**
   * Convert Rasa response to Message format
   */
  const rasaToMessage = useCallback((response: RasaMessage): Message | null => {
    const hasText = response.text && response.text.trim();
    const hasButtons = response.buttons && response.buttons.length > 0;
    
    if (!hasText && !hasButtons) return null;
    
    return createMessage(response.text || '', false, response.buttons);
  }, [createMessage]);

  /**
   * Send message to Rasa and return responses (without adding to chat)
   * The caller handles displaying messages with delays
   */
  const sendMessage = useCallback(async (
    message: string,
    showInChat: boolean = false,
    metadata?: MessageMetadata
  ): Promise<Message[]> => {
    if (!message.trim() && !metadata) return [];

    // Add user message to chat if needed
    if (showInChat && !message.startsWith('/')) {
      setMessages(prev => [...prev, createMessage(message, true)]);
    }

    setIsLoading(true);

    try {
      const responses = await sendToRasa(sessionId, message, metadata);
      
      if (!responses || responses.length === 0) {
        return [createMessage(ERROR_MESSAGES.NO_RESPONSE, false)];
      }

      // Convert Rasa responses to Messages
      const botMessages = responses
        .map(rasaToMessage)
        .filter((msg): msg is Message => msg !== null);

      return botMessages.length > 0 
        ? botMessages 
        : [createMessage(ERROR_MESSAGES.NO_RESPONSE, false)];
    } catch (error) {
      console.error('Error communicating with Rasa:', error);
      return [createMessage(ERROR_MESSAGES.CONNECTION_ERROR, false)];
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, createMessage, rasaToMessage]);

  /**
   * Add a user message to chat
   */
  const addUserMessage = useCallback((text: string) => {
    setMessages(prev => [...prev, createMessage(text, true)]);
  }, [createMessage]);

  /**
   * Add bot messages to chat (used for delayed display)
   */
  const addBotMessages = useCallback((newMessages: Message[]) => {
    setMessages(prev => [...prev, ...newMessages]);
  }, []);

  return {
    messages,
    isLoading,
    messagesEndRef,
    sendMessage,
    addUserMessage,
    addBotMessages,
  };
}

