"""
AgentMem 開始使用頁面
Getting Started - 交互式入門指南，包含 3 個實用示例
"""
import streamlit as st

# 頁面配置
st.set_page_config(
    page_title="開始使用 - AgentMem",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 開始使用 AgentMem")
st.markdown("### 歡迎！以下是 3 個快速示例幫助您開始使用")

# 檢查連接狀態
if "client" not in st.session_state or not st.session_state.client:
    st.warning(
        "⚠️ **尚未連接服務器**\n\n"
        "請返回首頁，在左側邊欄點擊「連接服務器」按鈕進行連接。"
    )
    st.stop()

st.success("✓ 已連接到服務器")
st.divider()

# 使用 Tabs 組織 3 個示例
tab1, tab2, tab3 = st.tabs([
    "💡 示例 1: 存儲想法",
    "🔍 示例 2: 搜索內容",
    "👥 示例 3: 分享記憶"
])


# ============================================================================
# 示例 1: 存儲想法
# ============================================================================
with tab1:
    st.subheader("💡 示例 1: 存儲想法")
    st.markdown("""
    在這個示例中，我們將展示如何快速存儲一個想法或筆記。
    """)

    # 步驟 1-3
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📝 步驟 1: 輸入內容")
        st.info("在下面的文本框中輸入您想要保存的想法或筆記。")

    with col2:
        st.markdown("#### 🏷️ 步驟 2: 選擇分類")
        st.info("選擇合適的類型和分類，便於後續查找和組織。")

    with col3:
        st.markdown("#### ✅ 步驟 3: 保存想法")
        st.info("點擊按鈕保存想法到您的記憶庫。")

    st.divider()

    # 交互式示例
    st.markdown("### 立即試試看")

    col_input, col_type = st.columns([2, 1])

    with col_input:
        example_thought = st.text_area(
            "輸入想法",
            value="我想到了一個改進應用性能的新想法：使用緩存機制來加速搜索...",
            height=80,
            help="輸入您想要保存的想法"
        )

    with col_type:
        memory_type = st.selectbox(
            "記憶類型",
            ["💡 想法", "📚 筆記", "🐛 Bug", "✅ 任務"]
        )

    col_category, col_button = st.columns([1, 1])

    with col_category:
        category = st.selectbox(
            "分類",
            ["技術", "設計", "產品", "其他"]
        )

    with col_button:
        if st.button("✅ 保存想法", use_container_width=True, key="save_thought"):
            try:
                with st.spinner("正在保存..."):
                    client = st.session_state.client

                    # 模擬保存想法
                    result = client.create_memory(
                        content=example_thought,
                        memory_type=memory_type.split()[1] if len(memory_type.split()) > 1 else "idea",
                        tags=[category],
                        metadata={"source": "getting_started"}
                    )

                    st.success(f"✓ 想法已保存！ID: {result.id}")
                    st.balloons()

            except Exception as e:
                st.error(f"✗ 保存失敗: {str(e)}")

    # 提示
    st.markdown("""
    **💡 提示:**
    - 想法可以是任何形式的信息（文字、代碼片段、想法等）
    - 系統會自動為您的想法生成嵌入向量用於語義搜索
    - 您可以隨時編輯或刪除保存的想法
    """)


# ============================================================================
# 示例 2: 搜索內容
# ============================================================================
with tab2:
    st.subheader("🔍 示例 2: 搜索記憶")
    st.markdown("""
    在這個示例中，我們將展示如何使用語義搜索找到相關的記憶。
    """)

    # 步驟 1-2
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔎 步驟 1: 輸入查詢")
        st.info("輸入搜索關鍵詞或問題，系統會使用 AI 理解您的意圖。")

    with col2:
        st.markdown("#### 📊 步驟 2: 查看結果")
        st.info("系統會返回最相關的記憶，按相似度排序。")

    st.divider()

    # 交互式搜索示例
    st.markdown("### 立即試試看")

    col_search, col_threshold = st.columns([2, 1])

    with col_search:
        search_query = st.text_input(
            "搜索查詢",
            value="性能優化技巧",
            placeholder="輸入搜索詞或問題...",
            help="支持自然語言查詢"
        )

    with col_threshold:
        threshold = st.slider(
            "相似度閾值",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="只返回相似度大於此值的結果"
        )

    if st.button("🔍 搜索", use_container_width=True, key="search_btn"):
        try:
            with st.spinner("正在搜索..."):
                client = st.session_state.client

                # 執行搜索
                results = client.search(
                    query=search_query,
                    limit=5,
                    threshold=threshold
                )

                if results:
                    st.success(f"✓ 找到 {len(results)} 條相關記憶")

                    for i, result in enumerate(results, 1):
                        with st.expander(
                            f"📄 結果 {i} - 相似度: {result.similarity:.2%}",
                            expanded=i==1
                        ):
                            st.write(f"**內容:** {result.content}")
                            if hasattr(result, 'metadata') and result.metadata:
                                st.write(f"**標籤:** {', '.join(result.metadata.get('tags', []))}")
                            st.write(f"**創建時間:** {result.created_at}")
                else:
                    st.info("未找到匹配的記憶。請嘗試調整搜索詞或相似度閾值。")

        except Exception as e:
            st.error(f"✗ 搜索失敗: {str(e)}")

    # 提示
    st.markdown("""
    **💡 提示:**
    - 系統使用語義搜索，不僅匹配字面意思
    - 調整相似度閾值可以控制結果的精確度
    - 相似度越高（接近 100%），表示越相關
    """)


# ============================================================================
# 示例 3: 分享記憶
# ============================================================================
with tab3:
    st.subheader("👥 示例 3: 分享記憶")
    st.markdown("""
    在這個示例中，我們將展示如何與其他 Agent 分享您的記憶。
    """)

    # 步驟 1-3
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 1️⃣ 步驟 1: 選擇記憶")
        st.info("選擇您想要分享的記憶。")

    with col2:
        st.markdown("#### 2️⃣ 步驟 2: 指定收件人")
        st.info("輸入目標 Agent 的 ID。")

    with col3:
        st.markdown("#### 3️⃣ 步驟 3: 設置權限")
        st.info("選擇分享級別（只讀、可編輯等）。")

    st.divider()

    # 交互式分享示例
    st.markdown("### 立即試試看")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**選擇記憶 ID**")
        memory_id = st.text_input(
            "Memory ID",
            value="memory_example_001",
            placeholder="例如: memory_12345",
            help="要分享的記憶的 ID"
        )

    with col2:
        st.markdown("**目標 Agent ID**")
        target_agent = st.text_input(
            "Target Agent ID",
            value="agent_recipient_001",
            placeholder="例如: agent_abc123",
            help="接收分享的 Agent 的 ID"
        )

    col1, col2 = st.columns(2)

    with col1:
        permission = st.selectbox(
            "分享權限",
            ["只讀 (Read Only)", "可編輯 (Editable)", "完全訪問 (Full Access)"]
        )

    with col2:
        st.markdown("**過期時間**")
        expiry_days = st.number_input(
            "過期天數",
            min_value=1,
            max_value=365,
            value=30,
            help="分享鏈接在多少天後過期"
        )

    if st.button("👥 分享記憶", use_container_width=True, key="share_btn"):
        try:
            with st.spinner("正在分享..."):
                client = st.session_state.client

                # 模擬分享記憶
                result = client.share_memory(
                    memory_id=memory_id,
                    target_agent_id=target_agent,
                    permission=permission.split()[0].lower(),
                    expiry_days=expiry_days
                )

                st.success("✓ 記憶已成功分享！")

                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**分享 ID:** {result.id}")
                with col2:
                    st.info(f"**過期日期:** {expiry_days} 天後")

                # 顯示分享詳情
                with st.expander("📋 分享詳情", expanded=True):
                    st.write(f"- 記憶 ID: {memory_id}")
                    st.write(f"- 目標 Agent: {target_agent}")
                    st.write(f"- 權限: {permission}")
                    st.write(f"- 過期天數: {expiry_days} 天")

        except Exception as e:
            st.error(f"✗ 分享失敗: {str(e)}")

    # 提示
    st.markdown("""
    **💡 提示:**
    - 只讀模式適合分享知識和參考資料
    - 可編輯模式適合協作項目
    - 完全訪問權限應謹慎使用
    - 您可以隨時撤銷分享的記憶
    """)


# ============================================================================
# 底部：下一步
# ============================================================================
st.divider()
st.markdown("""
## 📚 下一步

完成以上示例後，您可以：

1. **💾 創建記憶** - 進入「創建記憶」頁面，保存更多內容
2. **🔍 搜索記憶** - 進入「搜索記憶」頁面，查找已保存的內容
3. **📋 管理記憶** - 進入「管理記憶」頁面，編輯或刪除記憶
4. **👥 分享記憶** - 進入「共享記憶」頁面，與他人協作

## ❓ 需要幫助？

- 查看側邊欄中的「快速開始」章節
- 閱讀「常見問題」了解常見問題
- 訪問 [GitHub 倉庫](https://github.com/Hayatelin/agent-memory-mvp) 查看完整文檔

祝您使用愉快！🎉
""")
