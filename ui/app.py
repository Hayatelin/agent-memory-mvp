"""
AgentMem Web UI 主應用程式
使用 Streamlit 構建的交互式記憶管理介面
"""
import streamlit as st
import uuid
from src.client import AgentMemClient
from ui.features import create, search, manage, share


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
                client = AgentMemClient(
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
            stats = st.session_state.client.get_search_stats()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("總記憶數", stats.total_memories)
            with col2:
                st.metric("覆蓋率", f"{stats.embedding_coverage:.1%}")
        except:
            pass
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
    # 導航菜單
    st.subheader("導航")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nav_create = st.button("➕ 創建記憶", use_container_width=True, key="nav_create")
    with col2:
        nav_search = st.button("🔍 搜索記憶", use_container_width=True, key="nav_search")
    with col3:
        nav_manage = st.button("📋 管理記憶", use_container_width=True, key="nav_manage")
    with col4:
        nav_share = st.button("👥 共享記憶", use_container_width=True, key="nav_share")

    st.divider()

    # 根據選擇渲染頁面
    if "current_page" not in st.session_state:
        st.session_state.current_page = "create"

    if nav_create:
        st.session_state.current_page = "create"
    elif nav_search:
        st.session_state.current_page = "search"
    elif nav_manage:
        st.session_state.current_page = "manage"
    elif nav_share:
        st.session_state.current_page = "share"

    # 渲染選定的頁面
    if st.session_state.current_page == "create":
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
