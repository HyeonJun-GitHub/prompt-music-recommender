import os
import base64
import requests
import json
import re
import streamlit as st
import openai
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import youtube_search
from youtube_search import YoutubeSearch
from urllib.parse import urlparse, parse_qs
import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html
import cloudscraper
import pyttsx3 as p

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
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )
            # 반환 데이터 안전하게 처리
            choices = completion.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "응답이 없습니다.")
            else:
                return "OpenAI 응답이 비어 있습니다."
        except openai.error.OpenAIError as e:
            return f"OpenAI API 호출 중 오류 발생: {str(e)}"

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
def namu_wiki(query):
    """
Purpose:
Provide detailed and accurate information about songs, artists, or related topics based on user queries.
Prompt:
Analyze the user query to identify the key subject (e.g., a specific artist, song, or related information).
Search reliable sources to gather relevant and accurate details about the subject.
Structure the response with the following format:
Name/Title: (if applicable)
Key Information: Brief introduction or overview.
Notable Works or Achievements: Highlight important works, contributions, or recognitions.
Additional Details: Context, history, or other relevant facts.
Ensure the response is concise, up-to-date, and easy to understand.
Example:

User Query: "Tell me about the singer Sung Si-Kyung."
Agent Response Template:
Name: Sung Si-Kyung
Key Information: Sung Si-Kyung is a South Korean ballad singer known for his smooth vocals and emotional performances. He debuted in 2001 and is often referred to as the "Prince of Ballads."
Notable Works:
"Two People"
"On the Street"
"The Road to Me"
Additional Details: In addition to his music career, he has appeared on various TV shows, such as 2 Days & 1 Night, and has also hosted radio programs.
    """
    url = f"https://ko.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        full_content = data.get("extract", f"'{query}'에 대한 정보를 찾을 수 없습니다.")

        # OpenAI를 사용해 요약 및 질문에 답변 생성
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 전문적인 질문 분석 AI입니다."},
                {"role": "user", "content": f"다음 내용을 읽고 '{query}'에 대해 요약 및 분석을 해주세요:\n{full_content}"}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        return answer

    except httpx.RequestError as e:
        return f"HTTP 요청 중 오류가 발생했습니다: {str(e)}"
    except Exception as e:
        return f"데이터 처리 중 오류가 발생했습니다: {str(e)}"

    
    # try:
    #     response = httpx.get(base_url, headers=headers, cookies=cookies)
    #     response.raise_for_status()
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     content_div = soup.find('div', {'class': 'wiki-paragraph'})
        
    #     if not content_div:
    #         return f"'{query}'에 대한 정보를 찾을 수 없습니다."

    #     summary = content_div.get_text(strip=True)
    #     return summary

    # except httpx.RequestError as e:
    #     return f"HTTP 요청 중 오류가 발생했습니다: {str(e)}"
    # except Exception as e:
    #     return f"데이터 처리 중 오류가 발생했습니다: {str(e)}"

def extract_date(text):
    date_patterns = [
        r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})",  # YYYY-MM-DD
        r"(\d{1,2}월 \d{1,2}일)",             # MM월 DD일
        r"(\d{4}년 \d{1,2}월 \d{1,2}일)"      # YYYY년 MM월 DD일
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None

def select_most_recent(results):
    if not isinstance(results, list):
        return None  # 리스트가 아닌 경우 처리하지 않음

    recent_date = None
    recent_result = None

    for result in results:
        # 결과가 딕셔너리인지 확인
        if not isinstance(result, dict) or "snippet" not in result:
            continue

        date_text = extract_date(result["snippet"])  # 결과의 텍스트에서 날짜 추출
        if date_text:
            try:
                date_obj = datetime.strptime(date_text, "%Y-%m-%d")
                if not recent_date or date_obj > recent_date:
                    recent_date = date_obj
                    recent_result = result
            except ValueError:
                pass  # 날짜 형식이 맞지 않으면 무시
    return recent_result

def web_search(query, source="google"):
    if source == "google":
        url = "https://www.google.com/search"
        params = {"q": query}
    elif source == "naver":
        url = "https://search.naver.com/search.naver"
        params = {"query": query}
    else:
        return f"지원하지 않는 소스입니다: {source}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = httpx.get(url, params=params, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        if source == "google":
            # re 모듈을 안전하게 제거한 방식으로 링크 처리
            links = soup.find_all("a", href=True)
            parsed_links = [
                link["href"].split('&')[0].replace('/url?q=', '')
                for link in links
                if '/url?q=' in link["href"]
            ][:5]
            return parsed_links
        elif source == "naver":
            summaries = soup.find_all('div', {'class': 'api_txt_lines'})
            parsed_summaries = [summary.get_text(strip=True) for summary in summaries[:5]]
            return parsed_summaries
        else:
            return "알 수 없는 소스입니다."

    except httpx.RequestError as re:
        return f"HTTP 요청 중 오류 발생: {re}"
    except Exception as e:
        return f"웹 검색 중 알 수 없는 오류 발생: {e}"

