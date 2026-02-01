/**
 * Rasa API Client
 * Handles all communication with Rasa backend
 * 
 * All decision-making logic is in Rasa - this is just UI communication
 */

import axios from 'axios';

// Construct Rasa server URL from environment variables
// Priority: NEXT_PUBLIC_RASA_URL > RASA_SERVER_HOST + RASA_SERVER_PORT > default
function getRasaUrl(): string {
  // Direct URL override (highest priority)
  if (process.env.NEXT_PUBLIC_RASA_URL) {
    return process.env.NEXT_PUBLIC_RASA_URL;
  }
  
  // Construct from host and port
  const host = process.env.NEXT_PUBLIC_RASA_SERVER_HOST;
  const port = process.env.NEXT_PUBLIC_RASA_SERVER_PORT || '5005';
  
  if (host) {
    // Use https for Render public URLs, http for internal/localhost
    const protocol = host.includes('.onrender.com') ? 'https' : 'http';
    return `${protocol}://${host}:${port}`;
  }
  
  // Fallback to localhost
  return 'http://localhost:5005';
}

const RASA_URL = getRasaUrl();

/**
 * Message from Rasa
 */
export interface RasaMessage {
  recipient_id: string;
  text?: string;
  buttons?: Array<{
    title: string;
    payload: string;
  }>;
  image?: string;
  custom?: Record<string, any>;
}

/**
 * Metadata to send with messages
 * Used by Rasa actions to get additional context
 */
export interface MessageMetadata {
  location_coords?: {
    lat: number;
    lng: number;
  };
  emergency_type?: string;
  district?: string;
  postcode?: string;
}

/**
 * Send a message to Rasa and get responses
 * 
 * @param senderId - Unique session identifier
 * @param message - User's message text
 * @param metadata - Optional metadata (GPS coords, etc.)
 * @returns Array of Rasa response messages
 */
export async function sendToRasa(
  senderId: string,
  message: string,
  metadata?: MessageMetadata
): Promise<RasaMessage[]> {
  try {
    const response = await axios.post(
      `${RASA_URL}/webhooks/rest/webhook`,
      {
        sender: senderId,
        message: message,
        metadata: metadata || {},
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 30000, // 30 second timeout
      }
    );

    return response.data as RasaMessage[];
  } catch (error: any) {
    console.error('Rasa communication error:', error);
    
    // Return error message for UI
    return [{
      recipient_id: senderId,
      text: '⚠️ Unable to connect to the emergency response system. Please call **112** if this is an emergency.',
    }];
  }
}

/**
 * Check if Rasa server is available
 */
export async function checkRasaHealth(): Promise<boolean> {
  try {
    const response = await axios.get(`${RASA_URL}/`, { timeout: 5000 });
    return response.status === 200;
  } catch {
    return false;
  }
}

