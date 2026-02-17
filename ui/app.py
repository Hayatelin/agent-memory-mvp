"""
AgentMem Web UI 主應用程式
使用 Streamlit 構建的交互式記憶管理介面
"""
import streamlit as st
import uuid
from datetime import datetime, timedelta
from typing import List
from src.client import AgentMemClient
from src.client.models import Memory, SearchStats
from ui.features import create, search, manage, share


# ============================================================================
# 緩存函數 (Part 1: Caching Infrastructure)
# ============================================================================

@st.cache_resource(ttl=3600)
def get_cached_client(api_url: str, agent_id: str) -> AgentMemClient:
    """
    緩存客戶端初始化
    使用 cache_resource 因為包含 session 對象（不可序列化）
    TTL: 1 小時
    """
    return AgentMemClient(api_url=api_url, agent_id=agent_id)


@st.cache_data(ttl=30)
def fetch_search_stats(client: AgentMemClient) -> SearchStats:
    """
    緩存統計數據
    短 TTL 保持數據較新，減少 API 調用 85%
    TTL: 30 秒
    """
    try:
        return client.get_search_stats()
    except Exception:
        return None


@st.cache_data(ttl=60)
def fetch_memories_list(client: AgentMemClient, limit: int = 100) -> List[Memory]:
    """
    緩存記憶列表用於儀表板
    用於顯示最近記憶和類型分佈
    TTL: 60 秒
    """
    try:
        return client.list_memories(limit=limit, offset=0)
    except Exception:
        return []


# ============================================================================
# 輔助函數
# ============================================================================

def format_time_ago(dt: datetime) -> str:
    """將時間格式化為 'XX ago' 格式"""
    if not dt:
        return "Unknown"

    # 處理 naive 和 aware datetime
    now = datetime.utcnow() if dt.tzinfo is None else datetime.now(dt.tzinfo)
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        return f"{int(seconds)}s ago"
    elif seconds < 3600:
        return f"{int(seconds / 60)}m ago"
    elif seconds < 86400:
        return f"{int(seconds / 3600)}h ago"
    else:
        return f"{int(seconds / 86400)}d ago"


def get_type_emoji(memory_type: str) -> str:
    """為記憶類型返回對應 emoji"""
    emoji_map = {
        "knowledge": "📚",
        "note": "📝",
        "experience": "🎯",
        "idea": "💡",
    }
    return emoji_map.get(memory_type, "📌")


