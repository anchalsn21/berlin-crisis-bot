# Location Validation Fix for Injured/Trapped Users

## Problem
When users reported being injured or trapped in earthquake emergencies, location validation was failing. Users could provide district names like "Kreuzberg", "Charlottenburg", "Prenzlauer Berg", "Mitte", or postcodes like "12169", but the bot responded with "⚠️ No response received."

## Root Cause
In `action_validate_location`, there was a check that prevented location validation when `escalation_required` was True:

```python
escalation_required = tracker.get_slot('escalation_required')
if escalation_required:
    return []
```

This check was blocking location validation for injured/trapped users, even though location is critical for emergency services to find them.

## Solution
Removed the `escalation_required` check that was blocking location validation. Location validation is now allowed for all users, including those requiring escalation.

## Changes Made

### 1. `actions/location/validate_location.py`
- **Removed**: The `escalation_required` check that was preventing location validation (lines 80-82)
- **Updated**: `_trigger_shelter_finding` to not auto-trigger shelters for earthquake emergencies (let stories handle the flow)

### 2. Stories Already Exist
The following stories handle location text input after critical location question:
- `earthquake - injured - location text only`
- `earthquake - trapped - location text only`
- `earthquake - nlu_fallback after status - injured flow`
- `earthquake - nlu_fallback after status - trapped flow`

## How It Works Now

1. User: "I'm injured" or "I'm trapped"
2. Bot: Shows critical instructions (`utter_injured_response` or `utter_trapped_response`)
3. Bot: Asks for location (`utter_ask_location_critical`)
4. User: Provides location (e.g., "Kreuzberg", "12169")
5. **`action_validate_location` is now called** (previously blocked by `escalation_required` check)
6. Bot: Validates location and shows shelters
7. Bot: Shows conclusion with buttons

## Testing
After training, test the flow:
1. Say: "Earthquake"
2. Say: "I'm injured"
3. Provide location: "Kreuzberg"
4. Verify: Location is validated and shelters are shown

## Expected Behavior
- Location validation works for injured/trapped users
- District names are recognized (Kreuzberg, Charlottenburg, Mitte, etc.)
- Postcodes are recognized (12169, etc.)
- Shelters are shown after location validation
- Conclusion flow works correctly
