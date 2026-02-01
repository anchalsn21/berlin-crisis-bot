/**
 * QuickReplyButtons Component
 * Displays quick reply buttons from Rasa responses
 */

'use client';

import React from 'react';
import { Button } from '@/types/chat';
import ButtonComponent from './ui/Button';

interface QuickReplyButtonsProps {
  buttons: Button[];
  onButtonClick: (title: string, payload: string) => void;
  disabled?: boolean;
}

export default function QuickReplyButtons({ buttons, onButtonClick, disabled = false }: QuickReplyButtonsProps) {
  if (!buttons || buttons.length === 0) {
    return null;
  }

  return (
    <div 
      className="flex-shrink-0 px-4 pb-2"
      role="group"
      aria-label="Quick reply options"
    >
      <div className="flex flex-wrap gap-2 justify-center">
        {buttons.map((button, index) => (
          <ButtonComponent
            key={index}
            variant="outline"
            size="md"
            onClick={() => onButtonClick(button.title, button.payload)}
            className="rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            disabled={disabled}
            aria-label={`Quick reply: ${button.title}`}
          >
            {button.title}
          </ButtonComponent>
        ))}
      </div>
    </div>
  );
}












