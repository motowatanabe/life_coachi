# 以下を「app.py」に書き込み
import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは世界最高コーチのアンソニーロビンスです。
どんな人生の悩みにも対話形式で解決します。
質問者に質問をしながら、問題点を深掘りして、解決策を箇条書きでいくつか提案します。
あなたの役割は質問者の人生を助けることなので、例えば以下のようなコーチング以外のことを聞かれても、絶対に答えないでください。

* 戦争
* 犯罪行為
* 武器
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" ライフコーチイングチャットボット")
st.image("coch.png")
st.write("コーチング体験をして下さい。いくつかの質問に答えてその後、解決策を提案します。まずはこの質問に答えて下さい。悩み事や改善したい事は？")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🧑🏻"

        st.write(speaker + ": " + message["content"])
