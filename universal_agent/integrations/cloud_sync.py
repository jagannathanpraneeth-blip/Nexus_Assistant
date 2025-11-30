import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any
import aiohttp

class CloudSync:
    def __init__(self, sync_url: str = None):
        self.sync_url = sync_url or os.getenv("CLOUD_SYNC_URL")
        self.enabled = bool(self.sync_url)
        
    async def upload_knowledge(self, knowledge_data: Dict[str, Any]) -> bool:
        """Upload knowledge graph to cloud"""
        if not self.enabled:
            print("[CLOUD SYNC] Not configured. Set CLOUD_SYNC_URL in .env")
            return False
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.sync_url}/upload",
                    json={
                        "timestamp": datetime.now().isoformat(),
                        "data": knowledge_data
                    }
                ) as response:
                    return response.status == 200
        except Exception as e:
            print(f"[CLOUD SYNC] Upload failed: {e}")
            return False
    
    async def download_knowledge(self) -> Dict[str, Any]:
        """Download knowledge graph from cloud"""
        if not self.enabled:
            return {}
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.sync_url}/download") as response:
                    if response.status == 200:
                        return await response.json()
                    return {}
        except Exception as e:
            print(f"[CLOUD SYNC] Download failed: {e}")
            return {}
    
    async def sync(self, local_data: Dict[str, Any]) -> Dict[str, Any]:
        """Bidirectional sync - merge local and cloud data"""
        if not self.enabled:
            return local_data
            
        cloud_data = await self.download_knowledge()
        # Simple merge strategy - cloud takes precedence for conflicts
        merged = {**local_data, **cloud_data}
        await self.upload_knowledge(merged)
        return merged
