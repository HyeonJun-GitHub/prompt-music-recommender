import os
import base64
import streamlit as st
from openai import OpenAI

# 사이드바에서 OpenAI API 키 입력
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# 배경 이미지 설정 (옵션)
background_img_path = os.path.join(os.getcwd(), "background.jpg")
if os.path.exists(background_img_path):
    with open(background_img_path, "rb") as img_file:
        background_img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{background_img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# CSS 스타일 정의
# CSS 스타일 정의
st.markdown(
    """
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .chat-bubble {
        padding: 10px 15px;
        margin: 10px 0;
        font-size: 16px;
        word-wrap: break-word;
    }
    .user-message {
        background-color: rgb(8, 40, 70);
        color: black;
        text-align: right;
        margin-left: auto;
        border: 2px solid #ccc;
        border-radius: 15px;
        border-top-right-radius: 0px;
        width: 50%; /* 사용자의 말풍선 너비를 50%로 제한 */
    }
    .ai-message {
        color: white;
        text-align: left;
        margin-right: auto;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]
if "past" not in st.session_state:
    st.session_state.past = []
if "generated" not in st.session_state:
    st.session_state.generated = []

# 메시지 입력 처리
def on_input_change():
    user_input = st.session_state.user_input

    if user_input.strip():
        # 사용자 메시지 저장
        st.session_state.past.append(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # OpenAI API 호출
        if openai_api_key.strip():
            try:
                client = OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                msg = response.choices[0].message.content

                # 응답 메시지 저장
                st.session_state.generated.append(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})

            except Exception as e:
                st.error(f"OpenAI API 호출 중 오류 발생: {e}")
        else:
            st.warning("Please enter a valid OpenAI API key.")

# 메시지 초기화
def on_btn_click():
    st.session_state.past.clear()
    st.session_state.generated.clear()
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]

# 제목 표시
st.title("💬 Genie 에이전트")

# 채팅 UI
chat_placeholder = st.empty()
with chat_placeholder.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for i in range(len(st.session_state["past"])):
        # 사용자 메시지 출력
        st.markdown(
            f'<div class="chat-bubble user-message">{st.session_state["past"][i]}</div>',
            unsafe_allow_html=True
        )
        # AI 응답 메시지 출력
        st.markdown(
            f'<div class="chat-bubble ai-message">{st.session_state["generated"][i]}</div>',
            unsafe_allow_html=True
        )
        st.write("")
    st.markdown('</div>', unsafe_allow_html=True)

# 초기화 버튼
st.button("Clear Messages", on_click=on_btn_click)

# 사용자 입력 필드
st.text_input("Your Message:", on_change=on_input_change, key="user_input")
