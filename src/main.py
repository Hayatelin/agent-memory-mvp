"""FastAPI 應用主文件"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.database import Base, engine
from contextlib import asynccontextmanager
from src.api import memories, search, sharing

# 建立數據庫表
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動事件
    print("應用啟動...")
    yield
    # 關閉事件
    print("應用關閉...")


app = FastAPI(
    title="AgentMem API",
    description="Agent Memory System",
    version="0.2.0",
    lifespan=lifespan
)

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(memories.router)
app.include_router(search.router)
app.include_router(sharing.router)


@app.get("/health")
async def health_check():
    """健康檢查"""
    return {"status": "ok", "version": "0.2.0"}


@app.get("/docs")
async def docs():
    """API 文檔"""
    return {"docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