def search_youtube_shorts(query):
    results = YoutubeSearch(query, max_results=3).to_json()
    if isinstance(results, str):
        results = json.loads(results)

    # st.text(results)
    # st.text("---")

    videos = results.get("videos", [])
    result = [
        f'\n{video['title']}\n<iframe width="400" height="215" src="https://www.youtube.com/embed/{extract_parameter_value(video['url_suffix'],"v")}" title="YouTube" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>\n'
        for video in videos
        if "title" in video and "url_suffix" in video
    ]
    return '\n'.join(result)

def extract_parameter_value(url, parameter):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get(parameter, [None])[0]

def search_google(query):
    sources = ["google"]
    all_results = {}

    for source in sources:
        st.text(f"소스 '{source}'에 대해 검색 시작: {query}")
        search_result = web_search(query, source=source)
        
        # 반환 값 디버깅
        st.text(f"'{source}' 검색 결과: {search_result}")

        if isinstance(search_result, str):
            st.text(f"'{source}' 결과가 문자열 형식: {search_result}")
            try:
                search_result = json.loads(search_result)
            except json.JSONDecodeError:
                st.text(f"'{source}' 결과가 JSON 형식이 아닙니다.")
                search_result = None

        if isinstance(search_result, list):
            st.text(f"'{source}' 결과가 리스트 형식. 날짜 기반으로 가장 최신 데이터 선택 중...")
            recent_result = select_most_recent(search_result)
            st.text(f"'{source}' 최신 데이터: {recent_result}")
            all_results[source] = recent_result
        else:
            st.text(f"'{source}' 결과가 비어있거나 처리되지 않았습니다.")
            all_results[source] = search_result  # 원본 저장 (None 포함 가능)

    # 결과 반환
    combined_results = []
    for source, result in all_results.items():
        if result:
            combined_results.append(f"**{source.capitalize()}**: {result}")
            st.text(f"최종 결과 추가: {result}")
        else:
            st.text(f"'{source}'에서 결과 없음.")

    return "\n".join(combined_results)

def chatbot_response(song_data):
    # 결과에서 필요한 데이터를 추출
    songs = song_data.get("song", [])
    artist = song_data.get("artist", "null")
    
    # 대답 생성
    response = ""
    
    if songs:
        response += "안녕하세요! 다음은 지니(geniemusic)에서 찾은 곡 리스트입니다:\n"
        for i, song in enumerate(songs, start=1):
            song_name = song.get("name", "곡명 없음")
            song_id = song.get("id", "song_id 없음")
            response += f"{i}. 곡명: {song_name}\n   song_id: {song_id}\n"
    else:
        response += "안녕하세요! 입력하신 검색어에 대한 곡을 찾지 못했어요. 😢\n"

    if artist == "null":
        response += "그리고 입력하신 검색어에 해당하는 아티스트 정보는 찾지 못했어요. 😥\n"
    else:
        response += f"아티스트 이름: {artist}\n"

    return response

# # 테스트 데이터
# song_data = {
#     "song": [
#         {"name": "가을 아침 - ('아이유 (IU)',)", "id": 87443133},
#         {"name": "가을 아침 - 아이유(IU) (멜로디 MR) - ('Musicsum (뮤직섬)',)", "id": 88228506},
#         {"name": "가을 아침 (아이유) (MR) (-1키) - ('뮤직마루',)", "id": 88369708},
#     ],
#     "artist": "null"
# }

# 아티스트 검색 API 호출 함수
def search_genie(query):
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

        song_cnt = len(song_list) if song_list else 0
        if song_cnt > 3:song_cnt = 3
        song_list = song_list[0:song_cnt]
        
        # 아티스트 이름과 ID 추출
        artist_list = [
            {
                "name": artist["artist_name"].get("original", "Unknown Artist"),
                "id": artist.get("artist_id", None)
            }
            for artist in data.get('searchResult', {}).get('result', {}).get('artists', {}).get('items', [])
        ]
        artist_cnt = len(artist_list) if artist_list else 0
        if artist_cnt > 3:artist_cnt = 3
        artist_list = artist_list[0:artist_cnt]
        
        result = {}
        if song_list:
            result["song"] = song_list
        if artist_list:
            result["artist"] = artist_list

        # JSON 문자열로 반환
        # json.dumps(result, ensure_ascii=False, indent=2)
        msg = chatbot_response(result)
        return msg

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
    "namu_wiki": namu_wiki,
    "search_google": search_google,
    "search_youtube_shorts": search_youtube_shorts,
    "search_genie": search_genie,
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

