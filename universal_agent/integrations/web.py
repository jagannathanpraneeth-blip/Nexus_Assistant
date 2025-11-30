import asyncio

class WebIntegration:
    async def fetch_page(self, url: str) -> str:
        # Mock implementation to avoid external dependencies for MVP
        await asyncio.sleep(1)
        return f"<html><body>Mock content for {url}</body></html>"

    async def summarize_url(self, url: str) -> str:
        content = await self.fetch_page(url)
        return f"Summary of {url}: {content[:50]}..."
