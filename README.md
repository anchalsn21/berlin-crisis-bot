# Berlin Crisis Bot 🚨

An intelligent emergency response chatbot designed to assist users during earthquake, flood, and fire emergencies in Berlin. The bot provides real-time safety instructions, location-based shelter information, and critical emergency guidance.

## 🌟 Features

- **Multi-Emergency Support**: Handles earthquake, flood, and fire emergencies
- **Location-Based Assistance**: Provides nearby emergency shelters based on Berlin districts
- **Status Assessment**: Assesses user condition (safe, injured, trapped) and provides appropriate guidance
- **Critical Escalation**: Automatically escalates critical cases and provides emergency contact information
- **Interactive UI**: Modern Next.js frontend with quick reply buttons and accessibility features
- **Multi-Language NLU**: Robust natural language understanding with fallback mechanisms
- **GPS Location Support**: Accepts GPS coordinates for precise location identification

## 🏗️ Architecture

The system consists of two main components:

1. **Rasa Backend**: Natural language understanding and dialogue management
   - Rasa NLU for intent classification and entity extraction
   - Rasa Core for conversation flow management
   - Custom actions for business logic (location validation, shelter finding, status assessment)

2. **Next.js Frontend**: User interface and interaction
   - React-based chat interface
   - Quick reply buttons for faster interaction
   - Accessibility features (ARIA labels, keyboard navigation)
   - Dark mode support

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+ and npm
- Virtual environment (venv) for Python dependencies

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Build the Docker image:**
   ```bash
   docker build -t berlin-crisis-bot .
   ```

2. **Run the container:**
   ```bash
   docker run -p 7860:7860 -p 5055:5055 berlin-crisis-bot
   ```

   The bot will automatically:
   - Train the model if not found
   - Start the Rasa actions server on port 5055
   - Start the Rasa server on port 7860

### Option 2: Local Development

#### Backend Setup

1. **Create and activate virtual environment:**
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the Rasa model:**
   ```bash
   python -m rasa train --fixed-model-name crisis-bot
   ```

4. **Start the Rasa actions server** (in one terminal):
   ```bash
   python -m rasa run actions --port 5055
   ```

