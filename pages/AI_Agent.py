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
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = "Hi (Debug)" #response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

# st.image(title_00_img, caption='', use_column_width=True)
# # 레이아웃 시작
# st.write("---")
# st.title("검색 설정")
# segment = st.radio("국가 선택", ("전체", "국내", "해외"))

# album_release_country = ""
# if segment == "전체":
#     album_release_country = ""
# elif segment == "국내":
#     album_release_country = "KOREA"
# elif segment == "해외":
#     album_release_country = "POPULAR"

# # 현재 날짜와 과거 날짜 설정
# day_number = 365 * 5
# current_date = datetime.now()  # 최대값 (오늘)
# past_date = current_date - timedelta(days=day_number)  # 최소값
# date_range = [(past_date + timedelta(days=x)).strftime('%Y%m') for x in range(0, day_number+1, 30)]  # 매월 1회씩

# st.markdown("""
#     <style>
#     /* 슬라이더 바 색상 */
#     .streamlit-slider > div[data-baseweb="slider"] > div {
#         background: linear-gradient(to right, #1E90FF, #87CEEB); /* 파란색 그라데이션 */
#     }
#     /* 슬라이더 핸들 색상 */
#     .streamlit-slider > div[data-baseweb="slider"] > div > div > div {
#         background-color: #1E90FF; /* 슬라이더 핸들 파란색 */
#     }
#     </style>
#     """, unsafe_allow_html=True)

# selected_date = st.select_slider(
#     '발매 기간 범위',
#     options=date_range,
#     value=(date_range[-48], date_range[-1])  # 기본값 설정: 4개월 전부터 현재까지
# )

# def yyyymm_to_date(yyyymm):
#     return datetime.strptime(yyyymm, "%Y%m")

# # 슬라이더에서 선택된 값 변환 함수
# def yyyymm_to_last_date(yyyymm):
#     # YYYYMM 형식의 문자열을 연도와 월로 분리
#     year = int(yyyymm[:4])
#     month = int(yyyymm[4:])
    
#     # 해당 연도와 월의 말일을 계산
#     last_day = calendar.monthrange(year, month)[1]
    
#     # 말일로 datetime 객체 생성
#     return datetime(year, month, last_day)

# # 선택된 값을 날짜로 변환
# start_date = yyyymm_to_date(selected_date[0])
# end_date = yyyymm_to_date(selected_date[1])

# start_last_date = yyyymm_to_last_date(selected_date[0])
# start_last_format = start_last_date.strftime("%Y%m%d")
# end_last_date = yyyymm_to_last_date(selected_date[1])
# end_last_format = end_last_date.strftime("%Y%m%d")
# st.write("---")
# # 선택된 날짜 출력
# # st.write(f"검색 기간 : {start_date.strftime('%Y년 %m월')} ~ {end_date.strftime('%Y년 %m월')}")
# # st.write("")
# # 검색 함수들
# def search_by_artist_id(artist_ids_prompt):
#     url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
#     param = {
#         "artist_id": str(artist_ids_prompt),
#         "album_release_country": album_release_country,
#         "limit": 1000,
#         "sort": "SCORE",
#         "album_release_start_date": f'{start_last_format}',
#         "album_release_end_date": f'{end_last_format}',
#         "cnt": 50
#     }
#     param_json = json.dumps(param)
#     res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
#     json_data = res.json()
#     if len(json_data.get('songs',[])) >= 1:
#         data_info = info(json_data)
#         score_info = evaluate(json_data)
#         display_sample_results(data_info)
#         display_score_result(score_info)
#     else:
#         st.warning("찾으시는 아티스트가 없습니다. 다시 입력해주세요.")

