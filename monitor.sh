#!/bin/bash

cleanup() {
    echo "Cleaning up temporary files..."
    find /app/temp -type f -mtime +1 -delete
}

while true; do
    python bot.py
    
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "Bot exited normally with code 0. Exiting."
        break
    else
        echo "Bot crashed with exit code $EXIT_CODE. Restarting in 5 seconds..."
        cleanup
        sleep 5
    fi
done
