#!/usr/bin/env python3
"""
Telegram Music Bot - Like @Vkmbot_musikbot
Auto-searches and downloads music from YouTube for any non-command message.
"""

import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from downloader import MusicDownloader
import tempfile
import shutil

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramMusicBot:
    def __init__(self, token):
        self.token = token
        self.downloader = MusicDownloader()
        self.application = Application.builder().token(token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_music_search))
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🎵 **Welcome to Music Bot!** 🎵

Just send me any song name or artist, and I'll find and send you the MP3!

**How to use:**
• Simply type: "Bohemian Rhapsody Queen"  
• Or: "Imagine Dragons Believer"
• Or: "Taylor Swift Anti-Hero"

I'll automatically search YouTube and send you the best match as an MP3 file.

**Note:** Files are limited to 50MB for Telegram compatibility.

🎶 Ready to find your music? Just send me a song name! 🎶
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        
    async def handle_music_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle any non-command message as music search query"""
        query = update.message.text.strip()
        user_id = update.effective_user.id
        
        if not query:
            await update.message.reply_text("❌ Please send a song name or artist to search for.")
            return
            
        # Send "searching" message
        search_msg = await update.message.reply_text(f"🔍 Searching for: *{query}*...", parse_mode='Markdown')
        
        try:
            # Download music
            result = await self.downloader.download_music(query)
            
            if result['success']:
                # Update message to "uploading"
                await search_msg.edit_text(f"⬆️ Found! Uploading: *{result['title']}*...", parse_mode='Markdown')
                
                # Send audio file
                with open(result['file_path'], 'rb') as audio_file:
                    await update.message.reply_audio(
                        audio=audio_file,
                        title=result['title'],
                        performer=result.get('artist', 'Unknown Artist'),
                        duration=result.get('duration', 0),
                        caption=f"🎵 {result['title']}"
                    )
                
                # Delete the search message
                await search_msg.delete()
                
                # Clean up the downloaded file
                try:
                    os.remove(result['file_path'])
                    logger.info(f"Cleaned up file: {result['file_path']}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup file {result['file_path']}: {e}")
                    
            else:
                await search_msg.edit_text(f"❌ Couldn't find that song. Try again with different keywords.\n\nError: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"Error processing music search for '{query}': {e}")
            await search_msg.edit_text("❌ Something went wrong. Please try again later.")
            
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram Music Bot...")
        self.application.run_polling(drop_pending_updates=True)

def main():
    # Load bot token from environment
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Please set TELEGRAM_BOT_TOKEN in your .env file")
        return
        
    # Create and run bot
    bot = TelegramMusicBot(bot_token)
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()