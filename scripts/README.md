# Scripts

This folder contains utility scripts for training and running the Rasa chatbot.

## Scripts

### train_model.sh
Trains the Rasa model and saves it as `models/crisis-bot.tar.gz`.

**Usage:**
```bash
./scripts/train_model.sh
```

### start_actions_server.sh
Starts the Rasa actions server on port 5055.

**Usage:**
```bash
./scripts/start_actions_server.sh
```

### start_rasa_server.sh
Starts the main Rasa server on port 7860 (or PORT environment variable).

**Usage:**
```bash
./scripts/start_rasa_server.sh
```

Or with custom port:
```bash
PORT=8080 ./scripts/start_rasa_server.sh
```

## Running Both Servers

To run both servers simultaneously, use two terminal windows:

**Terminal 1:**
```bash
./scripts/start_actions_server.sh
```

**Terminal 2:**
```bash
./scripts/start_rasa_server.sh
```
