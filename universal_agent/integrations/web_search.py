import asyncio
import aiohttp
from typing import List, Dict, Any

class WebSearch:
    def __init__(self):
        self.search_api_key = None  # Will use DuckDuckGo (no API key needed)
        
    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search the web using DuckDuckGo"""
        try:
            # Use DuckDuckGo HTML search (no API key required)
            url = f"https://html.duckduckgo.com/html/?q={query}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
                    if response.status == 200:
                        html = await response.text()
                        # Simple parsing for demo - in production use BeautifulSoup
                        results = []
                        # Extract basic info (simplified)
                        results.append({
                            "title": f"Search results for: {query}",
                            "snippet": "Found multiple results",
                            "url": url
                        })
                        return results
                    else:
                        return [{"error": f"Search failed with status {response.status}"}]
        except Exception as e:
            print(f"[WEB SEARCH] Error: {e}")
            return [{"error": str(e)}]
    
    async def get_page_content(self, url: str) -> str:
        """Fetch content from a URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        return f"Error: Status {response.status}"
        except Exception as e:
            return f"Error: {e}"
