# Slot Persistence - Strict Linear Flow

## Overview
Location (`district`) and emergency type (`emergency_type`) slots now persist across conversations until the user explicitly reports a new emergency or clicks "Report Emergency" button.

## How It Works

### Slots Reset Only When:
1. **User reports a new emergency** (earthquake/flood/fire)
   - Stories call `action_reset_emergency_slots` at the start
   - Rule `Handle earthquake report anytime` calls it
   - Rule `Handle flood report anytime` calls it
   - Rule `Handle fire report anytime` calls it

2. **User clicks "Report Emergency" button**
   - Rule `Handle request emergency type anytime` calls `action_reset_emergency_slots`
   - This explicitly resets all slots to start fresh

### Slots Persist When:
- User clicks "Show Shelters" after conclusion
- User clicks "Safety Instructions" after conclusion
- User clicks "Emergency Contacts" after conclusion
- User says "I'm all set" (goodbye)
- Any other interaction that doesn't involve reporting a new emergency

## Changes Made

### 1. `actions/safety/reset_emergency_slots.py`
- **Added**: `emergency_type` reset to the action
- **Purpose**: Ensures both `emergency_type` and `district` are cleared when starting a new emergency
- **Called by**: All emergency report rules/stories and "Report Emergency" button rule

### 2. Flow Behavior
- **Strict and Linear**: Flows are straightforward - slots reset only at explicit emergency start
- **Simple**: No complex slot management - just reset when new emergency, persist otherwise

## Example Flow

### Scenario 1: User reports earthquake, then requests shelters
1. User: "Earthquake" → `action_reset_emergency_slots` called → `emergency_type` = "earthquake", `district` = None
2. User: "I'm safe" → Flow completes
3. User: "Show Shelters" → `district` still None → Asks for location
4. User: "Kreuzberg" → `district` = "Kreuzberg" → Shows shelters
5. User: "I'm all set" → Slots persist: `emergency_type` = "earthquake", `district` = "Kreuzberg"
6. User: "Show Shelters" → Uses persisted `district` → Shows shelters immediately

### Scenario 2: User reports new emergency
1. User: "Show Shelters" → Uses persisted slots
2. User: "Report Emergency" → `action_reset_emergency_slots` called → All slots cleared
3. User: "Earthquake" → New emergency flow starts with clean slate

## Benefits
- **User-friendly**: Don't need to re-enter location/emergency type for repeated requests
- **Strict**: Clear rules - slots reset only when explicitly starting new emergency
- **Simple**: Linear flow - no complex slot management logic
- **Consistent**: Same behavior across all emergency types
