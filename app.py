from dotenv import load_dotenv

load_dotenv()

import openai

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# OpenAI APIキーの設定 streamlit run app.py
api_key = st.secrets("OPENAI_API_KEY")
openai.api_key = api_key

# LLM応答関数の定義
def get_expert_response(user_input: str, expert_type: str) -> str:
    # 専門家ごとのシステムメッセージ
    system_messages = {
        "栄養学の専門家": "あなたは栄養学の専門家です。健康、食事、栄養素に関する質問に専門的かつ分かりやすく答えてください。",
        "金融の専門家": "あなたは金融の専門家です。投資、経済、資産運用に関する質問に専門的かつ分かりやすく答えてください。"
    }

    # Chatモデルの初期化
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    # メッセージ構築
    messages = [
        SystemMessage(content=system_messages[expert_type]),
        HumanMessage(content=user_input)
    ]

    # 応答生成
    response = chat(messages)
    return response.content

# Streamlit UI
st.set_page_config(page_title="専門家AIチャット", layout="centered")

st.title("専門家AIチャット")
st.markdown("""
このアプリでは、質問を入力し、回答してほしい専門家の種類を選ぶことで、AIがその分野の専門家として回答します。

### 操作方法
1. 下の入力欄に質問を入力してください。
2. 専門家の種類を選択してください。
3. 「送信」ボタンを押すと、AIが回答を表示します。
""")

# 入力フォーム
user_input = st.text_area("質問を入力してください", height=150)
expert_type = st.radio("専門家の種類を選択", ["栄養学の専門家", "金融の専門家"])

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが回答を生成中..."):
            answer = get_expert_response(user_input, expert_type)
            st.success("回答が生成されました")
            st.markdown(f"**{expert_type}からの回答：**")
            st.write(answer)