youtube_embed = '''
<iframe width="400" height="215" src="https://www.youtube.com/embed/LMQ5Gauy17k" title="YouTube video player" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>
'''

# 2. search_google:
# e.g. search_google: 다비치가 부른 최근 방송
# Searches for the most recent information about the given query from Google.
# Returns a summary of the most recent and relevant information from all sources, sorted by date.

# ChatBot 인스턴스 생성
bot_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop, you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

----------------------------------------------------

**Important:** Always provide the final Answer in Korean, regardless of the input language.

----------------------------------------------------

Available Actions:
1. namu_wiki:
e.g. namu_wiki: 성시경 - 거리에서
Purpose:
Provide detailed and accurate information about songs, artists, or related topics based on user queries.

Prompt:

Analyze the user query to identify the key subject (e.g., a specific artist, song, or related information).
Search reliable sources to gather relevant and accurate details about the subject.
Structure the response with the following format:
Name/Title: (if applicable)
Key Information: Brief introduction or overview.
Notable Works or Achievements: Highlight important works, contributions, or recognitions.
Additional Details: Context, history, or other relevant facts.
Ensure the response is concise, up-to-date, and easy to understand.
Example:

User Query: "Tell me about the singer Sung Si-Kyung."
Agent Response Template:
Name: Sung Si-Kyung
Key Information: Sung Si-Kyung is a South Korean ballad singer known for his smooth vocals and emotional performances. He debuted in 2001 and is often referred to as the "Prince of Ballads."
Notable Works:
"Two People"
"On the Street"
"The Road to Me"
Additional Details: In addition to his music career, he has appeared on various TV shows, such as 2 Days & 1 Night, and has also hosted radio programs.

2. search_youtube_shorts:
e.g. search_youtube_shorts: 다비치가 부른 최근 방송
Searches for the most recent information about the given query from YouTube.
Returns a summary of the most recent and relevant information from all sources, sorted by date.

3. search_genie:
e.g. search_genie: 성시경 - 거리에서
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

----------------------------------------------------

**History Management**:
- Every query and its result are stored using the `save_to_history` action.
- The `search_history` action retrieves a previously saved response based on a matching query.
- `analyze_data` automatically checks the history using `search_history` before performing new computations.

----------------------------------------------------

**`search_genie(json format)` Dataset Structure**:
The dataset contains the following variables:

1. 전체 데이터 관련 변수:
- `total`: 데이터의 총 개수입니다. (예: 전체 데이터가 120개인 경우 `total: 120`).
- `size`: 데이터의 크기입니다. 단위는 MB 또는 KB입니다. (예: `size: 10.5`는 10.5MB).
- `items`: 세부 항목의 리스트입니다. 각 항목은 아래 변수를 포함합니다.

2. 공통 변수:
- `artist_name`: 아티스트 이름입니다. (예: `"BTS"`).
- `song_name`: 곡 이름입니다. (예: `"Dynamite"`).
- `album_name`: 앨범 이름입니다. (예: `"BE"`).
- `tag`: 곡 또는 플레이리스트와 관련된 태그입니다. (예: `"pop, dance, hit"`).
- `category`: 데이터의 카테고리를 나타냅니다. (예: `"trending"` 또는 `"user-generated"`).
- `disp_dt`: 데이터가 배포되거나 표시된 날짜입니다. (예: `"2024-12-01"`).
- `reg_dt`: 데이터가 등록된 날짜입니다. (예: `"2024-11-28"`).

3. 특정 데이터 카테고리 관련 변수:
- Playlist:
  - `title`: 플레이리스트 제목입니다. (예: `"Morning Vibes"`).
  - `contents`: 플레이리스트 설명입니다. (예: `"A collection of upbeat songs to start your day."`).
  - `img_path`: 플레이리스트 이미지를 가리키는 경로입니다. (예: `"https://example.com/images/morning_vibes.jpg"`).
  - `song`: 플레이리스트에 포함된 곡의 개수입니다. (예: `25`).
  - `view`: 플레이리스트 조회수입니다. (예: `100000`).
  - `favorite`: 플레이리스트 즐겨찾기 횟수입니다. (예: `5000`).
  - `popular_all`: 전체 기간 동안의 인기 순위입니다. (예: `1`).
  - `popular_recent`: 최근 기간 동안의 인기 순위입니다. (예: `3`).

