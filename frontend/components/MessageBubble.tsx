/**
 * MessageBubble Component
 * Displays individual chat messages (bot or user)
 * 
 * Renders markdown-like formatting for bold text, etc.
 */

'use client';

import React from 'react';
import { isEmergencyMessage, getMessageAriaLabel } from '@/utils';

interface MessageBubbleProps {
  text: string;
  isUser: boolean;
  timestamp?: Date;
  messageId?: string;
}

/**
 * Parse and render text with basic markdown support
 * Handles: **bold**, newlines, lists
 */
function renderFormattedText(text: string): React.ReactNode {
  // Split by lines
  const lines = text.split('\n');
  
  return lines.map((line, lineIndex) => {
    // Handle bold text with **
    const parts = line.split(/(\*\*[^*]+\*\*)/g);
    
    const formattedParts = parts.map((part, partIndex) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        // Bold text
        return (
          <strong key={`${lineIndex}-${partIndex}`}>
            {part.slice(2, -2)}
          </strong>
        );
      }
      return part;
    });

    return (
      <React.Fragment key={lineIndex}>
        {formattedParts}
        {lineIndex < lines.length - 1 && <br />}
      </React.Fragment>
    );
  });
}

export default function MessageBubble({ text, isUser, timestamp, messageId }: MessageBubbleProps) {
  const isEmergency = !isUser && isEmergencyMessage(text);
  const ariaLabel = getMessageAriaLabel(text, isUser);
  const timeString = timestamp?.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <article
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-slide-in`}
      role={isEmergency ? 'alert' : 'article'}
      aria-label={ariaLabel}
      aria-live={isEmergency ? 'assertive' : 'off'}
      aria-atomic="true"
    >
      <div
        className={`max-w-[85%] md:max-w-[70%] px-4 py-3 rounded-2xl ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-sm'
            : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-bl-sm shadow-md border border-gray-100 dark:border-gray-700'
        }`}
        role={isEmergency ? 'alert' : undefined}
      >
        {/* Message Label */}
        {!isUser && (
          <div 
            className="text-xs font-medium text-blue-600 dark:text-blue-400 mb-1"
            aria-hidden="true"
          >
            🤖 Crisis Bot
          </div>
        )}

        {/* Message Content */}
        <div 
          className="message-content text-sm md:text-base leading-relaxed whitespace-pre-wrap"
          id={messageId ? `message-${messageId}` : undefined}
        >
          {renderFormattedText(text)}
        </div>

        {/* Timestamp */}
        {timestamp && (
          <time
            dateTime={timestamp.toISOString()}
            className={`text-xs mt-2 block ${
              isUser ? 'text-blue-200' : 'text-gray-400 dark:text-gray-500'
            }`}
            aria-label={`Sent at ${timeString}`}
          >
            {timeString}
          </time>
        )}
      </div>
    </article>
  );
}

