"""
管理記憶頁面
"""
import streamlit as st
from src.client import AgentMemClient


def render():
    """渲染管理記憶頁面"""
    st.header("管理記憶")

    client = st.session_state.get("client")
    if not client:
        st.error("未連接到服務器。請先在設置中配置。")
        return

    # 標籤頁選擇
    tab1, tab2, tab3 = st.tabs(["查看記憶", "更新記憶", "刪除記憶"])

    # 標籤頁 1：查看記憶
    with tab1:
        st.subheader("所有記憶")

        col1, col2 = st.columns([3, 1])
        with col1:
            limit = st.number_input("顯示數量", value=20, min_value=1, max_value=100, key="list_limit")
        with col2:
            if st.button("刷新", use_container_width=True, key="refresh_btn"):
                st.rerun()

        try:
            with st.spinner("正在載入記憶..."):
                memories = client.list_memories(limit=limit)

            if memories:
                st.info(f"共找到 {len(memories)} 條記憶")

                for i, memory in enumerate(memories, 1):
                    with st.expander(
                        f"{i}. [{memory.type}] {memory.content[:60]}...",
                        expanded=False
                    ):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("類型", memory.type)
                        with col2:
                            st.metric("分類", memory.category)
                        with col3:
                            st.metric("可見性", memory.visibility)
                        with col4:
                            # Bug Fix: Use created_by_agent_id instead of agent_id
                            agent_display = (memory.created_by_agent_id[:8] + "...") if memory.created_by_agent_id else "N/A"
                            st.metric("Agent ID", agent_display)

                        st.write("**完整內容:**")
                        st.write(memory.content)

                        st.write("**ID:**")
                        st.code(memory.id)

                        st.write("**建立時間:**")
                        st.text(str(memory.created_at))
            else:
                st.info("還沒有建立任何記憶")

        except Exception as e:
            st.error(f"載入記憶失敗: {str(e)}")

    # 標籤頁 2：更新記憶
    with tab2:
        st.subheader("更新記憶")

        memory_id = st.text_input(
            "記憶 ID",
            placeholder="輸入要更新的記憶 ID...",
            key="update_id"
        )

        if memory_id:
            try:
                # 先獲取現有記憶
                with st.spinner("正在載入記憶..."):
                    memory = client.get_memory(memory_id)

                st.info(f"找到記憶: {memory.content[:100]}...")

                # 更新表單
                with st.form("update_memory_form"):
                    new_content = st.text_area(
                        "新內容",
                        value=memory.content,
                        height=200
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        new_type = st.selectbox(
                            "新類型",
                            ["knowledge", "note", "experience", "idea"],
                            index=["knowledge", "note", "experience", "idea"].index(memory.type)
                        )
                    with col2:
                        new_category = st.text_input(
                            "新分類",
                            value=memory.category
                        )

                    submitted = st.form_submit_button("更新記憶", use_container_width=True)

                    if submitted:
                        try:
                            with st.spinner("正在更新..."):
                                updated = client.update_memory(
                                    memory_id,
                                    content=new_content,
                                    type=new_type,
                                    category=new_category
                                )

                            st.success("✓ 記憶已更新！")
                            # Part 3: 清除緩存
                            st.cache_data.clear()
                            st.json({
                                "id": updated.id,
                                "type": updated.type,
                                "category": updated.category
                            })

                        except Exception as e:
                            st.error(f"更新失敗: {str(e)}")

            except Exception as e:
                st.error(f"載入記憶失敗: {str(e)}")

    # 標籤頁 3：刪除記憶
    with tab3:
        st.subheader("刪除記憶")

        delete_id = st.text_input(
            "記憶 ID",
            placeholder="輸入要刪除的記憶 ID...",
            key="delete_id"
        )

        if delete_id:
            try:
                # 先顯示要刪除的記憶
                with st.spinner("正在載入記憶..."):
                    memory = client.get_memory(delete_id)

                st.warning(f"您即將刪除: {memory.content[:100]}...")

                # 確認刪除
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("確認刪除", use_container_width=True, key="confirm_delete"):
                        try:
                            with st.spinner("正在刪除..."):
                                client.delete_memory(delete_id)

                            st.success("✓ 記憶已刪除！")
                            # Part 3: 清除緩存
                            st.cache_data.clear()
                            st.balloons()

                        except Exception as e:
                            st.error(f"刪除失敗: {str(e)}")

                with col2:
                    st.button("取消", use_container_width=True, disabled=True)

            except Exception as e:
                st.error(f"載入記憶失敗: {str(e)}")
