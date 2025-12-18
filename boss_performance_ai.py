import streamlit as st
import openai
import os

# ========== 設定你的 API KEY ==========
openai.api_key = os.getenv("OPENAI_API_KEY")

# ========== AI 分析函式 ==========
def ai_analyze(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是專為公司老闆服務的業績分析助理，語氣精準、果斷、以決策為導向"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ========== 網頁介面 ==========
st.set_page_config(page_title="老闆版業績 AI", layout="centered")
st.title("📊 老闆版業績 AI 分析")

st.write("請輸入關鍵業績數字，系統將自動產生決策用分析。")

current = st.number_input("本月營收（萬元）", min_value=0.0, step=100.0)
last_month = st.number_input("上月營收（萬元）", min_value=0.0, step=100.0)
last_year = st.number_input("去年同期營收（萬元）", min_value=0.0, step=100.0)

if st.button("🚀 產生業績分析"):
    if last_month > 0 and last_year > 0:
        mom = (current - last_month) / last_month * 100
        yoy = (current - last_year) / last_year * 100

        prompt = f"""
本月營收 {current:.0f} 萬元，
上月 {last_month:.0f} 萬元（MoM {mom:.1f}%），
去年同期 {last_year:.0f} 萬元（YoY {yoy:.1f}%）。

請用老闆看的語氣輸出：
1. 一句話結論
2. 關鍵觀察
3. 風險提醒
4. 建議決策
"""

        with st.spinner("AI 分析中..."):
            result = ai_analyze(prompt)

        st.success("分析完成")
        st.markdown(result)
    else:
        st.warning("上月與去年同期營收需大於 0")

