import streamlit as st
import google.generativeai as genai
import json
import os

# 1. 初始化 API 與 模擬資料庫
genai.configure(api_key="AIzaSyCXvYrU1GLwwtzxCCS5wAhOCVMtWn12rp8")
DB_FILE = "business_memory.json"

# 模擬資料庫讀取函數
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 模擬資料庫儲存函數
def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

# --- 介面開始 ---
st.title("🧠 綠金園 AI 戰略大腦 (研發版)")

# 2. 業務與客戶身份識別
col1, col2 = st.columns(2)
with col1:
    sales_id = st.text_input("業務編號", value="Sales_01")
with col2:
    client_name = st.text_input("客戶姓名", placeholder="例如：陳先生")

# 3. 載入該業務對該客戶的「專屬記憶」
db = load_db()
client_memory = db.get(sales_id, {}).get(client_name, [])

if client_name:
    st.info(f"📋 過去與 {client_name} 的互動紀錄：{len(client_memory)} 則")
    for msg in client_memory[-2:]: # 顯示最近兩則
        st.write(f"🔹 {msg['role']}: {msg['content'][:50]}...")

# 4. 對話輸入
user_input = st.chat_input("請輸入今日對談重點或客戶問題...")

if user_input:
    # 建立 Context (上下文)
    # 我們把過去的記憶塞進 Prompt，讓 AI 瞬間「想起」這個客戶
    context = "\n".join([f"{m['role']}: {m['content']}" for m in client_memory])
    
    full_prompt = f"""
    你現在是綠金園的銷售專家。
    【業務 ID】: {sales_id}
    【客戶姓名】: {client_name}
    【過去對話背景】: 
    {context}
    
    【今日客戶新問題】: {user_input}
    
    請根據過去的背景，給出最精準的銷售策略。
    """
    
    # 5. 呼叫 AI
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(full_prompt)
    
    # 6. 更新記憶並存回資料庫
    if sales_id not in db: db[sales_id] = {}
    if client_name not in db[sales_id]: db[sales_id][client_name] = []
    
    # 存入本次對話
    db[sales_id][client_name].append({"role": "user", "content": user_input})
    db[sales_id][client_name].append({"role": "assistant", "content": response.text})
    save_db(db)
    
    st.markdown(f"### 🚀 AI 建議策略：\n{response.text}")
