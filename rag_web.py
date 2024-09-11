import streamlit as st
import json
import requests
from datetime import datetime, timedelta
import os
import base64
from PIL import Image
import streamlit.components.v1 as components
import calendar

st.set_page_config(layout="wide")

# 로컬 이미지 경로 설정
# 리소스 디렉토리 경로 설정
title_01_path = os.path.join(os.getcwd(), "title_01.png")
box_img_path = os.path.join(os.getcwd(), "box_01.png")
background_img_path = os.path.join(os.getcwd(), "background.jpg")

title_01_img = Image.open(title_01_path)
background_img = Image.open(background_img_path)

# Base64로 로컬 이미지 인코딩
with open(box_img_path, "rb") as img_file:
    box_img_base64 = base64.b64encode(img_file.read()).decode()

# Base64로 로컬 이미지 인코딩 (배경 이미지)
with open(background_img_path, "rb") as img_file:
    background_img_base64 = base64.b64encode(img_file.read()).decode()

# 상태 저장을 위한 session_state 사용
if 'playing_song_id' not in st.session_state:
    st.session_state.playing_song_id = None
if 'playing_song_name' not in st.session_state:
    st.session_state.playing_song_name = None
if 'playing_artist_name' not in st.session_state:
    st.session_state.playing_artist_name = None
