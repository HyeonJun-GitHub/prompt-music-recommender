import streamlit as st
import json
import requests
from datetime import datetime, timedelta
import uuid  # UUID를 생성하기 위한 모듈
import os
import base64

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
  background-image: url("data:image/png;base64,{box_img_base64}"), url("data:image/jpg;base64,{background_img_base64}");
  background-size: cover, contain;  /* 첫 번째 이미지는 cover, 두 번째 이미지는 contain */
  background-position: center, right 400px top 500px;  /* 첫 번째 이미지는 중앙, 두 번째 이미지는 우측 상단 */
  background-repeat: no-repeat, no-repeat;  /* 둘 다 반복 없음 */
  background-origin: padding-box;  /* 배경 이미지를 패딩 영역부터 시작 */
  padding: 0px, 200px;  /* 패딩을 설정하여 배경 이미지가 이 안에서 표시되도록 */
}}
</style>
'''

# 플로팅 재생바를 위한 CSS
floating_player_style = '''
<style>
.floating-player {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  text-align: center;
  padding: 10px;
  z-index: 9999;
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

# 오버레이 스타일 정의 (배경 이미지를 포함)
overlay_style = f'''
<style>
.overlay-container {{
  position: relative;
  width: 100%;
  height: auto;
  background-image: url("data:image/png;base64,{box_img_base64}");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 50px;
  border-radius: 10px;
  display: block;
}}

.overlay-content {{
  background: rgba(255, 255, 255, 0.8);  /* 반투명 배경 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);  /* 그림자 */
  width: 100%;
  max-width: 800px;  /* 최대 너비 */
  margin: 0 auto;  /* 가운데 정렬 */
}}
</style>
'''

# 배경 이미지 적용
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(floating_player_style, unsafe_allow_html=True)

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

# 검색 함수들
def search_by_artist_id(artist_ids_prompt):
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
    param = {
        "artist_id": artist_ids_prompt,
        "album_release_country": "KOREA",
        "limit": 200,
        "voice_yn": "Y",
        "sort": "SCORE",
        "album_release_start_date": f'{selected_date.strftime("%Y%m%d")}',
        "album_release_end_date": f'{current_date.strftime("%Y%m%d")}',
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
        "album_release_start_date": f'{selected_date.strftime("%Y%m%d")}',
        "album_release_end_date": f'{current_date.strftime("%Y%m%d")}',
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
    for song in datas[:5]:  # 리스트 5개만 출력
        song_id = song['song_id']
        song_name = song['song_name']
        artist_name = song['artist_name']

        # UUID를 이용해 고유한 버튼 키 생성
        button_key = str(uuid.uuid4())

        # 상세정보와 Play 버튼을 같은 줄에 배치
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"{song_name} - {artist_name}  [상세정보](https://genie.co.kr/detail/songInfo?xgnm={song_id})")
        
        with col2:
            # 이미지 아이콘을 추가한 재생 버튼 생성 (크기를 줄임)
            play_button_html = f"""
            <div style='text-align: center;'>
                <button style="border:none;background-color:transparent;cursor:pointer;padding:5px;margin:0;">
                    <img src="data:image/webp;base64,{play_btn_img_base64}" width="30" height="30" />
                </button>
            </div>
            """
            st.markdown(play_button_html, unsafe_allow_html=True)

            if st.button(f"재생", key=f"play_{button_key}"):
                st.write(f"재생 버튼이 클릭되었습니다! Song ID: {song_id}")  # 디버깅용 로그
                # st.session_state.playing_song_id = song_id
                # st.session_state.playing_song_name = song_name
                # st.session_state.playing_artist_name = artist_name
                # st.session_state.playing_song_url = get_downloadurl(song_id)


# -------------------------------------------------------------

# Prompt 입력과 버튼
st.markdown(input_box_style, unsafe_allow_html=True)

# CSS 스타일 적용
st.markdown(overlay_style, unsafe_allow_html=True)

# 오버레이 컨테이너 시작
st.markdown('<div class="overlay-container">', unsafe_allow_html=True)

# 오버레이 컨텐츠 (위젯 포함)
st.markdown('<div class="overlay-content">', unsafe_allow_html=True)


st.subheader("프롬프트")
col1, col2 = st.columns([3, 1])
with col1:
    prompt = st.text_area("무슨 노래가 듣고 싶어요?")
with col2:
    spacer = st.empty()  # 빈 공간 추가
    spacer.write("")
    search_button_clicked = st.button("프롬프트 검색")

st.markdown('</div>', unsafe_allow_html=True)

# 오버레이 컨테이너 종료
st.markdown('</div>', unsafe_allow_html=True)


# Prompt 결과 표시 (버튼이 눌렸을 때만 결과 표시)
if search_button_clicked:
    search(prompt)

# Song ID 입력과 버튼
st.subheader("유사 곡 검색")
col3, col4 = st.columns([3, 1])
with col3:
    song_ids_prompt = st.text_input("예) 87443133 [아이유 - 가을 아침]")
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
    artist_ids_prompt = st.text_input("예) 67872918 [아이유]")
with col6:
    spacer = st.empty()  # 빈 공간 추가
    spacer.write("")
    spacer.write("")
    artist_search_button_clicked = st.button("아티스트 검색")

# Artist ID 검색 결과 표시 (버튼이 눌렸을 때만 결과 표시)
if artist_search_button_clicked:
    search_by_artist_id(artist_ids_prompt)

# 재생 중인 곡이 있을 때 하단에 고정된 재생바 출력
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
