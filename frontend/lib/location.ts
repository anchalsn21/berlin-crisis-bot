/**
 * Location Utilities
 * Handles GPS, postcode, and district name processing
 * 
 * Note: Actual validation is done by Rasa backend
 * These utilities just help with UI presentation and GPS conversion
 */

/**
 * Berlin district list for quick selection
 */
export const BERLIN_DISTRICTS = [
  'Mitte',
  'Kreuzberg',
  'Prenzlauer Berg',
  'Charlottenburg',
  'Friedrichshain',
  'Schöneberg',
  'Neukölln',
  'Tempelhof',
  'Steglitz',
  'Spandau',
  'Pankow',
  'Wedding',
  'Lichtenberg',
  'Marzahn',
  'Treptow',
  'Reinickendorf',
  'Wilmersdorf',
  'Köpenick',
  'Zehlendorf',
  'Hellersdorf',
];

/**
 * Get user's current GPS coordinates
 * @returns Promise with lat/lng coordinates
 */
export function getCurrentPosition(): Promise<GeolocationPosition> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by this browser'));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      resolve,
      (error) => {
        switch (error.code) {
          case error.PERMISSION_DENIED:
            reject(new Error('Location permission denied. Please type your district manually.'));
            break;
          case error.POSITION_UNAVAILABLE:
            reject(new Error('Location unavailable. Please type your district manually.'));
            break;
          case error.TIMEOUT:
            reject(new Error('Location request timed out. Please type your district manually.'));
            break;
          default:
            reject(new Error('Unable to get location. Please type your district manually.'));
        }
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000, // 5 minutes
      }
    );
  });
}

/**
 * Reverse geocode coordinates to Berlin district using Nominatim
 * @param lat - Latitude
 * @param lng - Longitude
 * @returns District name or null
 */
export async function reverseGeocode(lat: number, lng: number): Promise<string | null> {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1&accept-language=en`,
      {
        headers: {
          'User-Agent': 'Berlin-Emergency-Chatbot/1.0',
        },
      }
    );

    if (!response.ok) {
      throw new Error('Geocoding service unavailable');
    }

    const data = await response.json();
    const address = data.address || {};

    // Try to extract Berlin district
    const suburb = address.suburb || address.neighbourhood || '';
    const city = address.city || address.town || '';

    // Check if it's in Berlin
    if (!city.toLowerCase().includes('berlin')) {
      throw new Error('Location is not in Berlin');
    }

    return suburb || 'Mitte'; // Default to Mitte if suburb unknown
  } catch (error) {
    console.error('Reverse geocoding error:', error);
    return null;
  }
}

/**
 * Get district from GPS coordinates
 * Combines getCurrentPosition and reverseGeocode
 * @returns District name
 */
export async function getDistrictFromGPS(): Promise<string> {
  const position = await getCurrentPosition();
  const { latitude, longitude } = position.coords;
  
  const district = await reverseGeocode(latitude, longitude);
  
  if (!district) {
    throw new Error('Could not determine district from GPS. Please type your district manually.');
  }
  
  return district;
}

