#!/bin/bash

# Rasa Testing Script
# Runs NLU tests, story tests, or both

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/.."

# Colors
if [ -t 1 ] && command -v tput > /dev/null 2>&1; then
    GREEN=$(tput setaf 2)
    RED=$(tput setaf 1)
    YELLOW=$(tput setaf 3)
    BLUE=$(tput setaf 4)
    CYAN=$(tput setaf 6)
    BOLD=$(tput bold)
    NC=$(tput sgr0)
else
    GREEN=''; RED=''; YELLOW=''; BLUE=''; CYAN=''; BOLD=''; NC=''
fi

# Default values
TEST_NLU=true
TEST_STORIES=true
VERBOSE=false
FAIL_ON_ERRORS=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --nlu-only)
            TEST_STORIES=false
            shift
            ;;
        --stories-only)
            TEST_NLU=false
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --fail-on-errors)
            FAIL_ON_ERRORS=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --nlu-only          Run only NLU tests"
            echo "  --stories-only      Run only story tests"
            echo "  --verbose, -v       Show verbose output"
            echo "  --fail-on-errors    Exit with error code if tests fail"
            echo "  --help, -h          Show this help message"
            exit 0
            ;;
        *)
            echo "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

cd "$PROJECT_DIR"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

echo "${BOLD}${CYAN}=================================================="
echo "🧪 Rasa Testing Suite"
echo "==================================================${NC}"
echo ""

# Check if model exists
MODEL_PATH="models/crisis-bot.tar.gz"
if [ ! -f "$MODEL_PATH" ]; then
    echo "${YELLOW}⚠️  Model not found. Training model...${NC}"
    $PYTHON_CMD -m rasa train --fixed-model-name crisis-bot
    if [ ! -f "$MODEL_PATH" ]; then
        echo "${RED}❌ Model training failed${NC}"
        exit 1
    fi
    echo "${GREEN}✅ Model trained${NC}"
    echo ""
fi

# Check if test files exist
NLU_TEST_FILE="testing/data/test_data.yml"
STORY_TEST_FILE="testing/test_earthquake_flow.yml"

if [ "$TEST_NLU" = true ] && [ ! -f "$NLU_TEST_FILE" ]; then
    echo "${YELLOW}⚠️  NLU test file not found: $NLU_TEST_FILE${NC}"
    echo "   Using main NLU data instead..."
    NLU_TEST_FILE="data/nlu.yml"
fi

if [ "$TEST_STORIES" = true ] && [ ! -f "$STORY_TEST_FILE" ]; then
    echo "${RED}❌ Story test file not found: $STORY_TEST_FILE${NC}"
    exit 1
fi

# Start actions server if testing stories
ACTIONS_PID=""
if [ "$TEST_STORIES" = true ]; then
    echo "${BLUE}Starting actions server...${NC}"
    $PYTHON_CMD -m rasa run actions --port 5055 > /tmp/actions_test.log 2>&1 &
    ACTIONS_PID=$!
    
    # Wait for actions server to start
    sleep 5
    
    if ps -p $ACTIONS_PID > /dev/null 2>&1; then
        echo "${GREEN}✅ Actions server started (PID: $ACTIONS_PID)${NC}"
    else
        echo "${RED}❌ Actions server failed to start${NC}"
        echo "   Check logs: /tmp/actions_test.log"
        exit 1
    fi
    echo ""
fi

# Function to cleanup
cleanup() {
    if [ -n "$ACTIONS_PID" ]; then
        echo ""
        echo "${BLUE}Stopping actions server...${NC}"
        kill $ACTIONS_PID 2>/dev/null || true
        wait $ACTIONS_PID 2>/dev/null || true
        echo "${GREEN}✅ Actions server stopped${NC}"
    fi
}

# Trap cleanup on exit
trap cleanup EXIT

# Run NLU tests
if [ "$TEST_NLU" = true ]; then
    echo "${BOLD}${BLUE}=================================================="
    echo "Test 1: NLU (Intent Classification & Entity Extraction)"
    echo "==================================================${NC}"
    echo ""
    
    if [ "$VERBOSE" = true ]; then
        $PYTHON_CMD -m rasa test nlu \
            --nlu "$NLU_TEST_FILE" \
            --model "$MODEL_PATH"
    else
        $PYTHON_CMD -m rasa test nlu \
            --nlu "$NLU_TEST_FILE" \
            --model "$MODEL_PATH" \
            --quiet
    fi
    
    NLU_EXIT_CODE=$?
    
    if [ $NLU_EXIT_CODE -eq 0 ]; then
        echo "${GREEN}✅ NLU tests passed${NC}"
    else
        echo "${RED}❌ NLU tests failed${NC}"
        if [ "$FAIL_ON_ERRORS" = true ]; then
            exit $NLU_EXIT_CODE
        fi
    fi
    echo ""
fi

# Run story tests
if [ "$TEST_STORIES" = true ]; then
    echo "${BOLD}${BLUE}=================================================="
    echo "Test 2: Story Tests (Conversation Flows)"
    echo "==================================================${NC}"
    echo ""
    
    if [ "$VERBOSE" = true ]; then
        $PYTHON_CMD -m rasa test core \
            --stories "$STORY_TEST_FILE" \
            --model "$MODEL_PATH" \
            --endpoints endpoints.yml
    else
        $PYTHON_CMD -m rasa test core \
            --stories "$STORY_TEST_FILE" \
            --model "$MODEL_PATH" \
            --endpoints endpoints.yml \
            --quiet
    fi
    
    STORY_EXIT_CODE=$?
    
    if [ $STORY_EXIT_CODE -eq 0 ]; then
        echo "${GREEN}✅ Story tests passed${NC}"
    else
        echo "${RED}❌ Story tests failed${NC}"
        if [ "$FAIL_ON_ERRORS" = true ]; then
            exit $STORY_EXIT_CODE
        fi
    fi
    echo ""
fi

# Summary
echo "${BOLD}${CYAN}=================================================="
echo "📊 Test Summary"
echo "==================================================${NC}"
echo ""
echo "Results saved in: ${BLUE}results/${NC}"
echo ""
echo "Key files:"
echo "  - ${BLUE}results/intent_report.json${NC} - Intent classification results"
echo "  - ${BLUE}results/story_report.json${NC} - Story test results"
echo "  - ${BLUE}results/failed_test_stories.yml${NC} - Failed stories"
echo "  - ${BLUE}results/intent_errors.json${NC} - NLU misclassifications"
echo ""

if [ "$TEST_NLU" = true ] && [ "$TEST_STORIES" = true ]; then
    if [ $NLU_EXIT_CODE -eq 0 ] && [ $STORY_EXIT_CODE -eq 0 ]; then
        echo "${GREEN}✅ All tests passed!${NC}"
        exit 0
    else
        echo "${YELLOW}⚠️  Some tests failed. Check results/ directory for details.${NC}"
        exit 1
    fi
elif [ "$TEST_NLU" = true ]; then
    exit $NLU_EXIT_CODE
elif [ "$TEST_STORIES" = true ]; then
    exit $STORY_EXIT_CODE
fi
