import streamlit as st
import google.generativeai as genai
import time

# 設定您的 Google API Key
# 建議在 .streamlit/secrets.toml 中設定：GOOGLE_API_KEY = "你的金鑰"
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 初始化模型
model = genai.GenerativeModel('gemini-1.5-flash-latest')
prompt = "分析本月業績：本月1000萬，上月800萬，去年同期1200萬"

if "result" not in st.session_state:
    st.session_state.result = ""

if st.button("分析業績"):
    # 建立一個佔位符，顯示載入狀態
    with st.spinner("正在產生分析報告..."):
        for i in range(3):
            try:
                # 呼叫 Gemini API
                response = model.generate_content(prompt)
                
                # Gemini 的回傳內容在 response.text 中
                st.session_state.result = response.text
                break
            except Exception as e:
                if i < 2:
                    time.sleep(2)
                else:
                    st.session_state.result = f"Gemini API 發生錯誤: {e}"

# 顯示結果
st.write(st.session_state.result)