5. **Start the Rasa server** (in another terminal):
   ```bash
   python -m rasa run --enable-api --cors '*' --port 7860 --model models/crisis-bot.tar.gz
   ```

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set environment variables** (create `.env.local`):
   ```env
   NEXT_PUBLIC_RASA_URL=http://localhost:7860
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   ```
   http://localhost:3000
   ```

### Option 3: Using Startup Scripts

1. **Start both servers together:**
   ```bash
   python app.py
   ```

   This will automatically:
   - Train the model if needed
   - Start the actions server on port 5055
   - Start the Rasa server on port 7860

2. **Start frontend separately:**
   ```bash
   cd frontend
   npm run dev
   ```

## 📁 Project Structure

```
berlin-crisis-bot/
├── actions/              # Custom Rasa actions
│   ├── guidance/        # Safety instructions
│   ├── location/        # Location validation
│   ├── safety/          # Status assessment and escalation
│   ├── shelters/        # Shelter finding logic
│   └── utils/           # Utility functions
├── data/                # Training data
│   ├── nlu.yml         # NLU training examples
│   ├── stories.yml     # Conversation flows
│   ├── rules.yml       # Deterministic rules
│   └── berlin_shelters.json  # Shelter database
├── frontend/            # Next.js frontend application
│   ├── app/            # Next.js app directory
│   ├── components/      # React components
│   ├── hooks/          # Custom React hooks
│   └── lib/            # Utility libraries
├── models/              # Trained Rasa models
├── config.yml           # Rasa configuration
├── domain.yml           # Domain definition (intents, entities, responses)
├── endpoints.yml        # Action server configuration
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
└── app.py               # Main application entry point
```

## 🎯 Usage

### Starting a Conversation

1. Open the chat interface in your browser
2. The bot greets you and asks about the emergency type
3. Select an emergency type (Earthquake, Flood, or Fire) or use quick buttons

### Emergency Flow Examples

**Earthquake Emergency:**
1. Select "Earthquake"
2. Receive immediate safety instructions
3. Report your status (Safe, Injured, or Trapped)
4. If injured/trapped: Provide location → Receive shelter information
5. Receive follow-up options

**Flood/Fire Emergency:**
1. Select "Flood" or "Fire"
2. Provide your location in Berlin
3. Receive safety instructions
4. Receive nearby shelter information
5. Report your status
6. Receive follow-up options

### Quick Actions

Throughout the conversation, you can use quick buttons for:
- **Report Emergency**: Start a new emergency report
- **Show Shelters**: View nearby emergency shelters
- **Emergency Contacts**: View emergency contact numbers
- **Safety Instructions**: Request safety guidance

## 🔧 Configuration

### Environment Variables

**Frontend (.env.local):**
- `NEXT_PUBLIC_RASA_URL`: Rasa server URL (default: http://localhost:7860)

**Backend:**
- `PORT`: Rasa server port (default: 7860)
- Actions server runs on port 5055

### Rasa Configuration

- **NLU Pipeline**: DIETClassifier for intent and entity recognition
- **Policies**: RulePolicy, MemoizationPolicy, TEDPolicy
- **Fallback Threshold**: 0.7 (configurable in `config.yml`)

## 🧪 Testing

### Test NLU (Intent Classification)
```bash
python -m rasa test nlu --nlu testing/data/test_data.yml --model models/crisis-bot.tar.gz
```

### Test Core (Dialogue Management)
```bash
python -m rasa test core --stories testing/test_earthquake_flow.yml --model models/crisis-bot.tar.gz --endpoints endpoints.yml
```

### Run All Tests
```bash
cd scripts
./run_tests.sh
```

## 📊 Flowchart

Visual representation of the conversation flows and system architecture:

**[View Flowchart on Figma](https://www.figma.com/design/NXqdI0NOAHiggphMv86hOC/BERLIN-CRISIS-CHATBOT-FLOWCHART?m=auto&t=Cu1nd8yw2O1f2yL0-6)**

## 🛠️ Development

### Training the Model

After making changes to NLU data, stories, or rules:

```bash
python -m rasa train --fixed-model-name crisis-bot
```

### Adding New Intents

1. Add examples to `data/nlu.yml`
2. Add intent to `domain.yml`
3. Create stories/rules in `data/stories.yml` or `data/rules.yml`
4. Train the model

### Adding New Actions

1. Create action file in `actions/` directory
2. Register action in `actions/actions.py`
3. Add action to `domain.yml` under `actions:`
4. Restart the actions server

## 🌐 Deployment

The project uses a **split deployment architecture** where the backend and frontend are deployed separately:

### Backend Deployment (Hugging Face Spaces)

The Rasa backend is deployed on **Hugging Face Spaces** using Docker:

1. **Push your code to a GitHub repository** (must be public for Hugging Face Spaces)
2. **Create a new Space** on [Hugging Face Spaces](https://huggingface.co/spaces)
3. **Select Docker** as the SDK
4. **Configure the Space**:
   - Dockerfile: Uses the root `Dockerfile`
   - Port: 7860 (default Hugging Face Spaces port)
   - The container automatically:
     - Trains the model on first run if not present
     - Starts both Rasa server (port 7860) and actions server (port 5055)
     - Exposes the Rasa API endpoint

5. **Get your Space URL**: `https://your-username-berlin-crisis-bot.hf.space`

### Frontend Deployment

The Next.js frontend is deployed separately using Docker, built directly from the GitHub public repository:

1. **Ensure your repository is public** on GitHub
2. **Deploy to your preferred platform** (e.g., Vercel, Netlify, Render, Railway):
   - Point to the `frontend/` directory
   - Use the `frontend/Dockerfile` for containerized deployment
   - Set environment variable: `NEXT_PUBLIC_RASA_URL` to your Hugging Face Spaces backend URL

3. **Example environment configuration**:
   ```env
   NEXT_PUBLIC_RASA_URL=https://your-username-berlin-crisis-bot.hf.space
   ```

### Deployment Architecture

```
┌─────────────────────────┐         ┌─────────────────────────┐
│   Frontend (Docker)     │  ──────▶│  Backend (HF Spaces)   │
│   - Next.js App         │  HTTP   │  - Rasa Server          │
│   - Port: 3000/80       │         │  - Port: 7860          │
│   - GitHub Repo         │         │  - Actions: 5055        │
└─────────────────────────┘         └─────────────────────────┘
```

### Local Docker Testing

To test the full stack locally:

1. **Start backend**:
   ```bash
   docker build -t berlin-crisis-bot .
   docker run -p 7860:7860 -p 5055:5055 berlin-crisis-bot
   ```

2. **Start frontend**:
   ```bash
   cd frontend
   docker build -t berlin-crisis-frontend .
   docker run -p 3000:3000 -e NEXT_PUBLIC_RASA_URL=http://localhost:7860 berlin-crisis-frontend
   ```



## 📞 Support

For issues or questions, please open an issue on the project repository.

---

**Important**: In case of a real emergency, always call **112** (European emergency number) immediately. This bot is designed to provide guidance and information, not to replace emergency services.
