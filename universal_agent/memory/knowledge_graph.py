import json
import os
from typing import Dict, Any, List

class KnowledgeGraph:
    def __init__(self, storage_path: str = "knowledge.json"):
        self.storage_path = storage_path
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_node(self, node_id: str, properties: Dict[str, Any]):
        self.data[node_id] = properties
        self.save()

    def get_node(self, node_id: str) -> Dict[str, Any]:
        return self.data.get(node_id, {})

    def search(self, query: str) -> List[Dict[str, Any]]:
        # Simple keyword search
        results = []
        for key, value in self.data.items():
            if query.lower() in str(value).lower():
                results.append({"id": key, "data": value})
        return results
