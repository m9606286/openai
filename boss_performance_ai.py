import streamlit as st
import openai
import time

# 從 Streamlit Secrets 拿 API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

prompt = "分析本月業績：本月1000萬，上月800萬，去年同期1200萬"

if "result" not in st.session_state:
    st.session_state.result = ""

if st.button("分析業績"):
    for i in range(3):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.result = response.choices[0].message["content"]
            break
        except Exception as e:  # ✅ 最通用方式，捕捉所有錯誤
            if i < 2:
                time.sleep(2)
            else:
                st.session_state.result = f"OpenAI API 發生錯誤: {e}"

st.write(st.session_state.result)
