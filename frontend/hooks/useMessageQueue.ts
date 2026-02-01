/**
 * useMessageQueue Hook
 * Manages message queue for delayed display of multiple messages
 */

import { useState, useRef, useCallback } from 'react';
import { Message } from '@/types/chat';
import { MESSAGE_DELAY } from '@/constants/messages';

interface UseMessageQueueReturn {
  isProcessing: boolean;
  enqueueMessages: (messages: Message[]) => void;
  processQueue: (onMessage: (message: Message) => void) => Promise<void>;
}

export function useMessageQueue(): UseMessageQueueReturn {
  const [isProcessing, setIsProcessing] = useState(false);
  const messageQueueRef = useRef<Message[]>([]);
  const isProcessingRef = useRef(false);

  /**
   * Add messages to the queue
   */
  const enqueueMessages = useCallback((messages: Message[]) => {
    messageQueueRef.current.push(...messages);
  }, []);

  /**
   * Process the message queue, calling onMessage for each message with delay
   * Continues processing even if new messages are added while processing
   */
  const processQueue = useCallback(async (onMessage: (message: Message) => void) => {
    // Use ref to check processing state to avoid stale closure issues
    if (isProcessingRef.current) {
      // If already processing, messages are already in queue and will be processed
      // by the current running process (the while loop checks queue length)
      return;
    }

    // If queue is empty, nothing to process
    if (messageQueueRef.current.length === 0) {
      return;
    }

    isProcessingRef.current = true;
    setIsProcessing(true);

    try {
      // Process all messages in queue (including any added during processing)
      // The while loop will continue as long as there are messages, even if
      // new ones are added while processing
      while (messageQueueRef.current.length > 0) {
        const message = messageQueueRef.current.shift();
        if (message) {
          onMessage(message);
          // Wait before showing next message (except for the last one)
          if (messageQueueRef.current.length > 0) {
            await new Promise(resolve => setTimeout(resolve, MESSAGE_DELAY));
          }
        }
      }
    } finally {
      isProcessingRef.current = false;
      setIsProcessing(false);
      
      // After processing completes, check if new messages were added
      // This handles the race condition where messages are enqueued while processing
      if (messageQueueRef.current.length > 0) {
        // Process remaining messages after a brief delay to allow state to settle
        await new Promise(resolve => setTimeout(resolve, 50));
        // Recursively process remaining messages (only if not already processing)
        if (!isProcessingRef.current) {
          await processQueue(onMessage);
        }
      }
    }
  }, []);

  return {
    isProcessing,
    enqueueMessages,
    processQueue,
  };
}

