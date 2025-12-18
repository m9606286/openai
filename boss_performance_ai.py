import streamlit as st
from openai import OpenAI, error
import time

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

prompt = "分析本月業績：本月1000萬，上月800萬，去年同期1200萬"

if "result" not in st.session_state:
    st.session_state.result = ""

if st.button("分析業績"):
    for i in range(3):  # 重試機制
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.result = response.choices[0].message["content"]
            break
        except error.RateLimitError:
            if i < 2:
                time.sleep(2)
            else:
                st.session_state.result = "請求過多，稍後再試。"

st.write(st.session_state.result)
