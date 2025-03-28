"""
Application metadata management.
"""
import json
from pathlib import Path
from typing import Dict, Any

class MetadataManager:
    """
    Manages application metadata from a central JSON file.
    """
    def __init__(self):
        self._metadata: Dict[str, Any] = {}
        self._load_metadata()
    
    def _load_metadata(self) -> None:
        """Load metadata from JSON file."""
        try:
            metadata_path = Path(__file__).parent.parent.parent / "docs" / "metadata.json"
            with open(metadata_path, "r") as f:
                self._metadata = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load metadata: {e}")
            self._metadata = {}
    
    @property
    def version(self) -> str:
        """Get application version."""
        return self._metadata.get("version", "0.1.0")
    
    @property
    def api_version(self) -> str:
        """Get API version."""
        return self._metadata.get("api", {}).get("version", "0.1.0")
    
    @property
    def name(self) -> str:
        """Get application name."""
        return self._metadata.get("name", "NoteKo")
    
    @property
    def author(self) -> Dict[str, str]:
        """Get author information."""
        return self._metadata.get("author", {})
    
    @property
    def environment(self) -> Dict[str, str]:
        """Get environment information."""
        return self._metadata.get("environment", {})
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get any metadata value by key."""
        return self._metadata.get(key, default)

# Global instance
metadata = MetadataManager()
