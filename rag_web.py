import streamlit as st
import os
import base64
import json
import requests
from datetime import datetime, timedelta
import uuid

# 로컬 이미지 경로 설정
box_img_path = os.path.join(os.getcwd(), "box_01.png")
play_btn_img_path = os.path.join(os.getcwd(), "playbtn_img.webp")
background_img_path = os.path.join(os.getcwd(), "background.jpg")

# Base64로 로컬 이미지 인코딩
with open(box_img_path, "rb") as img_file:
    box_img_base64 = base64.b64encode(img_file.read()).decode()

# Base64로 로컬 이미지 인코딩
with open(play_btn_img_path, "rb") as img_file:
    play_btn_img_base64 = base64.b64encode(img_file.read()).decode()

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
}}
</style>
'''

# 이미지가 적용된 전체 프롬프트 영역 CSS (배경을 더 크게 설정)
view_style = f'''
<style>
.view-container {{
  background-image: url("data:image/png;base64,{box_img_base64}");
  background-size: 100% 100%;  /* 배경 크기를 전체 영역으로 확장 */
  background-position: center;
  background-repeat: no-repeat;
  padding: 50px;  /* 영역을 넓히기 위해 패딩을 증가 */
  border-radius: 10px;
  width: 100%;  /* 컨테이너가 화면 너비를 채우도록 설정 */
  margin-bottom: 20px;  /* 다른 요소와의 간격 추가 */
}}
</style>
'''

# 배경 이미지 적용
st.markdown(view_style, unsafe_allow_html=True)
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# -------------------------------------------------------------

# 레이아웃 시작
st.title("AI 큐레이션 TF")

# 현재 날짜와 과거 날짜 설정
day_number = 365
current_date = datetime.now()  # 최대값 (오늘)
past_date = current_date - timedelta(days=day_number)  # 최소값

# 숫자 -> 날짜 변환 함수
def int_to_date(days_from_today):
    return current_date + timedelta(days=days_from_today)

# 슬라이더 초기 값 및 키 값 설정
key = 1
slider_place_holder = st.empty()

# 슬라이더 생성
initial_slider_value = -90  # 기본값을 현재 날짜로 설정
my_slider = slider_place_holder.slider(
    "",
    min_value=-day_number,
    max_value=0,
    value=initial_slider_value,
    key=key
)

# 선택된 값을 날짜로 변환
selected_date = int_to_date(my_slider)

# 선택된 날짜 출력
st.write(f"{selected_date.strftime('%Y%m%d')} ~ {current_date.strftime('%Y%m%d')}")

# -------------------------------------------------------------
# 프롬프트 입력 및 검색 버튼을 "View"에 포함

# View 컨테이너 생성 (배경 이미지 적용)
st.markdown('<div class="view-container">', unsafe_allow_html=True)

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

# "View" 역할을 하는 div 닫기
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------

# 나머지 기능은 이전과 동일
def search(prompt):
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/songs"
    param = {
        "prompt": prompt,
        "album_release_country": "KOREA",
        "limit": 200,
        "voice_yn": "Y",
        "sort": "POPULAR",
        "album_release_start_date": f'{selected_date.strftime("%Y%m%d")}',
        "album_release_end_date": f'{current_date.strftime("%Y%m%d")}',
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

# 곡 리스트에서 샘플을 보여주는 함수
def display_sample_results(data_info):
    datas = data_info['songs']
    for song in datas[:5]:
        song_id = song['song_id']
        song_name = song['song_name']
        artist_name = song['artist_name']
        button_key = str(uuid.uuid4())

        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"{song_name} - {artist_name}  [상세정보](https://genie.co.kr/detail/songInfo?xgnm={song_id})")
        
        with col2:
            play_button_html = f"""
            <div style='text-align: center;'>
                <button style="border:none;background-color:transparent;cursor:pointer;padding:5px;margin:0;">
                    <img src="data:image/webp;base64,{play_btn_img_base64}" width="30" height="30" />
                </button>
            </div>
            """
            st.markdown(play_button_html, unsafe_allow_html=True)

            if st.button(f"재생", key=f"play_{button_key}"):
                st.write(f"재생 버튼이 클릭되었습니다! Song ID: {song_id}")

# -------------------------------------------------------------

# 재생바를 보여주는 함수
def show_playing_bar():
    if st.session_state.playing_song_id and st.session_state.playing_song_url:
        st.markdown(f'''
        <div class="floating-player">
            🎵 재생 중: {st.session_state.playing_song_name} - {st.session_state.playing_artist_name}
            <br>
            <audio controls autoplay>
                <source src="{st.session_state.playing_song_url}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </div>
        ''', unsafe_allow_html=True)

show_playing_bar()
