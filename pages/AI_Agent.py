import os
import base64
import requests
import json
import re
import streamlit as st
import openai
import httpx

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
        try:
            # Use the latest syntax
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )
            # Extract and return the response
            return completion["choices"][0]["message"]["content"]
        except openai.error.OpenAIError as e:
            # Gracefully handle OpenAI API errors
            return f"Error with OpenAI API: {str(e)}"

# 히스토리 저장 및 검색
history = []

def save_to_history(data):
    """히스토리에 데이터를 저장합니다."""
    history.append(data)

def search_history(query):
    """히스토리에서 쿼리에 해당하는 데이터를 검색합니다."""
    for item in history:
        if item.get("query") == query:
            return item.get("response")
    return None

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


# 아티스트 검색 API 호출 함수
def search_api(query):
    url = f"http://app.genie.co.kr/search/main/search.json?query={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    }
    
    try:
        # API 호출 시 헤더 추가
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
        
        try:
            data = response.json()  # JSON 형식으로 변환 시도
        except ValueError:
            st.error("API 응답이 JSON 형식이 아닙니다. 응답 내용: " + response.text)
            return [], []
        
        # 곡 이름과 ID 추출
        song_list = [
            {
                "name": f"{song["song_name"].get("original", "Unknown Song")} - {song["artist_name"].get("original", "Unknown Song"),}",
                "id": song.get("song_id", None)
            }
            for song in data.get('searchResult', {}).get('result', {}).get('songs', {}).get('items', [])
        ]
        
        # 아티스트 이름과 ID 추출
        artist_list = [
            {
                "name": artist["artist_name"].get("original", "Unknown Artist"),
                "id": artist.get("artist_id", None)
            }
            for artist in data.get('searchResult', {}).get('result', {}).get('artists', {}).get('items', [])
        ]
        
        result = {
            "song": song_list if song_list else "null",
            "artist": artist_list if artist_list else "null"
        }
        
        # JSON 문자열로 반환
        return json.dumps(result, ensure_ascii=False, indent=2)

    except requests.exceptions.RequestException as e:
        return json.dumps({"song": "null", "artist": "null"}, ensure_ascii=False)

    # except requests.exceptions.RequestException as e:
    #     st.error(f"API 요청 중 오류 발생: {e}")
    #     return [], []

def analyze_data(query):
    """데이터를 분석하거나 히스토리에서 검색"""
    cached_response = search_history(query)
    if cached_response:
        return cached_response
    return "No cached data. Please run a search first."

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "search_api": search_api,
    "save_to_history": save_to_history,
    "search_history": search_history,
    "analyze_data": analyze_data,
}

action_re = re.compile(r'^Action: (\w+): (.*)')

