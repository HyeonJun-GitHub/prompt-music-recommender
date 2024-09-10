import streamlit as st
import json
from datetime import datetime, timedelta

# 상태 저장을 위한 session_state 사용
if 'playing_song_id' not in st.session_state:
    st.session_state.playing_song_id = None
if 'playing_song_name' not in st.session_state:
    st.session_state.playing_song_name = None

# 상단과 하단의 Streamlit 기본 UI 제거를 위한 CSS
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
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

# 슬라이더 초기 값 및 키 값 설정
key = 1
slider_place_holder = st.empty()

# 슬라이더 생성
initial_slider_value = -90
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

# 박스 스타일 적용 (CSS)
box_style = """
    <style>
    .box {
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
    }
    </style>
    """
st.markdown(box_style, unsafe_allow_html=True)

# 프롬프트 입력 박스
st.markdown('<div class="box">', unsafe_allow_html=True)
st.subheader("프롬프트")
col1, col2 = st.columns([3, 1])
with col1:
    prompt = st.text_area("무슨 노래가 듣고 싶어요?")
with col2:
    spacer = st.empty()
    search_button_clicked = st.button("프롬프트 검색")

if search_button_clicked:
    st.write(f"Searching for: {prompt}")  # 검색 결과를 출력 (예시)
st.markdown('</div>', unsafe_allow_html=True)

# 유사 곡 검색 박스
st.markdown('<div class="box">', unsafe_allow_html=True)
st.subheader("유사 곡 검색")
col3, col4 = st.columns([3, 1])
with col3:
    song_ids_prompt = st.text_input("예) 87443133 [아이유 - 가을 아침]")
with col4:
    spacer = st.empty()
    song_search_button_clicked = st.button("곡 검색")

if song_search_button_clicked:
    st.write(f"Searching for song ID: {song_ids_prompt}")  # 검색 결과를 출력 (예시)
st.markdown('</div>', unsafe_allow_html=True)

# 유사 아티스트 검색 박스
st.markdown('<div class="box">', unsafe_allow_html=True)
st.subheader("유사 아티스트 검색")
col5, col6 = st.columns([3, 1])
with col5:
    artist_ids_prompt = st.text_input("예) 67872918 [아이유]")
with col6:
    spacer = st.empty()
    artist_search_button_clicked = st.button("아티스트 검색")

if artist_search_button_clicked:
    st.write(f"Searching for artist ID: {artist_ids_prompt}")  # 검색 결과를 출력 (예시)
st.markdown('</div>', unsafe_allow_html=True)
