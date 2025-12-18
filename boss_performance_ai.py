import streamlit as st
from openai import OpenAI

# 從 Streamlit Secrets 拿 Key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ai_analyze(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

prompt = "請分析本月業績：本月1000萬，上月800萬，去年同期1200萬"
result = ai_analyze(prompt)

st.write(result)
