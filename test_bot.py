#!/usr/bin/env python3
"""
Test script to demonstrate the Telegram Music Bot functionality
"""

import os
import asyncio
from downloader import MusicDownloader

async def test_music_bot():
    """Test the music download functionality"""
    print("🎵 Testing Telegram Music Bot Functionality 🎵\n")
    
    downloader = MusicDownloader()
    
    # Test queries
    test_queries = [
        "happy birthday",
        "twinkle twinkle little star",
        "jingle bells"
    ]
    
    for query in test_queries:
        print(f"🔍 Testing search for: '{query}'")
        result = await downloader.download_music(query)
        
        if result['success']:
            print(f"✅ SUCCESS: Downloaded '{result['title']}'")
            print(f"   📁 File: {result['file_path']}")
            print(f"   📏 Size: {result['file_size']/1024/1024:.1f} MB")
            print(f"   ⏱️  Duration: {result['duration']} seconds")
            
            # Clean up
            try:
                os.remove(result['file_path'])
                print(f"   🗑️  Cleaned up file")
            except:
                pass
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_music_bot())