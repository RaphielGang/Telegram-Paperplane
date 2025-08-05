#! /usr/bin/env bash
# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

echo "Starting Paperplane Userbot..."

# Check if we're using external Redis (Docker Compose)
REDIS_HOST=${REDIS_HOST:-localhost}

if [ "$REDIS_HOST" = "localhost" ]; then
    # Start local Redis server
    echo "Starting local Redis server..."
    redis-server --daemonize yes --bind 127.0.0.1 --port 6379
    
    # Wait for Redis to start
    sleep 2
    
    # Check if Redis is running
    if redis-cli ping > /dev/null 2>&1; then
        echo "Redis server started successfully"
    else
        echo "Warning: Redis server failed to start"
    fi
else
    echo "Using external Redis at $REDIS_HOST"
    
    # Wait for external Redis to be available
    echo "Waiting for Redis to be available..."
    while ! redis-cli -h "$REDIS_HOST" ping > /dev/null 2>&1; do
        echo "Waiting for Redis..."
        sleep 2
    done
    echo "Redis is available"
fi

# Start the userbot
echo "Starting userbot..."
python3 -m userbot
