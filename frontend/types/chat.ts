/**
 * Chat Types
 * Centralized type definitions for chat functionality
 */

export interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  buttons?: Array<{ title: string; payload: string }>;
}

export interface Button {
  title: string;
  payload: string;
}

export interface MessageMetadata {
  location_coords?: {
    lat: number;
    lng: number;
  };
  emergency_type?: string;
  district?: string;
  postcode?: string;
}






