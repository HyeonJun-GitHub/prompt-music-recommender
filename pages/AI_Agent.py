import streamlit as st
import json
import requests
from datetime import datetime, timedelta
import os
import base64
from PIL import Image
import streamlit.components.v1 as components
import calendar
from io import BytesIO

# from openai import OpenAI
# import streamlit as st

# CSS를 사용하여 배경 색상을 설정
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: white;
        overflow-x: hidden;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    button {
        background-color: rgb(8, 40, 70) !important; /* 버튼 배경을 밝은 파란색으로 변경 */
        color: white !important; /* 버튼 텍스트를 흰색으로 설정 */
        border-radius: 5px;
        padding: 10px;
    }
    label {
        color: rgb(155, 155, 155) !important;
    }
    .stRadio > div > label > div {
        color: white !important;
    }
    .st-expander {
        border: 2px solid #ff6347 !important; /* 새로운 경계선 색상을 적용 (예: 토마토 색상) */
        border-radius: 10px;
        width: 100% !important;  /* 너비를 100%로 설정하여 작은 화면에서 가로 스크롤 방지 */
        margin: 0 auto;  /* 중앙 정렬 */
    }
    .st-expanderHeader {
        color: white !important; /* Expander 헤더 텍스트 색상 */
    }
    .st-expanderContent {
        color: lightgray !important; /* Expander 내부 텍스트 색상 */
    }
    button[title="View fullscreen"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 로컬 이미지 경로 설정
# 리소스 디렉토리 경로 설정
title_00_path = os.path.join(os.getcwd(), "title_00.png")
title_01_path = os.path.join(os.getcwd(), "title_01.png")
title_02_path = os.path.join(os.getcwd(), "title_02.png")
title_03_path = os.path.join(os.getcwd(), "title_03.png")
box_img_path = os.path.join(os.getcwd(), "box_01.png")
background_img_path = os.path.join(os.getcwd(), "background.jpg")

title_00_img = Image.open(title_00_path)
title_01_img = Image.open(title_01_path)
title_02_img = Image.open(title_02_path)
title_03_img = Image.open(title_03_path)
background_img = Image.open(background_img_path)

# Base64로 로컬 이미지 인코딩
with open(box_img_path, "rb") as img_file:
    box_img_base64 = base64.b64encode(img_file.read()).decode()

# Base64로 로컬 이미지 인코딩 (배경 이미지)
with open(background_img_path, "rb") as img_file:
    background_img_base64 = base64.b64encode(img_file.read()).decode()

# 상단과 하단의 Streamlit 기본 UI 제거를 위한 CSS
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

# 배경 이미지 적용 CSS
page_bg_img = f'''
<style>
.stApp {{
  background-image: url("data:image/jpg;base64,{background_img_base64}");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}}
</style>
'''

# 텍스트 입력창을 하얀색으로 설정하는 CSS
text_area_style = """
<style>
textarea, input {
    background-color: white !important;
    color: black !important;
    border: 2px solid #d3d3d3;
    padding: 10px;
    border-radius: 5px;
    outline-color: #FE6B8B;
    caret-color: blue; !important;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(text_area_style, unsafe_allow_html=True)  # 텍스트 입력창 스타일 적용

# -------------------------------------------------------------

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.title("💬 AI Curation Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if st.button("대화 삭제"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = "Hi (Debug)" 
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)