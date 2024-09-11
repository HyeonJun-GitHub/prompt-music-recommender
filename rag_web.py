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

# 국내/해외 세그먼트 선택

st.set_page_config(layout="wide",)

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

st.image(title_00_img, caption='', use_column_width=True)
# 레이아웃 시작
st.write("---")
st.title("검색 설정")
segment = st.radio("국가 선택", ("전체", "국내", "해외"))

album_release_country = ""
if segment == "전체":
    album_release_country = ""
elif segment == "국내":
    album_release_country = "KOREA"
elif segment == "해외":
    album_release_country = "POPULAR"

# 현재 날짜와 과거 날짜 설정
day_number = 365 * 5
current_date = datetime.now()  # 최대값 (오늘)
past_date = current_date - timedelta(days=day_number)  # 최소값
date_range = [(past_date + timedelta(days=x)).strftime('%Y%m') for x in range(0, day_number+1, 30)]  # 매월 1회씩

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
    '발매 기간 범위',
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
st.write("---")
# 선택된 날짜 출력
# st.write(f"검색 기간 : {start_date.strftime('%Y년 %m월')} ~ {end_date.strftime('%Y년 %m월')}")
# st.write("")
# 검색 함수들
def search_by_artist_id(artist_ids_prompt):
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
    param = {
        "artist_id": artist_ids_prompt,
        "album_release_country": album_release_country,
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
    if len(json_data.get('songs',[])) >= 1:
        data_info = info(json_data)
        score_info = evaluate(json_data)
        display_sample_results(data_info)
        display_score_result(score_info)
    else:
        st.warning("음악을 못 찾았습니다. 다시 입력해주세요.")

def search_by_song_id(song_ids_prompt):
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/similarity"
    param = {
        "song_id": song_ids_prompt,
        "album_release_country": album_release_country,
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
    if len(json_data.get('songs',[])) >= 1:
        data_info = info(json_data)
        score_info = evaluate(json_data)
        display_sample_results(data_info)
        display_score_result(score_info)
    else:
        st.warning("음악을 못 찾았습니다. 다시 입력해주세요.")

def search(prompt):
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/songs"
    param = {
        "prompt": prompt,
        "album_release_country": album_release_country,
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
    if len(json_data.get('songs',[])) >= 1:
        data_info = info(json_data)
        score_info = evaluate(json_data)
        display_sample_results(data_info)
        display_score_result(score_info)
    else:
        st.warning("음악을 못 찾았습니다. 다시 입력해주세요.")
    

def info(res_json):
    info = res_json["songs"]
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/search/song-info"
    song_ids = ",".join([str(item["song_id"]) for item in info])
    param = {"song_id": song_ids}
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
    return res.json()

def evaluate(res_json):
    info = res_json["songs"]
    url = "https://hpc1ux4epg.execute-api.ap-northeast-2.amazonaws.com/api/v1/rag/evaluate/consistency"
    song_ids = ",".join([str(item["song_id"]) for item in info])
    param = {"song_id": song_ids}
    param_json = json.dumps(param)
    res = requests.post(url, data=param_json, headers={'Content-Type': 'application/json'})
    return res.json()

def display_score_result(score_info):
    info = score_info['score']
    image_data = info['radial_image']
    display_image(image_data)

# 이미지 디코딩 및 표시
def display_image(base64_str):
    st.write("")
    st.write("")
    img_data = base64.b64decode(base64_str)
    img = Image.open(BytesIO(img_data))
    cols = st.columns([1, 2, 1])  # 좌우 여백의 비율을 조정 (1:2:1)
    with cols[1]:  # 중간 열에 이미지를 배치
        st.image(img, caption="데이터 일관성", use_column_width=True)

# 곡 리스트에서 샘플을 보여주는 함수 (로컬 이미지 추가)
def display_sample_results(data_info):
    datas = data_info['songs']
    for song in datas[:10]:  # 리스트 5개만 출력
        song_id = song['song_id']
        song_name = song['song_name']
        artist_name = song['artist_name']
        st.markdown(f"{song_name} - {artist_name} [상세정보](https://genie.co.kr/detail/songInfo?xgnm={song_id})")

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

st.image(title_02_img, caption='', use_column_width=True)
# 곡 ID 검색 (st.expander 사용)

with st.expander("유사 곡 검색"):
    song_ids_prompt = st.text_input("곡 ID를 입력하세요 (예: 87443133 [아이유 - 가을 아침])")
    
    # 텍스트 입력창과 버튼을 같은 너비로 하기 위해 컨테이너 사용
    with st.container():
        song_search_button_clicked = st.button("곡 검색", use_container_width=True)
    
    if song_search_button_clicked:
        with st.spinner('AI가 플레이리스트를 만드는 중입니다...'):
            search_by_song_id(song_ids_prompt)

st.image(title_03_img, caption='', use_column_width=True)
# 아티스트 ID 검색 (st.expander 사용)
with st.expander("유사 아티스트 검색"):
    artist_ids_prompt = st.text_input("아티스트 ID를 입력하세요 (예: 67872918 [아이유])")
    
    # 텍스트 입력창과 버튼을 같은 너비로 하기 위해 컨테이너 사용
    with st.container():
        artist_search_button_clicked = st.button("아티스트 검색", use_container_width=True)
    
    if artist_search_button_clicked:
        with st.spinner('AI가 플레이리스트를 만드는 중입니다...'):
            search_by_artist_id(artist_ids_prompt)

import streamlit as st

from helper.ai_voice_helper import AIVoiceHelper
from helper.voices_dictionary import voices_dict

voice_dict = voices_dict.copy()

language_list = voice_dict.keys()


st.set_page_config(
    page_title="AI 음성 만들기 with AWS Polly",
    page_icon="🎤",
)

st.title("AI 음성 만들기")

st.markdown(
    """
    AI 음성을 만들어 보세요.
    
    ### 사용법
    1. 언어를 선택 합니다.
    2. 엔진을 선택 합니다.
       - neural 엔진 : 표준 음성보다 더 높은 품질의 음성을 생성할 수 있습니다. NTTS 시스템은 가능한 가장 자연스럽고 인간과 유사한 텍스트 음성 변환을 제공합니다.
       - standard 엔진 : 표준 TTS 음성은 연결합성(concatenative synthesis)을 사용합니다. 이 방법은 녹음된 음성의 음운을 연결하여 매우 자연스러운 합성 음성을 생성합니다. 그러나 불가피한 음성 변화와 음파를 분할하는 기술적인 한계로 인해 음성의 품질이 제한됩니다.
    3. 목소리를 선택 합니다.
    4. 속도를 선택 합니다.
    </br>
    """,
    unsafe_allow_html=True
)
with st.sidebar:
    access_key = st.text_input(
        "Write down a AWS ACCESS KEY",
        placeholder="AWS ACCESS KEY",
    )
    secret_access_key = st.text_input(
        "Write down a AWS SECRET ACCESS KEY",
        placeholder="AWS SECRET ACCESS KEY",
    )

selected_language = st.selectbox("언어 선택", language_list)

selected_engine = st.selectbox("엔진 선택", voice_dict[selected_language].keys())
select_data_list = [item['select_data'] for item in voice_dict[selected_language][selected_engine]]
selected_data = st.selectbox("목소리 선택", select_data_list)

selected_person_name = selected_data.split(" / ")[0]  # "Lupe / Female / Bilingual" -> "Lupe"

st.markdown(
    """
    ### 속도 선택
    - 20% : 매우 느림
    - 50% : 느림
    - 100% : 표준
    - 150% : 빠름
    - 200% : 매우 빠름
    """,
    unsafe_allow_html=True
)
speed_rate = st.slider(
    label="속도 선택",
    min_value=20, max_value=200, value=100,
    help="전체적으로 적용할 속도를 선택합니다. ssml 태그를 사용하면 부분적으로 속도를 따로 적용할 수 있습니다.",
)

text = st.text_area(
    label="내용 입력",
    help='음성으로 변환할 내용을 입력해주세요.',
    placeholder='음성으로 변환할 내용을 입력해주세요.',
    height=500,
)

create = st.button(
    label="음성 만들기",
)

if create:
    if selected_person_name and text:
        try:
            audio_stream = AIVoiceHelper(
                service="polly",
                access_key=access_key,
                secret_access_key=secret_access_key,
            ).synthesize_voice(
                text=text,
                voice_id=selected_person_name,
                rate=speed_rate,
                engine=selected_engine,
            )

        except Exception as e:
            st.error(f"음성 변환에 실패했습니다. {e}")
            audio_stream = None
            print(e)

        if audio_stream:
            selected_language_name = selected_language.split("/")[0]  # Swedish/sv-SE -> Swedish

            st.download_button(
                label="Download MP3",
                data=audio_stream,
                file_name=f"ai_voice_{selected_language_name}_{selected_engine}_{selected_person_name}.mp3",
                mime="audio/mpeg",
                disabled=False if audio_stream else True,
            )
            st.audio(audio_stream, format="audio/mpeg")

    else:
        st.warning("내용을 입력해주세요.")
        print("no")


st.markdown(
    """
    ### FAQ
    1. 음성 변환 실패 사례 (voice id 에러)
        - [AWS Polly 음성 목록](https://docs.aws.amazon.com/ko_kr/polly/latest/dg/voicelist.html) 에서 사용 가능한 목소리를 확인해주세요.
        - 만약 목소리가 없다면, helper/voice_dictionary.py 에서 해당 목소리를 삭제 해주세요. (aws 에서 지원 종료 했을 경우)
    """
)
