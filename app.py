#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from multiprocessing import Process

def start_actions_server():
    print("Starting Rasa actions server on port 5055...", flush=True)
    cmd = [sys.executable, '-m', 'rasa', 'run', 'actions', '--port', '5055']
    subprocess.run(cmd)

def start_rasa_server():
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
    model_path = 'models/crisis-bot.tar.gz'
    if not os.path.exists(model_path):
        print("Model not found. Training model...", flush=True)
        subprocess.run([
            sys.executable, '-m', 'rasa', 'train',
            '--fixed-model-name', 'crisis-bot'
        ], check=True)
        print("Model training completed.", flush=True)
    
    actions_process = Process(target=start_actions_server)
    actions_process.start()
    
    time.sleep(5)
    
    try:
        start_rasa_server()
    except KeyboardInterrupt:
        print("\nShutting down...", flush=True)
        actions_process.terminate()
        actions_process.join()
        sys.exit(0)

if __name__ == '__main__':
    main()