# def search_by_song_id(song_ids_prompt):
#     url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
#     param = {
#         "song_id": str(song_ids_prompt),
#         "album_release_country": album_release_country,
#         "limit": 1000,
#         "sort": "SCORE",
#         "album_release_start_date": f'{start_last_format}',
#         "album_release_end_date": f'{end_last_format}',
#         "cnt": 50
#     }
#     param_json = json.dumps(param)
#     res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
#     json_data = res.json()
#     if len(json_data.get('songs',[])) >= 1:
#         data_info = info(json_data)
#         score_info = evaluate(json_data)
#         display_sample_results(data_info)
#         display_score_result(score_info)
#     else:
#         st.warning("찾으시는 음악이 없습니다. 다시 입력해주세요.")

# def search(prompt):
#     url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/songs"
#     param = {
#         "prompt": prompt,
#         "album_release_country": album_release_country,
#         "limit": 1000,
#         "sort": "POPULAR",
#         "album_release_start_date": f'{start_last_format}',
#         "album_release_end_date": f'{end_last_format}',
#         "cnt": 50
#     }
#     param_json = json.dumps(param)
#     res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
#     json_data = res.json()
#     if len(json_data.get('songs',[])) >= 1:
#         data_info = info(json_data)
#         score_info = evaluate(json_data)
#         display_sample_results(data_info)
#         display_score_result(score_info)
#     else:
#         st.warning("음악을 못 찾았습니다. 다시 입력해주세요.")
    
# def info(res_json):
#     info = res_json["songs"]
#     url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/song-info"
#     song_ids = ",".join([str(item["song_id"]) for item in info])
#     param = {"song_id": song_ids}
#     param_json = json.dumps(param)
#     res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
#     return res.json()

# def evaluate(res_json):
#     info = res_json["songs"]
#     url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/evaluate/consistency"
#     song_ids = ",".join([str(item["song_id"]) for item in info])
#     param = {"song_id": song_ids, "mode":"dark"}
#     param_json = json.dumps(param)
#     res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
#     return res.json()

# def display_score_result(score_info):
#     info = score_info['score']
#     image_data = info['radial_image']
#     display_image(image_data)

# # 이미지 디코딩 및 표시
# def display_image(base64_str):
#     st.write("")
#     st.write("")
#     img_data = base64.b64decode(base64_str)
#     img = Image.open(BytesIO(img_data))
#     cols = st.columns([1, 2, 1])  # 좌우 여백의 비율을 조정 (1:2:1)
#     with cols[1]:  # 중간 열에 이미지를 배치
#         st.image(img, caption="", use_column_width=True)
#         st.markdown("""<div style="text-align: center;">데이터 일관성</div>""",unsafe_allow_html=True)
#         st.write("---")

# # 곡 리스트에서 샘플을 보여주는 함수 (로컬 이미지 추가)
# def display_sample_results(data_info):
#     datas = data_info['songs']
#     for song in datas[:8]:  # 리스트 8개만 출력
#         song_id = song['song_id']
#         song_name = song['song_name']
#         artist_name = song['artist_name']
#         st.markdown(f"""
#             <div style='text-align: center; background-color: rgba(20, 20, 20, 0.35); padding: 2px 10px; border-radius: 0px; width: 100%;'>
#                 <a href='https://genie.co.kr/detail/songInfo?xgnm={song_id}' style='color: white; text-decoration: none; font-size: 15px; padding: 10px 20px; display: inline-block; border-radius: 0px; width: 100%; box-sizing: border-box;'> 
#                     <span style='font-size: 14px;'>[ ▶️</span> 재생 ] {song_name} - {artist_name} 
#                 </a>
#             </div>
#         """, unsafe_allow_html=True)

# # 아티스트 검색 API 호출 함수
# def search_api(query, mode="songs"):
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
        
#         if mode == "songs":
#             # 곡 이름과 ID 추출
#             song_list = [
#                 {
#                     "name": f"{song["song_name"].get("original", "Unknown Song")} - {song["artist_name"].get("original", "Unknown Song"),}",
#                     "id": song.get("song_id", None)
#                 }
#                 for song in data.get('searchResult', {}).get('result', {}).get(mode, {}).get('items', [])
#             ]
#             song_names = [song["name"].replace('(\'', '').replace('\',)', '') for song in song_list]
#             song_ids = [song["id"] for song in song_list]
#             return song_names, song_ids

