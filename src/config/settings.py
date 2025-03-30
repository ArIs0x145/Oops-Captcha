from pathlib import Path
import yaml
from typing import Dict, Any
from functools import lru_cache

class Settings:
    
    def __init__(self, config_path: str = "configs/default.yaml"):
        self._config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self._config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{self._config_path}' not found")
    
    def get_captcha_config(self, type_: str) -> Dict[str, Any]:
        return self._config.get('captcha', {}).get(type_, {})

@lru_cache # Get Instance
def get_settings() -> Settings:
    return Settings()