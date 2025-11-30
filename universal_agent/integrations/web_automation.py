import asyncio
import webbrowser
from typing import Tuple
import pyautogui
import time

class WebAutomation:
    async def open_url(self, url: str):
        """Open a URL in the default browser"""
        try:
            webbrowser.open(url)
            await asyncio.sleep(2)  # Wait for browser to open
            return f"Opened {url}"
        except Exception as e:
            return f"Failed to open URL: {e}"
    
    async def search_and_play(self, query: str):
        """Search YouTube and play first result"""
        try:
            import aiohttp
            import re
            
            # Search YouTube and get the HTML
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        # Extract first video ID from the HTML
                        # YouTube video IDs are in format: "videoId":"XXXXXXXXXXX"
                        match = re.search(r'"videoId":"([^"]+)"', html)
                        
                        if match:
                            video_id = match.group(1)
                            video_url = f"https://www.youtube.com/watch?v={video_id}"
                            
                            # Open the video directly
                            webbrowser.open(video_url)
                            await asyncio.sleep(2)
                            
                            return f"Playing: {query}"
                        else:
                            # Fallback to old method if scraping fails
                            webbrowser.open(search_url)
                            await asyncio.sleep(4)
                            
                            def click_first_video():
                                time.sleep(1)
                                for _ in range(8):
                                    pyautogui.press('tab')
                                    time.sleep(0.1)
                                pyautogui.press('enter')
                            
                            await asyncio.to_thread(click_first_video)
                            return f"Playing: {query}"
                    else:
                        return f"Failed to search YouTube: Status {response.status}"
                        
        except Exception as e:
            return f"Failed to play video: {e}"


