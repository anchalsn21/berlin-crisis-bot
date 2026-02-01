/**
 * MessagesList Component
 * Displays the list of chat messages
 */

'use client';

import React, { useEffect, useRef } from 'react';
import { Message } from '@/types/chat';
import MessageBubble from './MessageBubble';
import LoadingIndicator from './LoadingIndicator';
import { isEmergencyMessage } from '@/utils';

interface MessagesListProps {
  messages: Message[];
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
}

export default function MessagesList({ messages, isLoading, messagesEndRef }: MessagesListProps) {
  const liveRegionRef = useRef<HTMLDivElement>(null);
  const previousMessagesLengthRef = useRef<number>(0);

  // Announce new bot messages to screen readers
  useEffect(() => {
    if (messages.length > previousMessagesLengthRef.current) {
      const newMessages = messages.slice(previousMessagesLengthRef.current);
      const botMessages = newMessages.filter(msg => !msg.isUser);
      
      if (botMessages.length > 0 && liveRegionRef.current) {
        const latestBotMessage = botMessages[botMessages.length - 1];
        const isEmergency = isEmergencyMessage(latestBotMessage.text);
        
        // Update live region with appropriate politeness level
        liveRegionRef.current.setAttribute('aria-live', isEmergency ? 'assertive' : 'polite');
        liveRegionRef.current.textContent = latestBotMessage.text;
        
        // Clear after announcement to allow re-announcement of same content
        setTimeout(() => {
          if (liveRegionRef.current) {
            liveRegionRef.current.textContent = '';
          }
        }, 1000);
      }
      
      previousMessagesLengthRef.current = messages.length;
    }
  }, [messages]);

  return (
    <section 
      className="flex-1 overflow-y-auto p-4 space-y-4"
      aria-label="Chat messages"
      role="log"
      aria-live="polite"
      aria-atomic="false"
    >
      {/* Hidden live region for assertive announcements */}
      <div
        ref={liveRegionRef}
        className="sr-only"
        aria-live="polite"
        aria-atomic="true"
        role="status"
      />

      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          text={message.text}
          isUser={message.isUser}
          timestamp={message.timestamp}
          messageId={message.id}
        />
      ))}

      {isLoading && <LoadingIndicator />}

      {/* Scroll anchor */}
      <div ref={messagesEndRef} aria-hidden="true" />
    </section>
  );
}

