/**
 * Berlin Crisis Response Chatbot - Landing Page
 * Entry point with theme toggle and start chat button
 */

'use client';

import {useState, useEffect} from 'react';
import {Moon, Sun, AlertTriangle, Shield} from 'lucide-react';
import Link from 'next/link';

export default function LandingPage() {
    const [darkMode, setDarkMode] = useState(false);

    // Initialize dark mode from localStorage
    useEffect(() => {
        // Check if we're in browser environment
        if (typeof window !== 'undefined') {
            const savedMode = localStorage.getItem('darkMode');
            if (savedMode === 'true') {
                setDarkMode(true);
                document.documentElement.classList.add('dark');
            }
        }
    }, []);

    // Toggle dark mode
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

    return (
        <div className='min-h-screen flex flex-col bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 transition-colors'>
            {/* Theme Toggle */}
            <div className='absolute top-4 right-4'>
                <button
                    onClick={toggleDarkMode}
                    className='p-3 rounded-full bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800'
                    aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
                >
                    {darkMode ? (
                        <Sun className='w-6 h-6 text-yellow-500' aria-hidden="true" />
                    ) : (
                        <Moon className='w-6 h-6 text-gray-700' aria-hidden="true" />
                    )}
                </button>
            </div>

            {/* Main Content */}
            <main className='flex-1 flex items-center justify-center p-8' role="main">
                <div className='max-w-2xl w-full text-center'>
                    {/* Logo/Icon */}
                    <div className='mb-8'>
                        <div className='inline-flex items-center justify-center w-24 h-24 rounded-full bg-red-100 dark:bg-red-900/30 mb-4' aria-hidden="true">
                            <Shield className='w-12 h-12 text-red-600 dark:text-red-400' />
                        </div>
                    </div>

                    {/* Title */}
                    <h1 className='text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4'>
                        Berlin Emergency
                        <span className='block text-red-600 dark:text-red-400'>Crisis Response</span>
                    </h1>

                    {/* Description */}
                    <p className='text-lg text-gray-600 dark:text-gray-300 mb-8 max-w-lg mx-auto'>
                        Get immediate assistance during <strong>earthquake</strong>, <strong>flood</strong>, or <strong>Fire</strong> emergencies in Berlin.
                    </p>

                    {/* Emergency Types */}
                    <section aria-label="Supported emergency types" className='flex justify-center gap-4 mb-8'>
                        <div className='px-4 py-2 bg-white dark:bg-gray-800 rounded-lg shadow text-gray-700 dark:text-gray-300' role="listitem">
                            <span aria-hidden="true">🏗️</span> Earthquake
                        </div>
                        <div className='px-4 py-2 bg-white dark:bg-gray-800 rounded-lg shadow text-gray-700 dark:text-gray-300' role="listitem">
                            <span aria-hidden="true">🌊</span> Flood
                        </div>
                        <div className='px-4 py-2 bg-white dark:bg-gray-800 rounded-lg shadow text-gray-700 dark:text-gray-300' role="listitem">
                            <span aria-hidden="true">🔥</span> Fire
                        </div>
                    </section>

                    {/* CTA Button */}
                    <Link
                        href='/chat'
                        className='inline-flex items-center gap-3 px-8 py-4 bg-red-600 hover:bg-red-700 text-white text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all cursor-pointer transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800'
                        aria-label="Start emergency chat conversation"
                    >
                        <AlertTriangle className='w-6 h-6' aria-hidden="true" />
                        Start Emergency Chat
                    </Link>

                    {/* Emergency Notice */}
                    <div 
                        className='mt-8 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg'
                        role="alert"
                        aria-live="polite"
                    >
                        <p className='text-yellow-800 dark:text-yellow-200 text-sm'>
                            <span aria-hidden="true">⚠️</span>{' '}
                            <strong>Life-threatening emergency?</strong> Call <strong>112</strong> immediately!
                        </p>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className='p-4 text-center text-gray-500 dark:text-gray-400 text-sm' role="contentinfo">
                Berlin Crisis Response Bot • Powered by Rasa & Next.js
            </footer>
        </div>
    );
}
