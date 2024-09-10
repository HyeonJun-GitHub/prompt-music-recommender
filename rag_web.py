import streamlit as st
import json
import requests
from datetime import datetime, timedelta

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

# -------------------------------------------------------------

# 레이아웃 시작
st.title("AI 큐레이션 TF")

# -------------------------------------------------------------

import streamlit as st
from datetime import datetime, timedelta

# 현재 날짜와 과거 날짜 설정
day_number = 365
current_date = datetime.now()  # 최대값 (오늘)
past_date = current_date - timedelta(days=day_number)  # 최소값 (30일 전)

# 숫자 -> 날짜 변환 함수
def int_to_date(days_from_today):
    return current_date + timedelta(days=days_from_today)

# 슬라이더 초기 값 및 키 값 설정
key = 1
slider_place_holder = st.empty()

# 슬라이더 생성 (min_value=-30, max_value=0으로 설정)
initial_slider_value = 0  # 기본값을 현재 날짜로 설정
my_slider = slider_place_holder.slider(
    "날짜 선택",
    min_value=-day_number,  # 슬라이더의 최소값은 -30 (과거 30일)
    max_value=0,  # 슬라이더의 최대값은 0 (오늘)
    value=initial_slider_value,  # 기본값을 오늘로 설정
    key=key
)

# 슬라이더 아래에 '과거'와 '현재' 레이블 추가
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("과거")
with col2:
    st.markdown("<div style='text-align: right'>현재</div>", unsafe_allow_html=True)

# 슬라이더 리셋 함수
def reset_all_sliders(reset_iteration):
    slider_place_holder.empty()  # 기존 슬라이더 지우기
    # 새 슬라이더를 다른 키로 다시 그리기 (이로 인해 슬라이더 값이 초기화됨)
    return slider_place_holder.slider(
        min_value=-day_number,  # 최소값을 -30 (과거 30일 전)
        max_value=0,  # 최대값을 0 (오늘)
        value=0,  # 기본값을 오늘로 리셋
        key=(key + reset_iteration)
    )

# 리셋 횟수 추적
reset_iteration = 1

# 슬라이더 값 변경 및 리셋 처리
if st.button('Reset to Default'):
    reset_iteration += 1
    st.write(f"슬라이더가 {reset_iteration}번째 리셋되었습니다.")
    my_slider = reset_all_sliders(reset_iteration)  # 슬라이더 리셋

# 선택된 값을 날짜로 변환 (-30일 ~ 0일을 실제 날짜로 변환)
selected_date = int_to_date(my_slider)

# 선택된 날짜 출력
st.write(f"선택된 날짜: {selected_date.strftime('%Y%m%d')}")

# -------------------------------------------------------------


# 검색 함수들
def search_by_artist_id(artist_ids_prompt):
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
    param = {
        "artist_id": artist_ids_prompt,
        "album_release_country": "KOREA",
        "limit": 200,
        "voice_yn": "Y",
        "sort": "SCORE",
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

def display_sample_results(data_info): 
    datas = data_info['songs']
    for song in datas[:5]:  # 리스트 5개만 출력
        st.markdown(f"{song['song_name']} - {song['artist_name']}  [상세정보](https://genie.co.kr/detail/songInfo?xgnm={song['song_id']})")

# -------------------------------------------------------------

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
    search(prompt)

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
    search_by_song_id(song_ids_prompt)

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
    search_by_artist_id(artist_ids_prompt)
