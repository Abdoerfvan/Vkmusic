#!/bin/bash
# Startup script for Telegram Music Bot on Render

echo "Installing FFmpeg..."
apt-get update && apt-get install -y ffmpeg

echo "Starting Telegram Music Bot..."
python bot.py