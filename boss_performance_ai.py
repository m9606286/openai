import streamlit as st
import openai
import time

# 從 Secrets 拿 API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

prompt = "分析本月業績：本月1000萬，上月800萬，去年同期1200萬"

# SessionState 儲存結果
if "result" not in st.session_state:
    st.session_state.result = ""

# 按鈕觸發呼叫 API
if st.button("分析業績"):
    for i in range(3):  # 重試機制
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.result = response.choices[0].message["content"]
            break
        except openai.error.RateLimitError:
            if i < 2:
                time.sleep(2)
            else:
                st.session_state.result = "請求過多，稍後再試。"
        except openai.error.OpenAIError as e:
            st.session_state.result = f"OpenAI API 發生錯誤: {e}"

st.write(st.session_state.result)