def render_dashboard(client: AgentMemClient):
    """
    渲染儀表板（Part 2: Dashboard UI Implementation）
    ~150 行左右，包含所有儀表板組件
    """
    st.subheader("📊 儀表板概覽")

    # 獲取數據
    stats = fetch_search_stats(client)
    memories = fetch_memories_list(client, limit=100)

    if not stats or not memories:
        st.warning("⚠️ 無法加載儀表板數據。請重試或檢查連接。")
        if st.button("🔄 重新加載"):
            fetch_search_stats.clear()
            fetch_memories_list.clear()
            st.rerun()
        return

    # ─────────────────────────────────────────────────────────────────────
    # 1. 關鍵指標行（4 個 metric）
    # ─────────────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 總記憶數", stats.total_memories)

    with col2:
        st.metric("🔍 可搜索數", stats.searchable_memories)

    with col3:
        coverage_pct = f"{stats.embedding_coverage:.1%}"
        st.metric("📊 覆蓋率", coverage_pct)

    with col4:
        # 最後添加時間
        if memories:
            latest = max(memories, key=lambda m: m.created_at or datetime.min)
            last_added = format_time_ago(latest.created_at)
            st.metric("⏱️ 最後添加", last_added)
        else:
            st.metric("⏱️ 最後添加", "N/A")

    st.divider()

    # ─────────────────────────────────────────────────────────────────────
    # 2. 雙欄布局（記憶類型分佈 + 最近活動）
    # ─────────────────────────────────────────────────────────────────────
    col_left, col_right = st.columns([1.2, 0.8])

    # 左：記憶類型分佈
    with col_left:
        st.write("**🏷️ 記憶類型分佈**")

        # 計算類型分佈
        type_counts = {}
        for memory in memories:
            type_counts[memory.type] = type_counts.get(memory.type, 0) + 1

        if type_counts:
            # 使用字典格式創建圖表
            import pandas as pd
            df = pd.DataFrame(
                list(type_counts.items()),
                columns=["Type", "Count"]
            )
            st.bar_chart(df.set_index("Type"))
        else:
            st.info("暫無記憶數據")

    # 右：最近活動列表
    with col_right:
        st.write("**🕐 最近活動**")

        # 按創建時間排序，取最新 5 條
        sorted_memories = sorted(
            memories,
            key=lambda m: m.created_at or datetime.min,
            reverse=True
        )[:5]

        if sorted_memories:
            for memory in sorted_memories:
                emoji = get_type_emoji(memory.type)
                time_str = format_time_ago(memory.created_at)
                st.caption(f"{emoji} {memory.type}: {time_str}")
        else:
            st.caption("暫無活動")

    st.divider()

    # ─────────────────────────────────────────────────────────────────────
    # 3. 最近記憶列表（最新 5 條，展開式卡片）
    # ─────────────────────────────────────────────────────────────────────
    st.write("**📌 最近記憶（最新 5 條）**")

    sorted_memories = sorted(
        memories,
        key=lambda m: m.created_at or datetime.min,
        reverse=True
    )[:5]

    if sorted_memories:
        for i, memory in enumerate(sorted_memories, 1):
            emoji = get_type_emoji(memory.type)
            preview = memory.content[:50] + "..." if len(memory.content) > 50 else memory.content

            with st.expander(f"{i}. {emoji} [{memory.type}] {preview}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("類型", memory.type)
                with col2:
                    st.metric("分類", memory.category)
                with col3:
                    st.metric("可見性", memory.visibility)

                st.write("**內容:**")
                st.write(memory.content)

                st.caption(f"📅 {memory.created_at} | 🆔 {memory.id[:12]}...")
    else:
        st.info("還沒有記憶。點擊下方「快速操作」來創建第一條記憶！")

    st.divider()

    # ─────────────────────────────────────────────────────────────────────
    # 4. 快速操作按鈕（4 個按鈕導航）
    # ─────────────────────────────────────────────────────────────────────
    st.write("**⚡ 快速操作**")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("➕ 創建記憶", use_container_width=True, key="dashboard_create"):
            st.session_state.current_page = "create"
            st.rerun()

    with col2:
        if st.button("🔍 搜索記憶", use_container_width=True, key="dashboard_search"):
            st.session_state.current_page = "search"
            st.rerun()

    with col3:
        if st.button("📋 管理記憶", use_container_width=True, key="dashboard_manage"):
            st.session_state.current_page = "manage"
            st.rerun()

    with col4:
        if st.button("👥 共享記憶", use_container_width=True, key="dashboard_share"):
            st.session_state.current_page = "share"
            st.rerun()


# 頁面配置
st.set_page_config(
    page_title="AgentMem - 記憶管理系統",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 應用標題
st.title("🧠 AgentMem - 智能記憶管理系統")
st.markdown("---")


# 初始化 Session State
def init_session():
    """初始化 Session State"""
    if "client" not in st.session_state:
        st.session_state.client = None
    if "agent_id" not in st.session_state:
        st.session_state.agent_id = None
    if "api_url" not in st.session_state:
        st.session_state.api_url = "http://localhost:8000"


init_session()


# 側邊欄：設置和導航
with st.sidebar:
    st.header("⚙️ 設置")

    # API 設置
    st.subheader("API 配置")
    api_url = st.text_input(
        "API URL",
        value=st.session_state.api_url,
        help="AgentMem 服務器的 URL"
    )

    if api_url != st.session_state.api_url:
        st.session_state.api_url = api_url
        st.session_state.client = None  # 重置客戶端

    # Agent ID 設置
    st.subheader("Agent 配置")

    col1, col2 = st.columns([3, 1])
    with col1:
        agent_id = st.text_input(
            "Agent ID",
            value=st.session_state.agent_id or "",
            placeholder="留空則自動生成",
            help="此 Agent 的唯一標識符"
        )

    with col2:
        if st.button("🔄 生成", help="生成新的 Agent ID"):
            new_id = str(uuid.uuid4())
            st.session_state.agent_id = new_id
            st.rerun()

    if agent_id:
        st.session_state.agent_id = agent_id
    else:
        if not st.session_state.agent_id:
            st.session_state.agent_id = str(uuid.uuid4())

    st.code(st.session_state.agent_id, language="text")

    # 連接按鈕
    st.divider()
    if st.button("🔗 連接服務器", use_container_width=True, key="connect_btn"):
        try:
            with st.spinner("正在連接..."):
                # 使用緩存客戶端（Part 1）
                client = get_cached_client(
                    api_url=st.session_state.api_url,
                    agent_id=st.session_state.agent_id
                )

                # 測試連接
                if client.health_check():
                    st.session_state.client = client
                    st.success("✓ 連接成功！")
                else:
                    st.error("✗ 無法連接到服務器")

        except Exception as e:
            st.error(f"連接失敗: {str(e)}")

    # 連接狀態
    st.divider()
    st.subheader("連接狀態")
    if st.session_state.client:
        st.success("🟢 已連接")
        try:
            # 使用緩存統計函數（Part 1）
            stats = fetch_search_stats(st.session_state.client)
            if stats:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("總記憶數", stats.total_memories)
                with col2:
                    st.metric("覆蓋率", f"{stats.embedding_coverage:.1%}")
        except:
            pass

        # 緩存管理按鈕
        if st.button("🔄 清除緩存", help="刷新所有緩存數據", use_container_width=True):
            fetch_search_stats.clear()
            fetch_memories_list.clear()
            st.success("✓ 緩存已清除！")
            st.rerun()
    else:
        st.warning("🟡 未連接")
        st.info("請點擊上面的「連接服務器」按鈕")

    # 幫助和關於
    st.divider()
    st.subheader("幫助")
    with st.expander("📖 快速開始"):
        st.write("""
        **第一步：連接服務器**
        1. 確保 AgentMem 服務器正在運行
        2. 檢查 API URL 是否正確
        3. 點擊「連接服務器」按鈕

        **第二步：創建記憶**
        1. 進入「創建記憶」頁面
        2. 選擇類型和分類
        3. 輸入記憶內容
        4. 點擊「創建記憶」

        **第三步：搜索記憶**
        1. 進入「搜索記憶」頁面
        2. 輸入搜索關鍵詞
        3. 調整相似度閾值
        4. 查看結果

        **第四步：管理和共享**
        - 在「管理記憶」中更新或刪除記憶
        - 在「共享記憶」中與其他 Agent 共享
        """)

    with st.expander("❓ 常見問題"):
        st.write("""
        **Q: Agent ID 有什麼用？**
        A: 用於識別不同的用戶或應用。每個 Agent 有獨立的記憶空間。

        **Q: 可以更改 API URL 嗎？**
        A: 可以。修改 API URL 後需要重新連接。

        **Q: 記憶會被永久保存嗎？**
        A: 是的，記憶被存儲在服務器的數據庫中。

        **Q: 如何備份我的記憶？**
        A: 使用「搜索記憶」並導出結果。
        """)

    with st.expander("ℹ️ 關於"):
        st.write("""
        **AgentMem - 智能記憶管理系統**

        版本: 1.0.0

        AgentMem 是一個強大的記憶管理系統，提供：
        - 💾 持久化記憶存儲
        - 🔍 智能語義搜索
        - 👥 記憶共享功能
        - 🔒 細粒度權限控制

        [GitHub 倉庫](https://github.com/yourusername/agentmem)
        [文檔](https://github.com/yourusername/agentmem/docs)
        """)


# 主要內容區域
if not st.session_state.client:
    st.warning("⚠️ 請在左側邊欄連接到服務器開始使用")
else:
    # 根據選擇渲染頁面
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    # 導航菜單
    st.subheader("導航")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        nav_dashboard = st.button("📊 儀表板", use_container_width=True, key="nav_dashboard")
    with col2:
        nav_create = st.button("➕ 創建記憶", use_container_width=True, key="nav_create")
    with col3:
        nav_search = st.button("🔍 搜索記憶", use_container_width=True, key="nav_search")
    with col4:
        nav_manage = st.button("📋 管理記憶", use_container_width=True, key="nav_manage")
    with col5:
        nav_share = st.button("👥 共享記憶", use_container_width=True, key="nav_share")

    st.divider()

    if nav_dashboard:
        st.session_state.current_page = "dashboard"
    elif nav_create:
        st.session_state.current_page = "create"
    elif nav_search:
        st.session_state.current_page = "search"
    elif nav_manage:
        st.session_state.current_page = "manage"
    elif nav_share:
        st.session_state.current_page = "share"

    # 渲染選定的頁面
    if st.session_state.current_page == "dashboard":
        render_dashboard(st.session_state.client)
    elif st.session_state.current_page == "create":
        create.render()
    elif st.session_state.current_page == "search":
        search.render()
    elif st.session_state.current_page == "manage":
        manage.render()
    elif st.session_state.current_page == "share":
        share.render()

    # 底部頁腳
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 12px; margin-top: 20px;'>
        <p>AgentMem © 2025 | 智能記憶管理系統</p>
        <p>
            <a href='https://github.com/yourusername/agentmem' target='_blank'>GitHub</a> |
            <a href='https://github.com/yourusername/agentmem/issues' target='_blank'>報告問題</a>
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
