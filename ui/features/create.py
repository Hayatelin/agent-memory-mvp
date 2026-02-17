"""
創建記憶頁面
"""
import streamlit as st
from src.client import AgentMemClient


def render():
    """渲染創建記憶頁面"""
    st.header("創建新記憶")
    
    # 獲取客戶端
    client = st.session_state.get("client")
    if not client:
        st.error("未連接到服務器。請先在設置中配置。")
        return
    
    # 創建表單
    with st.form("create_memory_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            memory_type = st.selectbox(
                "記憶類型",
                ["knowledge", "note", "experience", "idea"],
                help="選擇記憶的類型"
            )
            category = st.text_input(
                "分類",
                value="general",
                help="為記憶分配一個分類"
            )
        
        with col2:
            visibility = st.selectbox(
                "可見性",
                ["private", "shared", "public"],
                help="選擇誰可以看到這條記憶"
            )
        
        # 內容輸入
        content = st.text_area(
            "記憶內容",
            placeholder="在這裡輸入要保存的內容...",
            height=200,
            help="輸入您要保存的記憶內容"
        )
        
        # 提交按鈕
        submitted = st.form_submit_button("創建記憶", use_container_width=True)
        
        if submitted:
            if not content.strip():
                st.error("請輸入記憶內容")
                return
            
            try:
                with st.spinner("正在創建記憶..."):
                    memory = client.create_memory(
                        content=content,
                        type=memory_type,
                        category=category,
                        visibility=visibility
                    )
                
                st.success(f"✓ 記憶已創建！")
                st.info(f"記憶 ID: {memory.id}")

                # Part 3: 清除緩存後重新加載
                st.cache_data.clear()
                st.balloons()

                # 顯示記憶詳情
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("類型", memory.type)
                with col2:
                    st.metric("分類", memory.category)
                with col3:
                    st.metric("可見性", memory.visibility)

                st.json({
                    "id": memory.id,
                    "content": memory.content[:100] + "..." if len(memory.content) > 100 else memory.content,
                    "created_at": str(memory.created_at)
                })

            except Exception as e:
                st.error(f"創建失敗: {str(e)}")
