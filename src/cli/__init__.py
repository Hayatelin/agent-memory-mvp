"""
AgentMem CLI - 命令行工具

使用示例:
    agentmem --help
    agentmem create "記憶內容"
    agentmem search "查詢"
    agentmem list
"""
from .main import cli, main

__all__ = ["cli", "main"]
