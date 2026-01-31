# Earthquake Emergency Flow Verification

## Overview
This document verifies the injured/trapped flow for earthquake emergencies, including handling of NLU fallback scenarios.

## Flow Structure

### Standard Flow (when NLU correctly classifies)
1. User: "Earthquake"
2. Bot: Safety instructions
3. Bot: "Are you injured or in immediate danger?"
4. User: "I'm injured" (intent: `report_injured`)
5. Bot: Critical instructions (`utter_injured_response`)
6. Bot: Ask for location (`utter_ask_location_critical`)
7. User: Provides location
8. Bot: Show shelters
9. Bot: Conclusion (`utter_anything_else`)

### Fallback Flow (when NLU classifies as `nlu_fallback`)
1. User: "Earthquake"
2. Bot: Safety instructions
3. Bot: "Are you injured or in immediate danger?"
4. User: "I'm injured" (intent: `nlu_fallback` - misclassified)
5. `action_assess_status` extracts "injured" from text
6. Sets `injury_status: injured` slot
7. Bot: Critical instructions (`utter_injured_response`)
8. Bot: Ask for location (`utter_ask_location_critical`)
9. User: Provides location
10. Bot: Show shelters
11. Bot: Conclusion (`utter_anything_else`)

## Key Components

### 1. `action_assess_status` Enhancement
**File**: `actions/safety/assess_status.py`

**Key Logic**:
- Checks if `latest_intent == 'nlu_fallback'` and `status_asked == true`
- Extracts status from text using keyword matching:
  - Injured: "injured", "hurt", "bleeding", "wounded", "broken", "i'm injured", "i am injured"
  - Trapped: "trapped", "i'm trapped", "we're trapped", "i am trapped", "we are trapped", "stuck", "can't get out"
  - Safe: "safe", "fine", "okay", "ok", "good", "well", "alright", "i'm all set"
- Sets `injury_status` slot based on extracted status
- Returns empty list if status cannot be determined (triggers fallback message)

### 2. Stories for NLU Fallback
**File**: `data/stories.yml`

**Stories Added**:
- `earthquake - nlu_fallback after status - injured flow`
- `earthquake - nlu_fallback after status - trapped flow`
- `earthquake - nlu_fallback after status - safe flow`

**Story Pattern**:
```yaml
- story: earthquake - nlu_fallback after status - injured flow
  steps:
    - action: action_ask_status
    - slot_was_set:
        - status_asked: true
    - intent: nlu_fallback
    - action: action_assess_status
    - slot_was_set:
        - injury_status: injured
    - action: action_escalate_emergency
    - action: utter_injured_response
    - action: utter_ask_location_critical
    - intent: inform_location
    - action: action_validate_location
    - slot_was_set:
        - location_validated: true
    - action: action_find_nearest_shelters
    - action: utter_anything_else
```

### 3. Test Cases
**File**: `testing/test_earthquake_flow.yml`

**Tests Added**:
- `test_earthquake_nlu_fallback_injured_extracted`
- `test_earthquake_nlu_fallback_trapped_extracted`
- `test_earthquake_nlu_fallback_safe_extracted`

## Verification Checklist

### ✅ Code Logic
- [x] `action_assess_status` handles `nlu_fallback` when `status_asked` is true
- [x] Text extraction logic correctly identifies injured/trapped/safe keywords
- [x] Slot is set correctly (`injury_status`)
- [x] Returns empty list when status cannot be determined

### ✅ Stories
- [x] Stories exist for injured flow with `nlu_fallback`
- [x] Stories exist for trapped flow with `nlu_fallback`
- [x] Stories exist for safe flow with `nlu_fallback`
- [x] Stories follow correct sequence: critical instructions → location → shelters → conclusion

### ✅ Flow Order
- [x] Critical instructions appear BEFORE location question
- [x] Location question appears AFTER critical instructions
- [x] Shelters shown AFTER location validation
- [x] Conclusion appears at the end

### ✅ Test Coverage
- [x] Tests exist for injured with `nlu_fallback`
- [x] Tests exist for trapped with `nlu_fallback`
- [x] Tests exist for safe with `nlu_fallback`

## Testing Instructions

### 1. Train the Model
```bash
cd "/home/anchal/Crisis management Chatbot/berlin-crisis-bot"
./scripts/train_model.sh
```

### 2. Test the Flow Manually
1. Start Rasa server: `./scripts/start_rasa_server.sh`
2. Start actions server: `./scripts/start_actions_server.sh`
3. Test conversation:
   - Say: "Earthquake"
   - Say: "I'm injured" (should work even if NLU classifies as `nlu_fallback`)
   - Verify: Critical instructions appear FIRST
   - Verify: Location question appears SECOND
   - Provide location: "Kreuzberg"
   - Verify: Shelters are shown
   - Verify: Conclusion with buttons appears

### 3. Run Automated Tests
```bash
cd "/home/anchal/Crisis management Chatbot/berlin-crisis-bot"
python -m rasa test --stories testing/test_earthquake_flow.yml --model models/crisis-bot.tar.gz
```

## Expected Behavior

### When User Says "I'm injured" (correctly classified)
- Intent: `report_injured`
- Story: `earthquake - injured - complete flow`
- Flow: Instructions → Critical response → Location → Shelters → Conclusion

### When User Says "I'm injured" (misclassified as `nlu_fallback`)
- Intent: `nlu_fallback`
- `action_assess_status` extracts "injured" from text
- Sets `injury_status: injured` slot
- Story: `earthquake - nlu_fallback after status - injured flow`
- Flow: Instructions → Critical response → Location → Shelters → Conclusion

## Potential Issues and Solutions

### Issue 1: NLU still misclassifies after training
**Solution**: The fallback handling ensures the flow works even if NLU misclassifies. The text extraction in `action_assess_status` will handle it.

### Issue 2: Status not extracted from text
**Solution**: Check that `status_asked` slot is set to `true` before `action_assess_status` is called. Verify the keyword matching logic covers the user's phrasing.

### Issue 3: Stories don't match
**Solution**: Ensure `status_asked: true` is set before the `nlu_fallback` intent. Check that `injury_status` slot is set correctly by `action_assess_status`.

## Summary

The flow has been enhanced to handle NLU fallback scenarios where "I'm injured" or "I'm trapped" are misclassified. The `action_assess_status` action now extracts status from text when NLU falls back, ensuring the critical emergency flow continues correctly. The flow order is maintained: critical instructions appear BEFORE location question, ensuring users get immediate safety guidance.