#         else:
#             # 아티스트 이름과 ID 추출
#             artist_list = [
#                 {
#                     "name": artist["artist_name"].get("original", "Unknown Artist"),
#                     "id": artist.get("artist_id", None)
#                 }
#                 for artist in data.get('searchResult', {}).get('result', {}).get(mode, {}).get('items', [])
#             ]
#             artist_names = [artist["name"] for artist in artist_list]
#             artist_ids = [artist["id"] for artist in artist_list]
#             return artist_names, artist_ids

#     except requests.exceptions.RequestException as e:
#         st.error(f"API 요청 중 오류 발생: {e}")
#         return [], []

# # -------------------------------------------------------------

# st.image(title_01_img, caption='', use_column_width=True)
# # Prompt 입력과 버튼 (st.expander 사용)
# with st.expander("프롬프트 입력", expanded=True):
#     prompt = st.text_area("무슨 노래가 듣고 싶어요?")
    
#     # 텍스트 입력창과 버튼을 같은 너비로 하기 위해 컨테이너 사용
#     with st.container():
#         search_button_clicked = st.button("프롬프트 검색", use_container_width=True)
    
#     if search_button_clicked:
#         with st.spinner('AI가 플레이리스트를 만드는 중입니다...'):
#             search(prompt)

# st.image(title_02_img, caption='', use_column_width=True)

# st.markdown("""
#     <style>
#     .stSelectbox > div:first-child {
#         background-color: #1E90FF !important;  /* 파란색 배경 */
#         color: white !important;  /* 흰색 텍스트 */
#         border: 2px solid #1E90FF !important;  /* 파란색 테두리 */
#         padding: 5px 10px;
#         border-radius: 10px;
#         font-size: 16px;
#         font-weight: bold;
#     }
#     .stSelectbox:hover > div:first-child {
#         background-color: #4169E1 !important;  /* Hover 시 더 진한 파란색 */
#         border-color: #4169E1 !important;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # 유사 곡 검색
# with st.expander("유사 곡 검색"):
#     # 곡 이름 입력과 동시에 검색 및 선택 가능한 통합 입력창
#     query = st.text_input("곡 이름을 입력하세요", help="곡 이름을 입력하고 검색 결과에서 선택하세요")

#     # 초기값으로 None 할당
#     selected_song_name = None
#     selected_song_id = None

#     if query:
#         song_names, song_ids = search_api(query, 'songs')  # API 호출을 통해 곡 이름과 ID 검색
        
#         if song_names:
#             # 선택 창을 통해 입력한 이름과 검색 결과를 모두 표시
#             selected_song_name = st.selectbox("조회된 곡 선택", song_names, index=0)

#             if selected_song_name:
#                 selected_song_index = song_names.index(selected_song_name)
#                 selected_song_id = str(song_ids[selected_song_index])

#     if selected_song_name and selected_song_id:
#         with st.spinner(f'AI가 동작 중입니다..'):
#             search_by_song_id(selected_song_id)


# st.image(title_03_img, caption='', use_column_width=True)

# # 유사 아티스트 검색
# with st.expander("유사 아티스트 검색"):
#     query = st.text_input("아티스트 이름을 입력하세요")
    
#     # 초기값으로 None 할당
#     selected_artist_name = None
#     selected_artist_id = None
    
#     if query:
#         artist_names, artist_ids = search_api(query, 'artists')
        
#         if artist_names:
#             selected_artist_name = st.selectbox("조회된 아티스트", artist_names)
            
#             if selected_artist_name:
#                 selected_artist_index = artist_names.index(selected_artist_name)
#                 selected_artist_id = artist_ids[selected_artist_index]
    
#     if selected_artist_name and selected_artist_id:
#         with st.spinner(f'AI가 동작 중입니다..'):
#             search_by_artist_id(selected_artist_id)