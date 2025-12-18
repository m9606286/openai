import streamlit as st
import google.generativeai as genai
import time

# 設定金鑰
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 1. 自動偵測可用的模型名稱
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # 優先順序：1.5 Flash -> 1.5 Pro -> Pro
    for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
        if target in available_models:
            return target
    return available_models[0] if available_models else None

# 初始化模型
working_model_name = get_working_model()
if working_model_name:
    model = genai.GenerativeModel(working_model_name)
else:
    st.error("找不到可用的 Gemini 模型，請檢查 API Key 權限。")

prompt = "分析本月業績：本月1000萬，上月800萬，去年同期1200萬"

if "result" not in st.session_state:
    st.session_state.result = ""

if st.button("分析業績"):
    with st.spinner(f"使用 {working_model_name} 分析中..."):
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
