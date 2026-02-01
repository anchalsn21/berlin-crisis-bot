/**
 * LoadingIndicator Component
 * Shows loading state while waiting for bot response
 */

'use client';

import React from 'react';
import { Loader2 } from 'lucide-react';

export default function LoadingIndicator() {
  return (
    <div className="flex justify-start" role="status" aria-live="polite" aria-label="Bot is thinking">
      <div className="bg-white dark:bg-gray-800 rounded-2xl rounded-bl-sm px-4 py-3 shadow-md border border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
          <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
          <span className="text-sm">Thinking...</span>
        </div>
      </div>
    </div>
  );
}

















