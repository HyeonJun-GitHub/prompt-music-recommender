import streamlit as st
import json
import requests

# 상단과 하단의 Streamlit 기본 UI 제거를 위한 CSS
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

# 배경 이미지 설정을 위한 CSS
page_bg_img = '''
<style>
.stApp {
  background-image: url("https://image.genie.co.kr/Y/IMAGE/IMG_ALBUM/085/534/622/85534622_1724394868251_1_600x600.JPG/dims/resize/Q_80,0");
  background-size: cover;
  background-position: center;
}
</style>
'''

input_box_style = '''
<style>
textarea, input {
  background-color: white !important;
  color: black !important;
}
</style>
'''

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(input_box_style, unsafe_allow_html=True)

# 임시 데이터 (나중에 API를 통해 대체 가능)
sample_songs = [
    {"id": 1, "artist": "Artist A", "title": "Song A", "score": 90},
    {"id": 2, "artist": "Artist B", "title": "Song B", "score": 85},
    {"id": 3, "artist": "Artist C", "title": "Song C", "score": 80},
    {"id": 4, "artist": "Artist D", "title": "Song D", "score": 75},
    {"id": 5, "artist": "Artist E", "title": "Song E", "score": 88},
]

# 검색 함수들
def search_by_artist_id():
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
    param = {
        "artist_id":artist_ids_prompt,
        "album_release_country":"KOREA",
        "limit":200,
        "voice_yn":"Y",
        "sort":"SCORE",
        "cnt":50
    }
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type':'application/json'})
    json_data = res.json()
    data_info = info(json_data)
    display_sample_results(data_info)

def search_by_song_id():
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
    param = {
        "song_id":song_ids_prompt,
        "album_release_country":"KOREA",
        "limit":200,
        "voice_yn":"Y",
        "sort":"SCORE",
        "cnt":50
    }
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type':'application/json'})
    json_data = res.json()
    data_info = info(json_data)
    display_sample_results(data_info)

def search():
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/songs"
    param = {
        "prompt":prompt,
        "album_release_country":"KOREA",
        "limit":200,
        "voice_yn":"Y",
        "sort":"POPULAR",
        "cnt":50
    }
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type':'application/json'})
    json_data = res.json()
    data_info = info(json_data)
    display_sample_results(data_info)

def info(res_json):
    info = res_json["songs"]
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/song-info"
    song_ids = ",".join([str(item["song_id"]) for item in info])
    param = {"song_id":song_ids}
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type':'application/json'})
    return res.json()

def display_sample_results(data_info): 
    datas = data_info['songs']
    for song in datas[:5]:  # 리스트 5개만 출력
        st.markdown(f"{song['song_name']} - {song['artist_name']}  [상세정보](https://genie.co.kr/detail/songInfo?xgnm={song['song_id']})")
        # st.markdown(f"**{song['song_id']} : {song['artist_name']} - {song['song_name']} [상세정보](https://genie.co.kr/detail/songInfo?xgnm={song['song_id']})")

import streamlit as st
from datetime import datetime, timedelta

# 현재 날짜
current_date = datetime.now()

# 과거 날짜 (예: 30일 전)
past_date = current_date - timedelta(days=30)

# 슬라이더에 사용할 형식 (yyyymmdd)
def format_date(date):
    return date.strftime("%Y%m%d")

# 슬라이더 값 설정 (초기값을 None으로 설정하여 기본값이 자동으로 설정되지 않도록)
selected_date = st.slider(
    "날짜 선택",
    min_value=past_date,
    max_value=current_date,
    value=st.session_state.get('selected_date', current_date),  # 사용자가 선택한 날짜를 저장
    format="YYYY-MM-DD"
)

# 선택된 날짜를 session_state에 저장하여 계속 유지
st.session_state['selected_date'] = selected_date

# 선택된 날짜 출력
st.write(f"선택된 날짜: {format_date(selected_date)}")

# Prompt 입력과 버튼
st.subheader("프롬프트")
col1, col2 = st.columns([3, 1])
with col1:
    prompt = st.text_area("무슨 노래가 듣고 싶어요?")
with col2:
    spacer = st.empty()  # 빈 공간 추가
    spacer.write("")
    search_button_clicked = st.button("프롬프트 검색")

# Prompt 결과 표시 (버튼이 눌렸을 때만 결과 표시)
if search_button_clicked:
    search()

# Song ID 입력과 버튼
st.subheader("유사 곡 검색")
col3, col4 = st.columns([3, 1])
with col3:
    song_ids_prompt = st.text_input("예 : 92749701 (라일락)")
with col4:
    spacer = st.empty()  # 빈 공간 추가
    spacer.write("")
    spacer.write("")
    song_search_button_clicked = st.button("곡 검색")

# Song ID 검색 결과 표시 (버튼이 눌렸을 때만 결과 표시)
if song_search_button_clicked:
    search_by_song_id()

# Artist ID 입력과 버튼
st.subheader("유사 아티스트 검색")
col5, col6 = st.columns([3, 1])
with col5:
    artist_ids_prompt = st.text_input("예 : 67872918 (아이유)")
with col6:
    spacer = st.empty()  # 빈 공간 추가
    spacer.write("")
    spacer.write("")
    artist_search_button_clicked = st.button("아티스트 검색")

# Artist ID 검색 결과 표시 (버튼이 눌렸을 때만 결과 표시)
if artist_search_button_clicked:
    search_by_artist_id()
