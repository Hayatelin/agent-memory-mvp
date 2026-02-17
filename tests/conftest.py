"""Pytest 配置和 fixtures"""

import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """為異步測試創建事件循環"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
