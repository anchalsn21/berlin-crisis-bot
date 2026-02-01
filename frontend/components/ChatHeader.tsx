/**
 * ChatHeader Component
 * Header with navigation and dark mode toggle
 */

'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {ArrowLeft, Moon, Sun, Copy, Check} from 'lucide-react';
import { Message } from '@/types/chat';

interface ChatHeaderProps {
    darkMode: boolean;
    onToggleDarkMode: () => void;
    messages?: Message[];
}

export default function ChatHeader({darkMode, onToggleDarkMode, messages = []}: ChatHeaderProps) {
    const [isDebugMode, setIsDebugMode] = useState(false);
    const [copied, setCopied] = useState(false);

    useEffect(() => {
        if (typeof window !== 'undefined') {
            const urlParams = new URLSearchParams(window.location.search);
            setIsDebugMode(urlParams.get('debug') === 'true');
        }
    }, []);

    const copyConversation = () => {
        if (!messages || messages.length === 0) return;

        const conversationText = messages.map(msg => {
            const sender = msg.isUser ? 'User' : '🤖 Crisis Bot';
            const time = msg.timestamp.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
            return `${sender}\n${msg.text}\n${time}`;
        }).join('\n\n');

        navigator.clipboard.writeText(conversationText).then(() => {
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        });
    };

    return (
        <header 
            className='flex-shrink-0 bg-white dark:bg-gray-800 shadow-md px-4 py-3 flex items-center justify-between border-b border-gray-200 dark:border-gray-700'
            role="banner"
        >
            <div className='flex items-center gap-3'>
                <Link 
                    href='/' 
                    className='p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800'
                    aria-label='Return to home page'
                >
                    <ArrowLeft className='w-5 h-5 text-gray-600 dark:text-gray-300' aria-hidden="true" />
                </Link>
                <div>
                    <h1 className='font-bold text-gray-900 dark:text-white'>
                        <span aria-hidden="true">🚨</span> Berlin Emergency Response
                    </h1>
                    <p className='text-xs text-gray-500 dark:text-gray-400' aria-label='Emergency types: Earthquake, Flood, Fire'>
                        Earthquake • Flood • Fire
                    </p>
                </div>
            </div>
            <div className='flex items-center gap-2' role="toolbar" aria-label="Header actions">
                {isDebugMode && (
                    <button
                        onClick={copyConversation}
                        className='flex items-center gap-2 px-3 py-2 text-sm bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800'
                        aria-label={copied ? 'Conversation copied to clipboard' : 'Copy conversation to clipboard'}
                    >
                        {copied ? (
                            <>
                                <Check className='w-4 h-4' aria-hidden="true" />
                                <span>Copied!</span>
                            </>
                        ) : (
                            <>
                                <Copy className='w-4 h-4' aria-hidden="true" />
                                <span>Copy Chat</span>
                            </>
                        )}
                    </button>
                )}
                <button
                    onClick={onToggleDarkMode}
                    className='p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800'
                    aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
                >
                    {darkMode ? (
                        <Sun className='w-5 h-5 text-yellow-500' aria-hidden="true" />
                    ) : (
                        <Moon className='w-5 h-5 text-gray-600' aria-hidden="true" />
                    )}
                </button>
            </div>
        </header>
    );
}
