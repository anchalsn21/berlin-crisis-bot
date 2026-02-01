/**
 * EmergencyBanner Component
 * Displays emergency contact information
 */

'use client';

import React from 'react';
import { EMERGENCY_NUMBER } from '@/constants/messages';

export default function EmergencyBanner() {
  return (
    <div 
      className="flex-shrink-0 bg-red-50 dark:bg-red-900/30 border-b border-red-200 dark:border-red-800 px-4 py-2"
      role="alert"
      aria-live="assertive"
      aria-label="Emergency contact information"
    >
      <p className="text-center text-sm text-red-700 dark:text-red-300">
        <span aria-hidden="true">⚠️</span>{' '}
        <strong>Life-threatening?</strong> Call <strong>{EMERGENCY_NUMBER}</strong> immediately!
      </p>
    </div>
  );
}






