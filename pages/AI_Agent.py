# import streamlit as st
# import json
# import requests
# from datetime import datetime, timedelta
# import os
# import base64
# from PIL import Image
# import streamlit.components.v1 as components
# import calendar
# from io import BytesIO
# from openai import OpenAI

# # from openai import OpenAI
# # import streamlit as st

# # CSS를 사용하여 배경 색상을 설정
# st.markdown(
#     """
#     <style>
#     .st-chat-message-content { 
#         color: white !important;  /* 텍스트 색상 하얀색으로 변경 */
#     }
#     .stApp {
#         background-color: #000000;
#         color: white;
#         overflow-x: hidden;
#     }
#     h1, h2, h3, h4, h5, h6 {
#         color: white !important;
#     }
#     button {
#         background-color: rgb(8, 40, 70) !important; /* 버튼 배경을 밝은 파란색으로 변경 */
#         color: white !important; /* 버튼 텍스트를 흰색으로 설정 */
#         border-radius: 5px;
#         padding: 10px;
#     }
#     label {
#         color: rgb(155, 155, 155) !important;
#     }
#     .stRadio > div > label > div {
#         color: white !important;
#     }
#     .st-expander {
#         border: 2px solid #ff6347 !important; /* 새로운 경계선 색상을 적용 (예: 토마토 색상) */
#         border-radius: 10px;
#         width: 100% !important;  /* 너비를 100%로 설정하여 작은 화면에서 가로 스크롤 방지 */
#         margin: 0 auto;  /* 중앙 정렬 */
#     }
#     .st-expanderHeader {
#         color: white !important; /* Expander 헤더 텍스트 색상 */
#     }
#     .st-expanderContent {
#         color: lightgray !important; /* Expander 내부 텍스트 색상 */
#     }
#     button[title="View fullscreen"] {
#         display: none;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 로컬 이미지 경로 설정
# # 리소스 디렉토리 경로 설정
# title_00_path = os.path.join(os.getcwd(), "title_00.png")
# title_01_path = os.path.join(os.getcwd(), "title_01.png")
# title_02_path = os.path.join(os.getcwd(), "title_02.png")
# title_03_path = os.path.join(os.getcwd(), "title_03.png")
# box_img_path = os.path.join(os.getcwd(), "box_01.png")
# background_img_path = os.path.join(os.getcwd(), "background.jpg")

# title_00_img = Image.open(title_00_path)
# title_01_img = Image.open(title_01_path)
# title_02_img = Image.open(title_02_path)
# title_03_img = Image.open(title_03_path)
# background_img = Image.open(background_img_path)

# # Base64로 로컬 이미지 인코딩
# with open(box_img_path, "rb") as img_file:
#     box_img_base64 = base64.b64encode(img_file.read()).decode()

# # Base64로 로컬 이미지 인코딩 (배경 이미지)
# with open(background_img_path, "rb") as img_file:
#     background_img_base64 = base64.b64encode(img_file.read()).decode()

# # 상단과 하단의 Streamlit 기본 UI 제거를 위한 CSS
# hide_streamlit_style = """
#     <style>
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     </style>
#     """

# # 배경 이미지 적용 CSS
# page_bg_img = f'''
# <style>
# .stApp {{
#   background-image: url("data:image/jpg;base64,{background_img_base64}");
#   background-size: cover;
#   background-position: center;
#   background-repeat: no-repeat;
# }}
# </style>
# '''

# # 텍스트 입력창을 하얀색으로 설정하는 CSS
# text_area_style = """
# <style>
# textarea, input {
#     background-color: white !important;
#     color: black !important;
#     border: 2px solid #d3d3d3;
#     padding: 10px;
#     border-radius: 5px;
#     outline-color: #FE6B8B;
#     caret-color: blue; !important;
# }
# </style>
# """

# st.markdown(page_bg_img, unsafe_allow_html=True)
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# st.markdown(text_area_style, unsafe_allow_html=True)  # 텍스트 입력창 스타일 적용

# # -------------------------------------------------------------

# # import streamlit as st
# # from streamlit_chat import message
# # from streamlit.components.v1 import html

# # def on_input_change():
# #     user_input = st.session_state.user_input
# #     st.session_state.past.append(user_input)
# #     st.session_state.generated.append("The messages from Bot\nWith new line")

# # def on_btn_click():
# #     del st.session_state.past[:]
# #     del st.session_state.generated[:]

