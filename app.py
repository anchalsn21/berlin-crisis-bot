#!/usr/bin/env python3
"""
Entry point for Hugging Face Spaces.
Starts both Rasa server and actions server.
"""
import os
import subprocess
import sys
import time
import signal
from multiprocessing import Process

def start_actions_server():
    """Start Rasa actions server on port 5055."""
    print("Starting Rasa actions server on port 5055...", flush=True)
    cmd = [sys.executable, '-m', 'rasa', 'run', 'actions', '--port', '5055']
    subprocess.run(cmd)

def start_rasa_server():
    """Start main Rasa server."""
    port = os.environ.get('PORT', '7860')
    model_path = 'models/crisis-bot.tar.gz'
    
    print(f"Starting Rasa server on port {port}...", flush=True)
    print(f"Model: {model_path}", flush=True)
    
    cmd = [
        sys.executable, '-m', 'rasa', 'run',
        '--enable-api',
        '--cors', '*',
        '--port', port
    ]
    
    if os.path.exists(model_path):
        cmd.extend(['--model', model_path])
    
    subprocess.run(cmd)

def main():
    """Main entry point - starts both servers."""
    # Check if model exists, if not, train it
    model_path = 'models/crisis-bot.tar.gz'
    if not os.path.exists(model_path):
        print("Model not found. Training model...", flush=True)
        subprocess.run([
            sys.executable, '-m', 'rasa', 'train',
            '--fixed-model-name', 'crisis-bot'
        ], check=True)
        print("Model training completed.", flush=True)
    
    # Start actions server in background process
    actions_process = Process(target=start_actions_server)
    actions_process.start()
    
    # Wait a bit for actions server to start
    time.sleep(5)
    
    # Start main Rasa server (this will block)
    try:
        start_rasa_server()
    except KeyboardInterrupt:
        print("\nShutting down...", flush=True)
        actions_process.terminate()
        actions_process.join()
        sys.exit(0)

if __name__ == '__main__':
    main()

