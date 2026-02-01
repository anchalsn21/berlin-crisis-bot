/**
 * ChatInput Component
 * Input area with text field and send button
 */

'use client';

import React from 'react';
import { Send, Loader2 } from 'lucide-react';

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
  placeholder?: string;
  inputRef?: React.RefObject<HTMLInputElement | null>;
}

export default function ChatInput({ 
  value, 
  onChange, 
  onSubmit, 
  isLoading,
  placeholder = "Describe your emergency...",
  inputRef,
}: ChatInputProps) {
  const inputId = 'chat-input';
  const sendButtonId = 'chat-send-button';

  return (
    <form 
      onSubmit={onSubmit} 
      className="flex gap-2"
      role="form"
      aria-label="Chat message input form"
    >
      <label htmlFor={inputId} className="sr-only">
        Type your message
      </label>
      <input
        id={inputId}
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={isLoading}
        aria-label="Chat message input"
        aria-describedby={isLoading ? 'input-loading-status' : undefined}
        aria-required="false"
        autoComplete="off"
        className="flex-1 px-4 py-3 bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 transition disabled:opacity-50 disabled:cursor-not-allowed"
      />
      {isLoading && (
        <span id="input-loading-status" className="sr-only" aria-live="polite">
          Bot is processing your message
        </span>
      )}
      <button
        id={sendButtonId}
        type="submit"
        disabled={isLoading || !value.trim()}
        aria-label={isLoading ? 'Sending message' : 'Send message'}
        aria-disabled={isLoading || !value.trim()}
        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-xl transition cursor-pointer disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
      >
        {isLoading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" aria-hidden="true" />
            <span className="sr-only">Sending</span>
          </>
        ) : (
          <>
            <Send className="w-5 h-5" aria-hidden="true" />
            <span className="sr-only">Send</span>
          </>
        )}
      </button>
    </form>
  );
}

















