import streamlit as st
from openai import OpenAI
import time
import openai

# 從 Secrets 拿 Key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

prompt = "分析本月業績：本月1000萬，上月800萬，去年同期1200萬"

# SessionState 儲存結果，避免每次互動都重跑
if "result" not in st.session_state:
    st.session_state.result = ""

# 按鈕觸發呼叫
if st.button("分析業績"):
    # RateLimitError 重試機制
    for i in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.result = response.choices[0].message["content"]
            break
        except openai.error.RateLimitError:
            if i < 2:
                time.sleep(2)  # 等 2 秒再重試
            else:
                st.session_state.result = "請求過多，稍後再試。"

st.write(st.session_state.result)
