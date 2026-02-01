/**
 * ChatWindow Component
 * Main chat interface that communicates with Rasa backend
 * 
 * All decision-making is done by Rasa - this is just a "dumb" UI that:
 * 1. Sends user messages to Rasa
 * 2. Displays Rasa responses
 * 3. Renders quick reply buttons from Rasa
 * 4. Displays district selection buttons when location is needed
 */

'use client';

import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { useChatMessages, useDarkMode, useMessageQueue, useChatHandlers } from '@/hooks';
import ChatHeader from './ChatHeader';
import EmergencyBanner from './EmergencyBanner';
import MessagesList from './MessagesList';
import ChatFooter from './ChatFooter';

export default function ChatWindow() {
  const [inputValue, setInputValue] = useState('');
  const [sessionId] = useState(() => uuidv4());
  const inputRef = useRef<HTMLInputElement>(null);
  
  const { darkMode, toggleDarkMode } = useDarkMode();
  const { messages, isLoading, messagesEndRef, sendMessage, addUserMessage, addBotMessages } = useChatMessages(sessionId);
  const { isProcessing: isProcessingQueue, enqueueMessages, processQueue } = useMessageQueue();
  
  const { handleSubmit: handleSubmitMessage, handleQuickReply } = useChatHandlers({
    sendMessage,
    addUserMessage,
    enqueueMessages,
    processQueue,
    addBotMessage: (message) => addBotMessages([message]),
  });

  // Initialize: send greeting on mount
  useEffect(() => {
    const initializeGreeting = async () => {
      const botMessages = await sendMessage('hello', false);
      if (botMessages.length > 0) {
        enqueueMessages(botMessages);
        await processQueue((message) => {
          addBotMessages([message]);
        });
      }
    };
    initializeGreeting();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Only run once on mount

  // Focus input after loading
  useEffect(() => {
    if (!isLoading && !isProcessingQueue) {
      inputRef.current?.focus();
    }
  }, [isLoading, isProcessingQueue]);

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading && !isProcessingQueue) {
      const userInput = inputValue.trim();
      setInputValue('');
      await handleSubmitMessage(userInput);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900 transition-colors" role="application" aria-label="Berlin Emergency Crisis Response Chatbot">
      <ChatHeader darkMode={darkMode} onToggleDarkMode={toggleDarkMode} messages={messages} />
      <EmergencyBanner />
      
      <main className="flex-1 flex flex-col overflow-hidden" role="main" aria-label="Chat conversation">
        <MessagesList 
          messages={messages}
          isLoading={isLoading || isProcessingQueue}
          messagesEndRef={messagesEndRef}
        />

        <ChatFooter
          inputValue={inputValue}
          onInputChange={setInputValue}
          onSubmit={handleSubmit}
          onQuickReply={handleQuickReply}
          messages={messages}
          isLoading={isLoading}
          isProcessingQueue={isProcessingQueue}
          inputRef={inputRef}
        />
      </main>
    </div>
  );
}