# # audio_path = "https://docs.google.com/uc?export=open&id=16QSvoLWNxeqco_Wb2JvzaReSAw5ow6Cl"
# # img_path = "https://www.groundzeroweb.com/wp-content/uploads/2017/05/Funny-Cat-Memes-11.jpg"
# # youtube_embed = '''
# # <iframe width="400" height="215" src="https://www.youtube.com/embed/LMQ5Gauy17k" title="YouTube video player" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>
# # '''

# # markdown = """
# # ### HTML in markdown is ~quite~ **unsafe**
# # <blockquote>
# #   However, if you are in a trusted environment (you trust the markdown). You can use allow_html props to enable support for html.
# # </blockquote>

# # * Lists
# # * [ ] todo
# # * [x] done

# # Math:

# # Lift($L$) can be determined by Lift Coefficient ($C_L$) like the following
# # equation.

# # $$
# # L = \\frac{1}{2} \\rho v^2 S C_L
# # $$

# # ~~~py
# # import streamlit as st

# # st.write("Python code block")
# # ~~~

# # ~~~js
# # console.log("Here is some JavaScript code")
# # ~~~

# # """

# # table_markdown = '''
# # A Table:

# # | Feature     | Support              |
# # | ----------: | :------------------- |
# # | CommonMark  | 100%                 |
# # | GFM         | 100% w/ `remark-gfm` |
# # '''

# # st.session_state.setdefault(
# #     'past', 
# #     ['plan text with line break',
# #      'play the song "Dancing Vegetables"', 
# #      'show me image of cat', 
# #      'and video of it',
# #      'show me some markdown sample',
# #      'table in markdown']
# # )
# # st.session_state.setdefault(
# #     'generated', 
# #     [{'type': 'normal', 'data': 'Line 1 \n Line 2 \n Line 3'},
# #      {'type': 'normal', 'data': f'<audio controls src="{audio_path}"></audio>'}, 
# #      {'type': 'normal', 'data': f'<img width="100%" height="200" src="{img_path}"/>'}, 
# #      {'type': 'normal', 'data': f'{youtube_embed}'},
# #      {'type': 'normal', 'data': f'{markdown}'},
# #      {'type': 'table', 'data': f'{table_markdown}'}]
# # )

# # st.title("Chat placeholder")

# # chat_placeholder = st.empty()

# # with chat_placeholder.container():    
# #     for i in range(len(st.session_state['generated'])):                
# #         message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
# #         message(
# #             st.session_state['generated'][i]['data'], 
# #             key=f"{i}", 
# #             allow_html=True,
# #             is_table=True if st.session_state['generated'][i]['type']=='table' else False
# #         )

# #     st.button("Clear message", on_click=on_btn_click)

# # with st.container():
# #     st.text_input("User Input:", on_change=on_input_change, key="user_input")

# # -------------------------------------------------------------

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# st.title("💬 AI Curation Chatbot")

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# if st.button("대화 삭제"):
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():

#     if not openai_api_key:
#         st.info("openai key를 입력해주세요.")
#         st.stop()

#     # 유저 메시지 추가
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     client = OpenAI(api_key=openai_api_key)
#     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
#     msg = response.choices[0].message.content
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)

import streamlit as st
import base64
import os
from PIL import Image
from openai import OpenAI

# CSS 스타일 정의
st.markdown(
    """
    <style>
    .st-chat-message-content { 
        color: white !important;  /* 텍스트 색상 하얀색으로 변경 */
    }
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
    textarea, input {
        background-color: white !important;
        color: black !important;
        border: 2px solid #d3d3d3;
        padding: 10px;
        border-radius: 5px;
        outline-color: #FE6B8B;
        caret-color: blue !important;
    }
    .stRadio > div > label > div {
        color: white !important;
    }
    .st-expander {
        border: 2px solid #ff6347 !important; /* 새로운 경계선 색상을 적용 (예: 토마토 색상) */
        border-radius: 10px;
        width: 100% !important;
        margin: 0 auto;
    }
    .st-expanderHeader {
        color: white !important;
    }
    .st-expanderContent {
        color: lightgray !important;
    }
    button[title="View fullscreen"] {
        display: none;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# 배경 이미지 경로 설정
background_img_path = os.path.join(os.getcwd(), "background.jpg")
with open(background_img_path, "rb") as img_file:
    background_img_base64 = base64.b64encode(img_file.read()).decode()

# 배경 이미지 적용
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

# 사이드바: OpenAI API 키 입력
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# 제목 및 초기 메시지 설정
st.title("💬 AI Curation Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# 대화 삭제 버튼
if st.button("대화 삭제"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# 메시지 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input():

    if not openai_api_key:
        st.info("OpenAI API Key를 입력해주세요.")
        st.stop()

    # 유저 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # OpenAI API 호출
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