- Lyrics:
  - `lyrics`: 곡의 가사입니다. (예: `"Oh, oh, I'm in love with you."`).
  - `file_path`: 가사 파일 경로입니다. (예: `"/lyrics/BTS_Dynamite.txt"`).
  - `file_size`: 가사 파일 크기입니다. 단위는 KB 또는 MB입니다. (예: `"1.2 KB"`).

- Songs:
  - `image_path`: 곡과 관련된 이미지 경로입니다. (예: `"https://example.com/images/dynamite.jpg"`).
  - `misspellings`: 곡 이름과 관련된 자주 발생하는 오타 목록입니다. (예: `["dynamite", "dynemite", "dymamite"]`).

4. 메타 데이터:
- `main.start_dt`: 데이터가 활성화되기 시작한 날짜입니다. (예: `"2024-12-01"`).
- `main.end_dt`: 데이터가 비활성화되거나 만료되는 날짜입니다. (예: `"2025-01-01"`).
- `main.reg_dt`: 데이터가 처음 등록된 날짜입니다. (예: `"2024-11-01"`).

----------------------------------------------------

**Link Addition**:
Whenever a song or artist is mentioned in the response, include a link to the song ID in the following format:  
`(https://genie.co.kr/detail/songInfo?xgnm=`song_id`).

----------------------------------------------------

**History Usage in `analyze_data`**:
When `analyze_data` is called:
1. Check the history using `search_history` to see if the query has been answered before.
2. If found, return the saved response.
3. If not found, perform a new computation or analysis, then save the query and response using `save_to_history`.

----------------------------------------------------

Example session:
Question: 성시경의 노래 "거리에서"에 대해 알려줘.
Thought: 성시경과 그의 노래 "거리에서"에 대해 검색해봐야겠어.
Action: search_google: 다비치 최근 방송
PAUSE

Observation: 
search_genie: 성시경은 대한민국의 발라드 가수로, "거리에서"는 이별의 슬픔을 다룬 그의 대표곡 중 하나입니다.
Google: 다비치가 최근 '유희열의 스케치북'에서 '그대는 나의 봄이다'를 공연했습니다 (2024-12-01).
search_youtube_shorts: 유튜브에서 찾은 리스트는 다음과 같습니다. [Duet song festival] 듀엣가요제-Sung Sikyung's mini concert! 20170317 - https://www.youtube.com/watch?v=oaIbr8mz9rk&pp=ygUQ7ISx7Iuc6rK9IOuTgOyXow%3D%3D \n[성시경 노래] 26. 나였으면 (With.나윤권) l Sung Si Kyung Music - https://www.youtube.com/watch?v=1vkKlQr2R4U&pp=ygUQ7ISx7Iuc6rK9IOuTgOyXow%3D%3D  \n성시경 그대네요 (duet with 아이유) (가사 첨부) - https://www.youtube.com/watch?v=e2-CY2VQyFc&pp=ygUQ7ISx7Iuc6rK9IOuTgOyXow%3D%3D  \n[성시경 노래] 60. 우리 참 좋았는데 (With.박정현) l Sung Si Kyung Music - https://www.youtube.com/watch?v=09Il5dbnAUY&pp=ygUQ7ISx7Iuc6rK9IOuTgOyXow%3D%3D  \n[성시경 노래] 21~30 모아듣기 l Sung Si Kyung Music l 희재, 너의 모든 순간, 우린 제법 잘 어울려요, 나였으면, 내게 오는길 - https://www.youtube.com/watch?v=cyrrGfZbXFA&pp=ygUQ7ISx7Iuc6rK9IOuTgOyXow%3D%3D \n

Action: 
save_to_history: { "query": "성시경 - 거리에서", "response": "성시경은 대한민국의 발라드 가수로, '거리에서'는 이별의 슬픔을 다룬 그의 대표곡 중 하나입니다." }

Answer: 
다비치는 대한민국의 발라드 가수로, "그대는 나의 봄이다"는 사랑을 다룬 다비치의 대표곡 중 하나입니다.
다비치는 최근 다양한 방송에서 다음 곡들을 선보였습니다:
1. 유희열의 스케치북: '그대는 나의 봄이다' (2024-12-01)
2. 유튜브 라이브: '사랑해서 그래' (2024-11-30)
3. 음악중심: '시간을 멈춰라' (2024-12-02)

(https://genie.co.kr/detail/songInfo?xgnm=43212134)
""".strip()

engine = p.init()

def query(question, max_turns=1):
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
            observation = known_actions[action](action_input)
            next_prompt = observation
        else:
            return result
    return next_prompt

# 메시지 입력 처리
def on_input_change():
    user_input = st.session_state.user_input
    if user_input.strip():
        st.session_state.past.append(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        if openai_api_key.strip():
            try:
                msg = query(user_input)
                if msg:  # 반환값이 유효한 경우
                    st.session_state.generated.append(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                else:  # 반환값이 None인 경우 디버깅 메시지 추가
                    st.error("Query 함수의 반환값이 None입니다.")
            except Exception as e:
                st.error(f"OpenAI API 호출 중 오류 발생: {e}")
        else:
            st.warning("유효한 OpenAI API 키를 입력해주세요.")

# 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Genie 🤖 : 무엇을 도와드릴까요?"}]
if "past" not in st.session_state:
    st.session_state.past = []
if "generated" not in st.session_state:
    st.session_state.generated = []

# 채팅 기록 표시
if st.session_state.messages:
    message = st.session_state.messages[0]
    role = message["role"]
    content = message["content"]
    if role == "assistant":
        st.markdown(f"<div style='text-align: left; background-color: #FFD700; padding: 10px; border-radius: 15px;'>{content}</div>", unsafe_allow_html=True)


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
        # st.markdown(
        #     f'<div class="chat-bubble ai-message">{youtube_embed}</div>',
        #     unsafe_allow_html=True
        # )

        # custom_message(
        #     msg["data"], 
        #     is_ai=is_ai
        # )
        st.write("")
    engine.say(st.session_state["generated"][len(st.session_state["past"])-1])
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




# test_data = """이해리 '에피소드' 달달한 사랑 노래였네 #다비치 #이해리 #이무진 #에피소드 #singing_the_에피소드 #싱잉더에피소드 - https://www.youtube.com/shorts/mjyRM8HN0yw """
# youtube_embed = '''
# <iframe width="400" height="215" src="https://www.youtube.com/embed/mjyRM8HN0yw" title="이해리 '에피소드' 달달한 사랑 노래였네 #다비치 #이해리 #이무진 #에피소드 #singing_the_에피소드 #싱잉더에피소드" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>
# '''

# st.session_state.setdefault(
#     'past', ['and video of it']
# )

# st.session_state.setdefault(
#     'generated', 
#     [{'type': 'normal', 'data': f'{youtube_embed}'}]
# )


# # Define the custom message method to create chat bubbles
# def custom_message(content, is_ai=False, allow_html=True):
#     if content is None:
#         st.error("Message content is empty or invalid.")
#         return
#     if is_ai:
#         bubble_class = "chat-bubble ai-message"
#     else:
#         bubble_class = "chat-bubble user-message"
    
#     # Wrap the content in a styled div
#     styled_message = f"""
#     <div class="{bubble_class}">
#         {content}
#     이해리 '에피소드' 달달한 사랑 노래였네 #다비치 #이해리 #이무진 #에피소드 #singing_the_에피소드 #싱잉더에피소드
#     """
#     st.markdown(styled_message, unsafe_allow_html=allow_html)

# # Check if "generated" is in session state
# if "generated" not in st.session_state:
#     st.session_state["generated"] = [{"data": "Hello, how can I assist you today?"}, 
#                                      {"data": "Sure, let me check that for you."}]

# # Validate session state
# if not isinstance(st.session_state["generated"], list):
#     st.error("`st.session_state['generated']` is not a list.")
# else:
#     st.markdown(
#         """
#         <style>
#         .chat-bubble {
#             padding: 10px;
#             margin: 10px 0;
#             border-radius: 10px;
#             max-width: 60%;
#         }
#         .ai-message {
#             background-color: #f0f0f0;
#             margin-left: auto;
#             margin-right: 0;
#         }
#         .user-message {
#             background-color: #d1f7d6;
#             margin-right: auto;
#             margin-left: 0;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

    # # Render messages
    # for i, msg in enumerate(st.session_state["generated"]):
    #     if not isinstance(msg, dict) or "data" not in msg:
    #         st.error(f"Message at index {i} is invalid: {msg}")
    #         continue
    #     is_ai = i % 2 == 0  # Example: alternate between AI and user messages
    #     custom_message(
    #         msg["data"], 
    #         is_ai=is_ai
    #     )
