"""
CLI 配置管理
"""
import os
import json
from pathlib import Path
from typing import Optional


class Config:
    """CLI 配置管理器"""

    CONFIG_DIR = Path.home() / ".agentmem"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self):
        """初始化配置"""
        self.config_dir = self.CONFIG_DIR
        self.config_file = self.CONFIG_FILE
        self._ensure_config_dir()
        self.data = self._load_config()

    def _ensure_config_dir(self) -> None:
        """確保配置目錄存在"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> dict:
        """從文件加載配置"""
        if not self.config_file.exists():
            return self._get_default_config()

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return self._get_default_config()

    def _get_default_config(self) -> dict:
        """獲取默認配置"""
        return {
            "api_url": os.getenv("AGENTMEM_API_URL", "http://localhost:8000"),
            "agent_id": os.getenv("AGENTMEM_AGENT_ID", ""),
            "timeout": int(os.getenv("AGENTMEM_TIMEOUT", "30")),
            "output_format": "table",  # table, json, yaml
        }

    def save(self) -> None:
        """保存配置到文件"""
        self._ensure_config_dir()
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: any = None) -> any:
        """獲取配置值"""
        return self.data.get(key, default)

    def set(self, key: str, value: any) -> None:
        """設置配置值"""
        self.data[key] = value
        self.save()

    def __repr__(self) -> str:
        return f"Config(api_url={self.get('api_url')}, agent_id={self.get('agent_id')})"
