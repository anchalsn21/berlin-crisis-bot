/**
 * useDarkMode Hook
 * Manages dark mode state and persistence
 * Compatible with Next.js 15 SSR
 */

import { useState, useEffect } from 'react';

export function useDarkMode() {
  const [darkMode, setDarkMode] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Mark as mounted (client-side only)
    setMounted(true);
    
    // Load dark mode preference from localStorage
    if (typeof window !== 'undefined') {
      const savedMode = localStorage.getItem('darkMode');
      if (savedMode === 'true') {
        setDarkMode(true);
        document.documentElement.classList.add('dark');
      }
    }
  }, []);

  const toggleDarkMode = () => {
    if (typeof window === 'undefined') return;
    
    const newMode = !darkMode;
    setDarkMode(newMode);
    localStorage.setItem('darkMode', String(newMode));
    
    if (newMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  // Return mounted state to prevent hydration mismatch
  return { darkMode, toggleDarkMode, mounted };
}

