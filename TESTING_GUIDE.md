# Rasa Testing Guide

This guide explains how to test your Berlin Crisis Bot Rasa project.

## Types of Tests

Rasa supports three main types of tests:

1. **NLU Tests** - Test intent classification and entity extraction
2. **Story Tests** - Test conversation flows and dialogue management
3. **End-to-End Tests** - Test complete conversations

## Prerequisites

1. Ensure your model is trained:
   ```bash
   cd "/home/anchal/Crisis management Chatbot/berlin-crisis-bot"
   source venv/bin/activate
   python -m rasa train --fixed-model-name crisis-bot
   ```

2. Ensure your actions server can run (for story tests):
   ```bash
   rasa run actions --port 5055
   ```

## Running Tests

### 1. Test NLU (Intent Classification & Entity Extraction)

Test how well the model classifies intents and extracts entities:

```bash
cd "/home/anchal/Crisis management Chatbot/berlin-crisis-bot"
source venv/bin/activate

# Test NLU with your test data
python -m rasa test nlu --nlu testing/data/test_data.yml --model models/crisis-bot.tar.gz

# Or test with the main NLU data
python -m rasa test nlu --nlu data/nlu.yml --model models/crisis-bot.tar.gz
```

**Output**: Results will be saved in `results/` directory:
- `intent_report.json` - Intent classification accuracy
- `intent_confusion_matrix.png` - Visual confusion matrix
- `intent_errors.json` - Misclassified examples

### 2. Test Stories (Conversation Flows)

Test complete conversation flows:

```bash
cd "/home/anchal/Crisis management Chatbot/berlin-crisis-bot"
source venv/bin/activate

# Start actions server in background (required for story tests)
rasa run actions --port 5055 &
ACTIONS_PID=$!

# Wait for actions server to start
sleep 5

# Run story tests
python -m rasa test core \
  --stories testing/test_earthquake_flow.yml \
  --model models/crisis-bot.tar.gz \
  --endpoints endpoints.yml

# Or test all stories
python -m rasa test core \
  --stories testing/ \
  --model models/crisis-bot.tar.gz \
  --endpoints endpoints.yml

# Stop actions server
kill $ACTIONS_PID
```

**Output**: Results will be saved in `results/` directory:
- `story_report.json` - Story test results
- `failed_test_stories.yml` - Stories that failed
- `stories_with_warnings.yml` - Stories with warnings

### 3. Test Everything Together

Run both NLU and story tests:

```bash
cd "/home/anchal/Crisis management Chatbot/berlin-crisis-bot"
source venv/bin/activate

# Start actions server
rasa run actions --port 5055 &
ACTIONS_PID=$!
sleep 5

# Run all tests
python -m rasa test \
  --nlu testing/data/test_data.yml \
  --stories testing/test_earthquake_flow.yml \
  --model models/crisis-bot.tar.gz \
  --endpoints endpoints.yml

# Stop actions server
kill $ACTIONS_PID
```

### 4. Test with Cross-Validation

Test model performance with cross-validation (splits data into folds):

```bash
cd "/home/anchal/Crisis management Chatbot/berlin-crisis-bot"
source venv/bin/activate

# NLU cross-validation
python -m rasa test nlu --nlu data/nlu.yml --cross-validation

# Story cross-validation
python -m rasa test core --stories data/stories.yml --cross-validation
```

## Test File Structure

Your test files are located in:
- `testing/test_earthquake_flow.yml` - Earthquake emergency flow tests
- `testing/test_earthquake_emergencies.yml` - Additional earthquake tests
- `testing/test_conversations.yml` - General conversation tests
- `testing/data/test_data.yml` - NLU test examples

## Creating New Tests

### Adding NLU Test Examples

Add examples to `testing/data/test_data.yml`:

```yaml
version: "3.1"

nlu:
- intent: report_fire
  examples: |
    - there's a fire in my building
    - fire emergency
    - smoke detected

- intent: report_injured
  examples: |
    - i'm hurt
    - bleeding
    - injured person
```

### Adding Story Tests

Add stories to `testing/test_earthquake_flow.yml` or create a new file:

```yaml
version: "3.1"

stories:
- story: test_fire_emergency_happy_path
  steps:
    - intent: report_fire
    - action: action_reset_emergency_slots
    - action: utter_acknowledge_fire
    - action: utter_ask_location
    - intent: inform_location
      entities:
        - district: "Charlottenburg"
    - action: action_validate_location
    - slot_was_set:
        - location_validated: true
        - district: "Charlottenburg"
    - action: action_provide_safety_instructions
    - action: action_find_nearest_shelters
    - action: action_ask_status
    - intent: report_safe
    - action: action_assess_status
    - action: utter_anything_else
```

## Understanding Test Results

### NLU Test Results

- **Intent Accuracy**: Percentage of correctly classified intents
- **Entity F1 Score**: F1 score for entity extraction
- **Confusion Matrix**: Shows which intents are confused with each other

### Story Test Results

- **Story Accuracy**: Percentage of stories that passed
- **Action Predictions**: Shows if actions were predicted correctly
- **Failed Stories**: Lists stories that didn't match expected flow

## Quick Test Commands

Use the provided test script:

```bash
cd "/home/anchal/Crisis management Chatbot/berlin-crisis-bot"
./scripts/run_tests.sh
```

Or run individual test types:

```bash
# Test NLU only
./scripts/run_tests.sh --nlu-only

# Test stories only
./scripts/run_tests.sh --stories-only

# Test with verbose output
./scripts/run_tests.sh --verbose
```

## Troubleshooting

### Actions Server Not Running

If story tests fail with "Connection refused":
```bash
# Start actions server manually
rasa run actions --port 5055
```

### Model Not Found

If you get "Model not found" error:
```bash
python -m rasa train --fixed-model-name crisis-bot
```

### Test Failures

1. Check `results/failed_test_stories.yml` for failed stories
2. Review `results/intent_errors.json` for NLU misclassifications
3. Update training data if needed
4. Retrain the model
5. Re-run tests

## Best Practices

1. **Test Regularly**: Run tests after making changes to NLU data, stories, or actions
2. **Add Test Cases**: Add tests for new features or edge cases
3. **Review Results**: Check confusion matrices to identify patterns
4. **Update Training Data**: If tests fail, add more training examples
5. **Keep Tests Updated**: Update tests when you change conversation flows

## Continuous Integration

For CI/CD pipelines, you can run tests automatically:

```bash
# Exit with error code if tests fail
python -m rasa test \
  --nlu testing/data/test_data.yml \
  --stories testing/test_earthquake_flow.yml \
  --model models/crisis-bot.tar.gz \
  --endpoints endpoints.yml \
  --fail-on-prediction-errors
```
