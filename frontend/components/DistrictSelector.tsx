/**
 * DistrictSelector Component
 * Shows all Berlin districts when location is needed
 * Includes GPS location button
 */

'use client';

import React, { useState } from 'react';
import { BERLIN_DISTRICTS } from '@/lib/location';
import { MapPin, Loader2 } from 'lucide-react';

interface DistrictSelectorProps {
  onDistrictSelect: (district: string) => void;
  onGPSSelect?: () => void;
  disabled?: boolean;
}

export default function DistrictSelector({ onDistrictSelect, onGPSSelect, disabled = false }: DistrictSelectorProps) {
  const [isGettingGPS, setIsGettingGPS] = useState(false);

  const handleGPSClick = async () => {
    if (disabled || isGettingGPS) return;
    
    setIsGettingGPS(true);
    try {
      if (onGPSSelect) {
        await onGPSSelect();
      }
    } catch (error) {
      console.error('GPS error:', error);
    } finally {
      setIsGettingGPS(false);
    }
  };

  return (
    <div className="mt-3 space-y-2">
      {/* GPS Button */}
      {onGPSSelect && (
        <button
          onClick={handleGPSClick}
          disabled={disabled || isGettingGPS}
          className="w-full px-4 py-2 text-sm bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-700 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/50 transition cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isGettingGPS ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Getting location...</span>
            </>
          ) : (
            <>
              <MapPin className="w-4 h-4" />
              <span>📍 Use my GPS location</span>
            </>
          )}
        </button>
      )}
      
      {/* District Buttons */}
      <div className="flex flex-wrap gap-2 justify-center max-h-32 overflow-y-auto">
        {BERLIN_DISTRICTS.map((district) => (
          <button
            key={district}
            onClick={() => onDistrictSelect(district)}
            disabled={disabled}
            className="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            📍 {district}
          </button>
        ))}
      </div>
    </div>
  );
}






