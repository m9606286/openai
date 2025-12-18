import streamlit as st
import google.generativeai as genai
import time

# 設定金鑰
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel('models/gemini-1.5-flash')

prompt = "分析本月業績：本月1000萬，上月800萬，去年同期1200萬"

if "result" not in st.session_state:
    st.session_state.result = ""

if st.button("分析業績"):
    with st.spinner(f"分析中..."):
        for i in range(3):
            try:
                response = model.generate_content(prompt)
                st.session_state.result = response.text
                break
            except Exception as e:
                if i < 2:
                    time.sleep(2)
                else:
                    st.session_state.result = f"錯誤: {e}"

st.write(st.session_state.result)