# 사이드바에서 OpenAI API 키 입력
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    openai.api_key = openai_api_key
    os.environ["OPENAI_API_KEY"] = openai_api_key

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
        display: inline-block;
        max-width: 80%; /* 말풍선의 최대 너비를 80%로 제한 */
    }
    .user-message {
        background-color: #ffffff; /*#D3D3D3;*/
        color: black;
        text-align: left; /* 말풍선 내부 텍스트는 왼쪽 정렬 */
        float: right; /* 말풍선을 오른쪽으로 정렬 */
        clear: both; /* 말풍선 사이 간격 보장 */
        border: 2px solid #ccc;
        border-radius: 15px;
        border-top-right-radius: 0px;
    }
    .ai-message {
        background-color: #3e95f8;
        color: white;
        text-align: left; /* 말풍선 내부 텍스트는 왼쪽 정렬 */
        float: left; /* 말풍선을 왼쪽으로 정렬 */
        clear: both; /* 말풍선 사이 간격 보장 */
        border: 2px solid #ccc;
        border-radius: 15px;
        border-top-left-radius: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Genie 🤖 : 무엇을 도와드릴까요?"}]
if "past" not in st.session_state:
    st.session_state.past = []
if "generated" not in st.session_state:
    st.session_state.generated = []


# 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# ChatBot 인스턴스 생성
bot_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop, you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

**Important:** Always provide the final Answer in Korean, regardless of the input language.

Available Actions:
1. calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python, so be sure to use floating point syntax if necessary.

2. wikipedia:
e.g. wikipedia: 서울
Returns a summary from searching Wikipedia.

3. search_api:
e.g. search_api: 성시경 - 거리에서
Search Simon's blog for information about both artists and song titles. If the name or title is in Korean, use the Korean characters.

4. save_to_history:
e.g. save_to_history: { "query": "성시경 - 거리에서", "response": "성시경은 대한민국의 발라드 가수로, '거리에서'는 이별의 슬픔을 다룬 그의 대표곡 중 하나입니다." }
Saves a query and its corresponding response into the history.

5. search_history:
e.g. search_history: "성시경 - 거리에서"
Searches the history for a query and returns the saved response, if available.

6. analyze_data:
e.g. analyze_data: { "query": "Playlists with over 10,000 views" }
Analyzes data by either searching the history for a matching query or performing new computations based on the dataset structure provided below.

**History Management**:
- Every query and its result are stored using the `save_to_history` action.
- The `search_history` action retrieves a previously saved response based on a matching query.
- `analyze_data` automatically checks the history using `search_history` before performing new computations.

**Dataset Structure**:
The dataset contains the following variables:

**1. 전체 데이터 관련 변수**:
- `total`: 데이터의 총 개수입니다. (예: 전체 데이터가 120개인 경우 `total: 120`).
- `size`: 데이터의 크기입니다. 단위는 MB 또는 KB입니다. (예: `size: 10.5`는 10.5MB).
- `items`: 세부 항목의 리스트입니다. 각 항목은 아래 변수를 포함합니다.

**2. 공통 변수**:
- `artist_name`: 아티스트 이름입니다. (예: `"BTS"`).
- `song_name`: 곡 이름입니다. (예: `"Dynamite"`).
- `album_name`: 앨범 이름입니다. (예: `"BE"`).
- `tag`: 곡 또는 플레이리스트와 관련된 태그입니다. (예: `"pop, dance, hit"`).
- `category`: 데이터의 카테고리를 나타냅니다. (예: `"trending"` 또는 `"user-generated"`).
- `disp_dt`: 데이터가 배포되거나 표시된 날짜입니다. (예: `"2024-12-01"`).
- `reg_dt`: 데이터가 등록된 날짜입니다. (예: `"2024-11-28"`).

**3. 특정 데이터 카테고리 관련 변수**:
- **Playlist**:
  - `title`: 플레이리스트 제목입니다. (예: `"Morning Vibes"`).
  - `contents`: 플레이리스트 설명입니다. (예: `"A collection of upbeat songs to start your day."`).
  - `img_path`: 플레이리스트 이미지를 가리키는 경로입니다. (예: `"https://example.com/images/morning_vibes.jpg"`).
  - `song`: 플레이리스트에 포함된 곡의 개수입니다. (예: `25`).
  - `view`: 플레이리스트 조회수입니다. (예: `100000`).
  - `favorite`: 플레이리스트 즐겨찾기 횟수입니다. (예: `5000`).
  - `popular_all`: 전체 기간 동안의 인기 순위입니다. (예: `1`).
  - `popular_recent`: 최근 기간 동안의 인기 순위입니다. (예: `3`).

- **Lyrics**:
  - `lyrics`: 곡의 가사입니다. (예: `"Oh, oh, I'm in love with you."`).
  - `file_path`: 가사 파일 경로입니다. (예: `"/lyrics/BTS_Dynamite.txt"`).
  - `file_size`: 가사 파일 크기입니다. 단위는 KB 또는 MB입니다. (예: `"1.2 KB"`).

- **Songs**:
  - `image_path`: 곡과 관련된 이미지 경로입니다. (예: `"https://example.com/images/dynamite.jpg"`).
  - `misspellings`: 곡 이름과 관련된 자주 발생하는 오타 목록입니다. (예: `["dynamite", "dynemite", "dymamite"]`).

**4. 메타 데이터**:
- `main.start_dt`: 데이터가 활성화되기 시작한 날짜입니다. (예: `"2024-12-01"`).
- `main.end_dt`: 데이터가 비활성화되거나 만료되는 날짜입니다. (예: `"2025-01-01"`).
- `main.reg_dt`: 데이터가 처음 등록된 날짜입니다. (예: `"2024-11-01"`).

**Link Addition**:
Whenever a song or artist is mentioned in the response, include a link to the song ID in the following format:  
`(https://genie.co.kr/detail/songInfo?xgnm=`song_id`).

**History Usage in `analyze_data`**:
When `analyze_data` is called:
1. Check the history using `search_history` to see if the query has been answered before.
2. If found, return the saved response.
3. If not found, perform a new computation or analysis, then save the query and response using `save_to_history`.

Example session:
Question: 성시경의 노래 "거리에서"에 대해 알려줘.
Thought: 성시경과 그의 노래 "거리에서"에 대해 검색해봐야겠어.
Action: search_api: 성시경 - 거리에서
PAUSE

Observation: 성시경은 대한민국의 발라드 가수로, "거리에서"는 이별의 슬픔을 다룬 그의 대표곡 중 하나입니다.
Action: save_to_history: { "query": "성시경 - 거리에서", "response": "성시경은 대한민국의 발라드 가수로, '거리에서'는 이별의 슬픔을 다룬 그의 대표곡 중 하나입니다." }
Answer: 성시경은 대한민국의 발라드 가수로, "거리에서"는 이별의 슬픔을 다룬 그의 대표곡 중 하나입니다.
(https://genie.co.kr/detail/songInfo?xgnm=43212134)
""".strip()

# chat_bot = ChatBot(system=bot_prompt)

def query(question, max_turns=3):
    i = 0
    bot = ChatBot(bot_prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(f"Unknown action: {action}: {action_input}")
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = f"Observation: {observation}"
        else:
            return result
        
# 메시지 입력 처리
def on_input_change():

    if not openai_api_key.strip():
        st.warning("OpenAI API key를 입력해주세요.")
        return

    user_input = st.session_state.user_input

    if user_input.strip():
        # 사용자 메시지 저장
        st.session_state.past.append(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # OpenAI API 호출
        if openai_api_key.strip():
            try:
                # client = OpenAI(api_key=openai_api_key)
                # response = client.chat.completions.create(
                #     model="gpt-3.5-turbo",
                #     messages=st.session_state.messages
                # )
                # msg = response.choices[0].message.content
                msg = query(user_input)

                # 응답 메시지 저장
                # st.session_state.generated.append(msg)
                # st.session_state.messages.append({"role": "assistant", "content": msg})

            except Exception as e:
                msg = "찾은 내용이 없습니다."
                st.error(f"OpenAI API 호출 중 오류 발생: {e}")

            st.session_state.generated.append(msg or "No response available.")
        else:
            st.warning("Please enter a valid OpenAI API key.")
            
# # 메시지 입력 처리
# def process_message():
#     user_input = st.session_state.user_input
#     if not openai_api_key:
#         st.warning("OpenAI API Key를 입력하세요.")
#         return
    
#     if user_input.strip():
#         # 사용자 입력을 ChatBot에 전달
#         result = chat_bot(user_input)

#         # 액션 처리
#         actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
#         if actions:
#             action, action_input = actions[0].groups()
#             if action in known_actions:
#                 observation = known_actions[action](action_input)
#                 result += f"\nObservation: {observation}"
#             else:
#                 result += f"\nUnknown action: {action}"

#         # 메시지 저장
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         st.session_state.messages.append({"role": "assistant", "content": result})

# 채팅 기록 표시
if st.session_state.messages:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "assistant":
            st.markdown(f"<div style='text-align: left; background-color: #FFD700; padding: 10px; border-radius: 15px;'>{content}</div>", unsafe_allow_html=True)
        # else:
            # st.markdown(f"<div style='text-align: right; background-color: #D3D3D3; padding: 10px; border-radius: 15px;'>{content}</div>", unsafe_allow_html=True)

# 메시지 초기화
def on_btn_click():
    st.session_state.past.clear()
    st.session_state.generated.clear()
    st.session_state.messages = [{"role": "assistant", "content": "Genie 🤖 : 무엇을 도와드릴까요?"}]

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

st.markdown(
    """
    <hr style="border: 1px solid white; margin: 20px 0;">
    """,
    unsafe_allow_html=True
)

# 초기화 버튼
st.button("대화 삭제", on_click=on_btn_click)

# 사용자 입력 필드
st.text_input("메세지:", on_change=on_input_change, key="user_input")











# # ChatBot과 Streamlit 통합
# st.title("💬 AI ChatBot")
# st.markdown("Chat with AI using custom prompts and dynamic actions.")
