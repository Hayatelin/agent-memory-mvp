"""
共享記憶頁面
"""
import streamlit as st
from src.client import AgentMemClient


def render():
    """渲染共享記憶頁面"""
    st.header("共享記憶")

    client = st.session_state.get("client")
    if not client:
        st.error("未連接到服務器。請先在設置中配置。")
        return

    # 標籤頁選擇
    tab1, tab2 = st.tabs(["共享記憶", "管理共享"])

    # 標籤頁 1：共享記憶
    with tab1:
        st.subheader("與其他 Agent 共享記憶")

        col1, col2 = st.columns([2, 1])
        with col1:
            memory_id = st.text_input(
                "記憶 ID",
                placeholder="輸入要共享的記憶 ID...",
                key="share_memory_id"
            )
        with col2:
            st.write("")  # 空間調整

        agent_id = st.text_input(
            "Agent ID",
            placeholder="輸入目標 Agent ID...",
            key="share_agent_id"
        )

        if st.button("共享", use_container_width=True, key="share_btn"):
            if not memory_id.strip():
                st.error("請輸入記憶 ID")
            elif not agent_id.strip():
                st.error("請輸入 Agent ID")
            else:
                try:
                    # 先驗證記憶是否存在
                    with st.spinner("正在驗證記憶..."):
                        memory = client.get_memory(memory_id)

                    st.info(f"記憶: {memory.content[:100]}...")

                    # 共享
                    with st.spinner("正在共享..."):
                        client.share_memory(memory_id, agent_id)

                    st.success(f"✓ 記憶已與 Agent {agent_id[:8]}... 共享！")

                    # 顯示共享列表
                    with st.spinner("正在獲取共享列表..."):
                        shared_with = client.get_shared_with(memory_id)

                    st.write("**此記憶已共享給以下 Agents:**")
                    for agent in shared_with:
                        st.text(f"• {agent}")

                except Exception as e:
                    st.error(f"共享失敗: {str(e)}")

        # 顯示提示
        with st.expander("需要幫助？"):
            st.write("""
            **如何共享記憶:**

            1. 輸入要共享的記憶 ID（可以在「管理記憶」頁面找到）
            2. 輸入目標 Agent 的 ID
            3. 點擊「共享」按鈕

            **什麼是 Agent ID?**

            Agent ID 是每個 Agent 的唯一標識符（UUID 格式）。
            您可以在應用設置中看到您自己的 Agent ID。
            """)

    # 標籤頁 2：管理共享
    with tab2:
        st.subheader("管理共享權限")

        memory_id = st.text_input(
            "記憶 ID",
            placeholder="輸入要管理的記憶 ID...",
            key="manage_share_id"
        )

        if memory_id:
            try:
                # 獲取記憶資訊
                with st.spinner("正在載入記憶..."):
                    memory = client.get_memory(memory_id)

                st.info(f"記憶: {memory.content[:100]}...")

                # 獲取共享列表
                with st.spinner("正在載入共享列表..."):
                    shared_with = client.get_shared_with(memory_id)

                if shared_with:
                    st.write(f"**此記憶已共享給 {len(shared_with)} 個 Agent:**")

                    for agent_id in shared_with:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.text(f"• {agent_id}")
                        with col2:
                            if st.button(
                                "撤銷",
                                key=f"revoke_{agent_id}",
                                use_container_width=True
                            ):
                                try:
                                    with st.spinner("正在撤銷共享..."):
                                        client.revoke_sharing(memory_id, agent_id)

                                    st.success(f"✓ 已撤銷與 {agent_id[:8]}... 的共享")
                                    st.rerun()

                                except Exception as e:
                                    st.error(f"撤銷失敗: {str(e)}")

                else:
                    st.info("此記憶還沒有與任何 Agent 共享")

            except Exception as e:
                st.error(f"載入失敗: {str(e)}")
