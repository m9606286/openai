import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
prompt = "分析本月業績：本月1000萬，上月800萬，去年同期1200萬"

# 使用 session_state 儲存結果，避免重複呼叫
if "result" not in st.session_state:
    st.session_state.result = ""

if st.button("分析業績"):
    st.session_state.result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message["content"]

st.write(st.session_state.result)
