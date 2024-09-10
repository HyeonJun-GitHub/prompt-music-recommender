import streamlit as st
import json
import uuid
from datetime import datetime, timedelta
import os
import base64

# 로컬 이미지 경로 설정
box_img_path = os.path.join(os.getcwd(), "box_01.png")
play_btn_img_path = os.path.join(os.getcwd(), "playbtn_img.webp")
background_img_path = os.path.join(os.getcwd(), "background.jpg")

# Base64로 로컬 이미지 인코딩
with open(box_img_path, "rb") as img_file:
    box_img_base64 = base64.b64encode(img_file.read()).decode()

with open(play_btn_img_path, "rb") as img_file:
    play_btn_img_base64 = base64.b64encode(img_file.read()).decode()

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

# 하드코딩된 URL을 반환하는 함수
def get_downloadurl(song_id):
    # 하드코딩된 재생 가능한 MP3 URL 반환
    # return "http://www.noiseaddicts.com/samples_1w72b820/4261.mp3"
    return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

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
  background-image: url("data:image/png;base64,{box_img_base64}"), url("data:image/jpg;base64,{background_img_base64}");
  background-size: calc(100% - 40px) 500px, cover;
  background-position: left 10px top 380px,center;
  background-repeat: no-repeat, no-repeat;
}}
</style>
'''

# 배경 이미지 적용
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 레이아웃 시작
st.title("AI 큐레이션 TF")

# 현재 날짜와 과거 날짜 설정
day_number = 365
current_date = datetime.now()
past_date = current_date - timedelta(days=day_number)

# 숫자 -> 날짜 변환 함수
def int_to_date(days_from_today):
    return current_date + timedelta(days=days_from_today)

# 슬라이더 생성 (기본값 설정)
initial_slider_value = -90
my_slider = st.slider(
    "",
    min_value=-day_number,
    max_value=0,
    value=initial_slider_value
)

selected_date = int_to_date(my_slider)
st.write(f"{selected_date.strftime('%Y%m%d')} ~ {current_date.strftime('%Y%m%d')}")

# 샘플 곡 리스트에서 결과를 표시하는 함수
def display_sample_results():
    sample_songs = [
        {"song_id": "87443133", "song_name": "가을 아침", "artist_name": "아이유"},
        {"song_id": "23456789", "song_name": "블루밍", "artist_name": "아이유"},
        {"song_id": "34567890", "song_name": "라일락", "artist_name": "아이유"},
        {"song_id": "45678901", "song_name": "너랑 나", "artist_name": "아이유"},
        {"song_id": "56789012", "song_name": "밤편지", "artist_name": "아이유"},
    ]

    for song in sample_songs:
        song_id = song['song_id']
        song_name = song['song_name']
        artist_name = song['artist_name']

        # UUID를 이용해 고유한 버튼 키 생성
        button_key = str(uuid.uuid4())

        # 상세정보와 Play 버튼을 같은 줄에 배치
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"{song_name} - {artist_name}")
        
        with col2:
            # Streamlit 버튼을 이용한 곡 재생 기능
            if st.button(f"Play {song_name}", key=f"play_{button_key}"):
                st.write(f"재생 버튼이 클릭되었습니다! Song ID: {song_id}")
                st.session_state.playing_song_id = song_id
                st.session_state.playing_song_name = song_name
                st.session_state.playing_artist_name = artist_name
                st.session_state.playing_song_url = get_downloadurl(song_id)

# 샘플 결과 표시
display_sample_results()

# Streamlit의 st.audio를 사용한 오디오 재생
if st.session_state.playing_song_url:
    mp3_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    st.audio(mp3_url, format="audio/mp3", start_time=0)
else:
    st.write("재생할 곡을 선택하세요.")
