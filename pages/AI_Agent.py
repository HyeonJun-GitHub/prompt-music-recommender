# import os
# import base64
# import requests
# import json
# import streamlit as st
# from openai import OpenAI

# # 사이드바에서 OpenAI API 키 입력
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# # 배경 이미지 설정 (옵션)
# background_img_path = os.path.join(os.getcwd(), "background.jpg")
# if os.path.exists(background_img_path):
#     with open(background_img_path, "rb") as img_file:
#         background_img_base64 = base64.b64encode(img_file.read()).decode()
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("data:image/jpg;base64,{background_img_base64}");
#             background-size: cover;
#             background-position: center;
#             background-repeat: no-repeat;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # CSS 스타일 정의
# st.markdown(
#     """
#     <style>
#     .chat-container {
#         display: flex;
#         flex-direction: column;
#         gap: 10px;
#     }
#     .chat-bubble {
#         padding: 10px 15px;
#         margin: 10px 0;
#         font-size: 16px;
#         word-wrap: break-word;
#     }
#     .user-message {
#         background-color: #D3D3D3;
#         color: black;
#         text-align: right;
#         margin-left: auto;
#         border: 2px solid #ccc;
#         border-radius: 15px;
#         border-top-right-radius: 0px;
#         width: 50%; /* 사용자의 말풍선 너비를 50%로 제한 */
#     }
#     .ai-message {
#         color: white;
#         text-align: left;
#         margin-right: auto;
#         font-size: 16px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 상태 초기화
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]
# if "past" not in st.session_state:
#     st.session_state.past = []
# if "generated" not in st.session_state:
#     st.session_state.generated = []

# # 아티스트 검색 API 호출 함수
# def search_api(query):
#     url = f"http://app.genie.co.kr/search/main/search.json?query={query}"
    
#     headers = {
#         "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
#     }
    
#     try:
#         # API 호출 시 헤더 추가
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
        
#         try:
#             data = response.json()  # JSON 형식으로 변환 시도
#         except ValueError:
#             st.error("API 응답이 JSON 형식이 아닙니다. 응답 내용: " + response.text)
#             return [], []
        
#         # 곡 이름과 ID 추출
#         song_list = [
#             {
#                 "name": f"{song["song_name"].get("original", "Unknown Song")} - {song["artist_name"].get("original", "Unknown Song"),}",
#                 "id": song.get("song_id", None)
#             }
#             for song in data.get('searchResult', {}).get('result', {}).get('songs', {}).get('items', [])
#         ]
        
#         # 아티스트 이름과 ID 추출
#         artist_list = [
#             {
#                 "name": artist["artist_name"].get("original", "Unknown Artist"),
#                 "id": artist.get("artist_id", None)
#             }
#             for artist in data.get('searchResult', {}).get('result', {}).get('artists', {}).get('items', [])
#         ]
        
#         result = {
#             "song": song_list if song_list else "null",
#             "artist": artist_list if artist_list else "null"
#         }
        
#         # JSON 문자열로 반환
#         return json.dumps(result, ensure_ascii=False, indent=2)

#     except requests.exceptions.RequestException as e:
#         return json.dumps({"song": "null", "artist": "null"}, ensure_ascii=False)

#     # except requests.exceptions.RequestException as e:
#     #     st.error(f"API 요청 중 오류 발생: {e}")
#     #     return [], []


# # 메시지 입력 처리
# def on_input_change():

#     if not openai_api_key.strip():
#         st.warning("OpenAI API key를 입력해주세요.")
#         return

#     user_input = st.session_state.user_input

#     if user_input.strip():
#         # 사용자 메시지 저장
#         st.session_state.past.append(user_input)
#         st.session_state.messages.append({"role": "user", "content": user_input})

#         # OpenAI API 호출
#         if openai_api_key.strip():
#             try:
#                 client = OpenAI(api_key=openai_api_key)
#                 response = client.chat.completions.create(
#                     model="gpt-3.5-turbo",
#                     messages=st.session_state.messages
#                 )
#                 msg = response.choices[0].message.content

#                 # 응답 메시지 저장
#                 st.session_state.generated.append(msg)
#                 st.session_state.messages.append({"role": "assistant", "content": msg})

#             except Exception as e:
#                 st.error(f"OpenAI API 호출 중 오류 발생: {e}")
#         else:
#             st.warning("Please enter a valid OpenAI API key.")

# # 메시지 초기화
# def on_btn_click():
#     st.session_state.past.clear()
#     st.session_state.generated.clear()
#     st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]

# # 제목 표시
# st.title("💬 Genie 에이전트")

# # 채팅 UI
# chat_placeholder = st.empty()
# with chat_placeholder.container():
#     st.markdown('<div class="chat-container">', unsafe_allow_html=True)
#     for i in range(len(st.session_state["past"])):
#         # 사용자 메시지 출력
#         st.markdown(
#             f'<div class="chat-bubble user-message">{st.session_state["past"][i]}</div>',
#             unsafe_allow_html=True
#         )
#         # AI 응답 메시지 출력
#         st.markdown(
#             f'<div class="chat-bubble ai-message">{st.session_state["generated"][i]}</div>',
#             unsafe_allow_html=True
#         )
#         st.write("")
#     st.markdown('</div>', unsafe_allow_html=True)

# st.markdown(
#     """
#     <hr style="border: 1px solid white; margin: 20px 0;">
#     """,
#     unsafe_allow_html=True
# )

# # 초기화 버튼
# st.button("대화 삭제", on_click=on_btn_click)

# # 사용자 입력 필드
# st.text_input("메세지:", on_change=on_input_change, key="user_input")

import os
import base64
import requests
import json
import re
import streamlit as st
from openai import OpenAI
import openai
import httpx

# OpenAI API Key 설정
openai_api_key = st.sidebar.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
os.environ["OPENAI_API_KEY"] = openai_api_key

# ChatBot 클래스 정의
class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        return completion.choices[0].message.content

# Action 처리 함수 정의
def wikipedia(q):
    response = httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    })
    return response.json()["query"]["search"][0]["snippet"]

def calculate(what):
    return eval(what)

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
}

action_re = re.compile(r'^Action: (\w+): (.*)')

# ChatBot과 Streamlit 통합
st.title("💬 AI ChatBot")
st.markdown("Chat with AI using custom prompts and dynamic actions.")

# 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# ChatBot 인스턴스 생성
bot_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.
""".strip()
chat_bot = ChatBot(system=bot_prompt)

# 메시지 입력 처리
def process_message():
    user_input = st.session_state.user_input
    if not openai_api_key:
        st.warning("OpenAI API Key를 입력하세요.")
        return
    
    if user_input.strip():
        # 사용자 입력을 ChatBot에 전달
        result = chat_bot(user_input)
        openai.api_key = openai_api_key

        # 액션 처리
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            action, action_input = actions[0].groups()
            if action in known_actions:
                observation = known_actions[action](action_input)
                result += f"\nObservation: {observation}"
            else:
                result += f"\nUnknown action: {action}"

        # 메시지 저장
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": result})

# 초기화 버튼
if st.button("대화 초기화"):
    st.session_state.messages = []

# 사용자 입력 필드
st.text_input("메세지:", on_change=process_message, key="user_input")

# 채팅 기록 표시
if st.session_state.messages:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "user":
            st.markdown(f"<div style='text-align: right; background-color: #D3D3D3; padding: 10px; border-radius: 15px;'>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; background-color: #FFD700; padding: 10px; border-radius: 15px;'>{content}</div>", unsafe_allow_html=True)
