"""
搜索記憶頁面
"""
import streamlit as st
from src.client import AgentMemClient


def render():
    """渲染搜索頁面"""
    st.header("搜索記憶")
    
    client = st.session_state.get("client")
    if not client:
        st.error("未連接到服務器。請先在設置中配置。")
        return
    
    # 搜索控件
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        query = st.text_input(
            "搜索查詢",
            placeholder="輸入搜索關鍵詞...",
            key="search_query"
        )
    
    with col2:
        limit = st.number_input("結果數量", value=10, min_value=1, max_value=100)
    
    with col3:
        threshold = st.slider("相似度閾值", 0.0, 1.0, 0.3, 0.1)
    
    # 搜索按鈕
    if st.button("搜索", use_container_width=True, key="search_btn"):
        if not query.strip():
            st.warning("請輸入搜索關鍵詞")
            return
        
        try:
            with st.spinner("正在搜索..."):
                results = client.search(
                    query=query,
                    limit=limit,
                    similarity_threshold=threshold
                )
            
            # 顯示結果統計
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("找到結果", len(results.results))
            with col2:
                st.metric("查詢時間", f"{results.query_embedding_time_ms}ms")
            with col3:
                st.metric("搜索時間", f"{results.search_time_ms}ms")
            
            # 顯示搜索結果
            if results.results:
                st.subheader(f"搜索結果 ({len(results.results)} 條)")
                
                for i, result in enumerate(results.results, 1):
                    with st.expander(
                        f"{i}. [{result.similarity_score:.1%}] {result.content[:60]}...",
                        expanded=(i == 1)
                    ):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("相似度", f"{result.similarity_score:.1%}")
                        with col2:
                            st.metric("類型", result.type)
                        with col3:
                            st.metric("分類", result.category)
                        
                        st.write("**內容:**")
                        st.write(result.content)
                        
                        st.write("**ID:**")
                        st.code(result.memory_id)
            else:
                st.info("未找到相關記憶")
        
        except Exception as e:
            st.error(f"搜索失敗: {str(e)}")
    
    # 顯示搜索統計
    st.divider()
    if st.checkbox("顯示搜索統計"):
        try:
            with st.spinner("正在獲取統計..."):
                stats = client.get_search_stats()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("總記憶數", stats.total_memories)
            with col2:
                st.metric("可搜索記憶", stats.searchable_memories)
            with col3:
                st.metric("覆蓋率", f"{stats.embedding_coverage:.1%}")
        
        except Exception as e:
            st.error(f"獲取統計失敗: {str(e)}")
