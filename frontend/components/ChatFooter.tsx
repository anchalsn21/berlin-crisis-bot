/**
 * ChatFooter Component
 * Input area with chat input and district selector
 */

'use client';

import React from 'react';
import { Message } from '@/types/chat';
import ChatInput from './ChatInput';
import QuickReplyButtons from './QuickReplyButtons';
import { getLatestButtons } from '@/utils';

interface ChatFooterProps {
  inputValue: string;
  onInputChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  onQuickReply: (title: string, payload: string) => void;
  messages: Message[];
  isLoading: boolean;
  isProcessingQueue: boolean;
  inputRef?: React.RefObject<HTMLInputElement | null>;
}

export default function ChatFooter({
  inputValue,
  onInputChange,
  onSubmit,
  onQuickReply,
  messages,
  isLoading,
  isProcessingQueue,
  inputRef,
}: ChatFooterProps) {
  const latestButtons = getLatestButtons(messages);
  const isDisabled = isLoading || isProcessingQueue;

  return (
    <section aria-label="Chat input and quick actions">
      {/* Quick Reply Buttons */}
      {latestButtons && (
        <QuickReplyButtons 
          buttons={latestButtons} 
          onButtonClick={onQuickReply}
          disabled={isDisabled}
        />
      )}

      {/* Input Area */}
      <div className="flex-shrink-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 p-4">
        <ChatInput
          value={inputValue}
          onChange={onInputChange}
          onSubmit={onSubmit}
          isLoading={isDisabled}
          inputRef={inputRef}
        />

        {/* District Selector removed - districts now come from Rasa backend buttons */}
      </div>
    </section>
  );
}