if 'playing_song_url' not in st.session_state:
    st.session_state.playing_song_url = None

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
}
</style>
"""

# 배경 이미지 적용
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(text_area_style, unsafe_allow_html=True)  # 텍스트 입력창 스타일 적용

# -------------------------------------------------------------

# 레이아웃 시작
st.title("AI 큐레이션 TF")

# 현재 날짜와 과거 날짜 설정
day_number = 365
current_date = datetime.now()  # 최대값 (오늘)
past_date = current_date - timedelta(days=day_number)  # 최소값
date_range = [(past_date + timedelta(days=x)).strftime('%Y%m') for x in range(0, 366, 30)]  # 매월 1회씩

st.markdown("""
    <style>
    /* 슬라이더 바 색상 */
    .streamlit-slider > div[data-baseweb="slider"] > div {
        background: linear-gradient(to right, #1E90FF, #87CEEB); /* 파란색 그라데이션 */
    }
    /* 슬라이더 핸들 색상 */
    .streamlit-slider > div[data-baseweb="slider"] > div > div > div {
        background-color: #1E90FF; /* 슬라이더 핸들 파란색 */
    }
    </style>
    """, unsafe_allow_html=True)

selected_date = st.select_slider(
    '검색하는 발매 기간을 선택하세요.',
    options=date_range,
    value=(date_range[-4], date_range[-1])  # 기본값 설정: 4개월 전부터 현재까지
)

def yyyymm_to_date(yyyymm):
    return datetime.strptime(yyyymm, "%Y%m")

# 슬라이더에서 선택된 값 변환 함수
def yyyymm_to_last_date(yyyymm):
    # YYYYMM 형식의 문자열을 연도와 월로 분리
    year = int(yyyymm[:4])
    month = int(yyyymm[4:])
    
    # 해당 연도와 월의 말일을 계산
    last_day = calendar.monthrange(year, month)[1]
    
    # 말일로 datetime 객체 생성
    return datetime(year, month, last_day)


# 선택된 값을 날짜로 변환
start_date = yyyymm_to_date(selected_date[0])
end_date = yyyymm_to_date(selected_date[1])

start_last_date = yyyymm_to_last_date(selected_date[0])
start_last_format = start_last_date.strftime("%Y%m%d")
end_last_date = yyyymm_to_last_date(selected_date[1])
end_last_format = end_last_date.strftime("%Y%m%d")

# 선택된 날짜 출력
st.write(f"검색 기간 : {start_date.strftime('%Y년 %m월')} ~ {end_date.strftime('%Y년 %m월')}")
st.write("")
# 검색 함수들
def search_by_artist_id(artist_ids_prompt):
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
    param = {
        "artist_id": artist_ids_prompt,
        "album_release_country": "KOREA",
        "limit": 200,
        "voice_yn": "Y",
        "sort": "SCORE",
        "album_release_start_date": f'{start_last_format}',
        "album_release_end_date": f'{end_last_format}',
        "cnt": 50
    }
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
    json_data = res.json()
    data_info = info(json_data)
    display_sample_results(data_info)

def search_by_song_id(song_ids_prompt):
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
    param = {
        "song_id": song_ids_prompt,
        "album_release_country": "KOREA",
        "limit": 200,
        "voice_yn": "Y",
        "sort": "SCORE",
        "album_release_start_date": f'{start_last_format}',
        "album_release_end_date": f'{end_last_format}',
        "cnt": 50
    }
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
    json_data = res.json()
    data_info = info(json_data)
    display_sample_results(data_info)

def search(prompt):
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/songs"
    param = {
        "prompt": prompt,
        "album_release_country": "KOREA",
        "limit": 200,
        "voice_yn": "Y",
        "sort": "POPULAR",
        "album_release_start_date": f'{start_last_format}',
        "album_release_end_date": f'{end_last_format}',
        "cnt": 50
    }
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
    json_data = res.json()
    data_info = info(json_data)
    display_sample_results(data_info)

def info(res_json):
    info = res_json["songs"]
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/song-info"
    song_ids = ",".join([str(item["song_id"]) for item in info])
    param = {"song_id": song_ids}
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
    return res.json()

# 곡 다운로드 URL을 가져오는 함수
def get_downloadurl(song_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    }
    download_url = f'https://stage-apis.genie.co.kr/api/v1/tracks/juice/{song_id}?protocolType=http&bitRate=192'
    res = requests.post(download_url, headers=headers)
    
    # 디버깅용 로그 출력
    st.write(f"API 호출 결과 상태 코드: {res.status_code}")
    
    if res.status_code == 200:
        st.write(f"다운로드 URL: {download_url}")  # URL을 출력하여 확인
        return download_url
    else:
        st.write("다운로드 URL을 가져오지 못했습니다.")  # 실패 시 출력
        return None

# 곡 리스트에서 샘플을 보여주는 함수 (로컬 이미지 추가)
def display_sample_results(data_info):
    datas = data_info['songs']
    for song in datas[:10]:  # 리스트 5개만 출력
        song_id = song['song_id']
        song_name = song['song_name']
        artist_name = song['artist_name']
        st.markdown(f"{song_name} - {artist_name} [상세정보](https://genie.co.kr/detail/songInfo?xgnm={song_id})")

# -------------------------------------------------------------

spacer_height = "<div style='height: 28px;'></div>"
st.image(title_01_img, caption='', use_column_width=True)
# Prompt 입력과 버튼 (st.expander 사용)
with st.expander("프롬프트 입력", expanded=True):
    prompt = st.text_area("무슨 노래가 듣고 싶어요?")
    
    # 텍스트 입력창과 버튼을 같은 너비로 하기 위해 컨테이너 사용
    with st.container():
        search_button_clicked = st.button("프롬프트 검색", use_container_width=True)
    
    if search_button_clicked:
        with st.spinner('AI가 플레이리스트를 만드는 중입니다...'):
            search(prompt)

# 곡 ID 검색 (st.expander 사용)
with st.expander("유사 곡 검색"):
    song_ids_prompt = st.text_input("곡 ID를 입력하세요 (예: 87443133 [아이유 - 가을 아침])")
    
    # 텍스트 입력창과 버튼을 같은 너비로 하기 위해 컨테이너 사용
    with st.container():
        song_search_button_clicked = st.button("곡 검색", use_container_width=True)
    
    if song_search_button_clicked:
        with st.spinner('AI가 플레이리스트를 만드는 중입니다...'):
            search_by_song_id(song_ids_prompt)

# 아티스트 ID 검색 (st.expander 사용)
with st.expander("유사 아티스트 검색"):
    artist_ids_prompt = st.text_input("아티스트 ID를 입력하세요 (예: 67872918 [아이유])")
    
    # 텍스트 입력창과 버튼을 같은 너비로 하기 위해 컨테이너 사용
    with st.container():
        artist_search_button_clicked = st.button("아티스트 검색", use_container_width=True)
    
    if artist_search_button_clicked:
        with st.spinner('AI가 플레이리스트를 만드는 중입니다...'):
            search_by_artist_id(artist_ids_prompt)
