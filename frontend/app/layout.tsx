/**
 * Berlin Crisis Response Chatbot - Root Layout
 * Provides global styles and theme support
 */

import type {Metadata} from 'next';
import './globals.css';

export const metadata: Metadata = {
    title: 'Berlin Emergency Crisis Response',
    description: 'Emergency response chatbot for earthquake, flood, and Fire situations in Berlin',
};

export default function RootLayout({children}: {children: React.ReactNode}) {
    return (
        <html lang='en'>
            <body className='min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors'>{children}</body>
        </html>
    );
}
