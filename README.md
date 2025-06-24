# Telegram Music Bot 🎵

A simple Telegram bot that automatically searches and downloads music from YouTube when you send any message (no commands needed).

## Features

- **Auto-Search**: Just send any message with a song name, and the bot will search and download it
- **YouTube Integration**: Uses yt_dlp to extract high-quality audio from YouTube
- **MP3 Conversion**: Automatically converts audio to MP3 format
- **Smart Limits**: 
  - File size limit: 50MB (Telegram maximum)
  - Duration limit: 10 minutes
- **Clean Interface**: No complex commands - just send song names!

## Setup

### Prerequisites

1. **FFmpeg** - Required for audio conversion
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS (with Homebrew)
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

2. **Python 3.10+**

### Installation

1. **Clone/Download** this project

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create Telegram Bot**:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow the prompts
   - Copy your bot token

4. **Configure environment**:
   - Update `.env` file with your bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

5. **Run the bot**:
```bash
python bot.py
```

## Usage

1. **Start the bot**: Send `/start` to your bot
2. **Search music**: Just send any message like:
   - "Bohemian Rhapsody Queen"
   - "Imagine Dragons Believer"  
   - "Taylor Swift Anti-Hero"
3. **Get your music**: The bot will search, download, and send you the MP3!

## How it Works

1. **Message Detection**: Every non-command message is treated as a search query
2. **YouTube Search**: Uses `yt_dlp` with `ytsearch1:` to find the best match
3. **Audio Extraction**: Downloads the best audio quality available
4. **MP3 Conversion**: Converts to MP3 using FFmpeg
5. **File Delivery**: Sends the MP3 file via Telegram
6. **Cleanup**: Automatically removes temporary files

## Deployment on Render

This bot is designed to run independently on Render's free tier:

1. **Create new Web Service** on Render
2. **Connect your repository**
3. **Set environment variables**:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
4. **Build & Deploy**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`

## File Structure

```
/app/
├── bot.py              # Main Telegram bot logic
├── downloader.py       # YouTube search & audio extraction
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (bot token)
└── README.md          # This file
```

## Limitations

- **File Size**: Maximum 50MB (Telegram limit)
- **Duration**: Maximum 10 minutes per song
- **Quality**: 192kbps MP3 (good balance of quality/size)
- **Rate Limits**: Respects YouTube's rate limiting

## Troubleshooting

**Bot not responding?**
- Check if bot token is correct
- Verify FFmpeg is installed
- Check logs for errors

**Downloads failing?**
- Update yt_dlp: `pip install --upgrade yt-dlp`
- Check internet connection
- Try different search terms

**Files too large?**
- Bot automatically rejects files > 50MB
- Try searching for shorter versions

## License

Free to use and modify for personal projects.