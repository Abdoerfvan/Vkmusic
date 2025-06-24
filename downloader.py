"""
Music Downloader - YouTube Search and Audio Extraction
Uses yt_dlp to search YouTube and extract audio as MP3
"""

import os
import tempfile
import asyncio
import logging
from typing import Dict, Optional
import yt_dlp

logger = logging.getLogger(__name__)

class MusicDownloader:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        
        # yt_dlp options for audio extraction
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.temp_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'embed_subs': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
        
    async def download_music(self, query: str) -> Dict:
        """
        Search YouTube and download music as MP3
        
        Args:
            query: Search query (song name, artist, etc.)
            
        Returns:
            Dict with success status, file path, title, and other metadata
        """
        try:
            # Use ytsearch1: to get the best single result
            search_query = f"ytsearch1:{query}"
            
            logger.info(f"Searching for: {query}")
            
            # Run yt_dlp in thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self._download_sync, search_query)
            
            return result
            
        except Exception as e:
            logger.error(f"Error downloading music for '{query}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def _download_sync(self, search_query: str) -> Dict:
        """Synchronous download function to run in executor"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(search_query, download=False)
                
                if not info or 'entries' not in info or not info['entries']:
                    return {
                        'success': False,
                        'error': 'No results found'
                    }
                
                # Get first (best) result
                video_info = info['entries'][0]
                video_title = video_info.get('title', 'Unknown')
                video_duration = video_info.get('duration', 0)
                video_uploader = video_info.get('uploader', 'Unknown')
                
                logger.info(f"Found: {video_title} by {video_uploader}")
                
                # Check duration (limit to 10 minutes to avoid huge files)
                if video_duration and video_duration > 600:  # 10 minutes
                    return {
                        'success': False,
                        'error': 'Song too long (max 10 minutes)'
                    }
                
                # Download the audio
                ydl.download([search_query])
                
                # Find the downloaded file (it will have .mp3 extension after post-processing)
                safe_title = self._sanitize_filename(video_title)
                possible_files = [
                    os.path.join(self.temp_dir, f"{safe_title}.mp3"),
                    os.path.join(self.temp_dir, f"{video_title}.mp3"),
                ]
                
                # Also check for files that might have been created with different naming
                temp_files = [f for f in os.listdir(self.temp_dir) if f.endswith('.mp3')]
                latest_file = None
                
                if temp_files:
                    # Get the most recently created .mp3 file
                    temp_files_with_path = [os.path.join(self.temp_dir, f) for f in temp_files]
                    latest_file = max(temp_files_with_path, key=os.path.getctime)
                
                # Try to find the file
                downloaded_file = None
                for file_path in possible_files:
                    if os.path.exists(file_path):
                        downloaded_file = file_path
                        break
                
                if not downloaded_file and latest_file:
                    downloaded_file = latest_file
                
                if not downloaded_file:
                    return {
                        'success': False,
                        'error': 'Downloaded file not found'
                    }
                
                # Check file size (Telegram limit is 50MB)
                file_size = os.path.getsize(downloaded_file)
                if file_size > 50 * 1024 * 1024:  # 50MB
                    os.remove(downloaded_file)
                    return {
                        'success': False,
                        'error': 'File too large (max 50MB for Telegram)'
                    }
                
                logger.info(f"Successfully downloaded: {downloaded_file} ({file_size/1024/1024:.1f}MB)")
                
                return {
                    'success': True,
                    'file_path': downloaded_file,
                    'title': video_title,
                    'artist': video_uploader,
                    'duration': video_duration,
                    'file_size': file_size
                }
                
        except Exception as e:
            logger.error(f"Sync download error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def _sanitize_filename(self, filename: str) -> str:
        """Remove invalid characters from filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:100]  # Limit length