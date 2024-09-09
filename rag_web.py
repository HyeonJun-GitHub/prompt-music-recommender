import streamlit as st
import requests

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


# CSS 추가
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
    display_sample_results()

def search_by_song_id():
    display_sample_results()

def search():
    data = {"prompt":f"{prompt}","album_release_country":"KOREA","limit":200,"voice_yn":"Y","sort":"POPULAR","cnt":50}
    header = {"Content-Type":"application/json"}
    res = requests.post(data,headers=header)
    display_sample_results(res)

def display_sample_results(res):
    for song in res[:5]:  # 리스트 5개만 출력
        # st.markdown(f"**{song['song_id']} : {song['artist']} - {song['title']}** (Score: {song['score']}%)")
        st.markdown(f"[Link to song](https://genie.co.kr/detail/songInfo?xgnm={song['song_id']})")

# 레이아웃 시작
st.title("AI 큐레이션 TF!")
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
    song_ids_prompt = st.text_input("song_id,song_id,song_id")
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
    artist_ids_prompt = st.text_input("artist_id,artist_id,artist_id")
with col6:
    spacer = st.empty()  # 빈 공간 추가
    spacer.write("")
    spacer.write("")
    artist_search_button_clicked = st.button("아티스트 검색")

# Artist ID 검색 결과 표시 (버튼이 눌렸을 때만 결과 표시)
if artist_search_button_clicked:
    search_by_artist_id()
