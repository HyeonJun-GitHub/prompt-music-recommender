import streamlit as st

# 임시 데이터 (나중에 API를 통해 대체 가능)
sample_songs = [
    {"id": 1, "artist": "Artist A", "title": "Song A", "score": 90},
    {"id": 2, "artist": "Artist B", "title": "Song B", "score": 85},
    {"id": 3, "artist": "Artist C", "title": "Song C", "score": 80},
    {"id": 4, "artist": "Artist D", "title": "Song D", "score": 75},
    {"id": 5, "artist": "Artist E", "title": "Song E", "score": 88},
]

# CSS로 버튼과 입력 필드의 높이를 맞추기 위한 스타일 추가
st.markdown("""
    <style>
    .stTextInput > div > input {
        height: 38px;
        font-size: 14px;
    }
    .stButton > button {
        height: 40px;
        padding: 5px 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 검색 함수들
def search_by_artist_id(results_placeholder):
    results_placeholder.write("Artist ID 검색 결과:")
    display_sample_results(results_placeholder)

def search_by_song_id(results_placeholder):
    results_placeholder.write("Song ID 검색 결과:")
    display_sample_results(results_placeholder)

def search(results_placeholder):
    results_placeholder.write("Prompt 검색 결과:")
    display_sample_results(results_placeholder)

def display_sample_results(placeholder):
    for song in sample_songs[:5]:  # 리스트 5개만 출력
        placeholder.markdown(f"**{song['id']} : {song['artist']} - {song['title']}** (Score: {song['score']})")
        placeholder.markdown(f"[Link to song](https://genie.co.kr/detail/songInfo?xgnm={song['id']})")

# 레이아웃 시작
st.title("Prompt Search Application")

# Prompt 입력과 버튼
st.subheader("Prompt")
col1, col2 = st.columns([4, 1])
with col1:
    prompt = st.text_area("Enter your prompt")
with col2:
    if st.button("Search by Prompt"):
        prompt_results_placeholder = st.empty()
        search(prompt_results_placeholder)

# Prompt 결과 표시
prompt_results_placeholder = st.empty()  # 결과 표시 공간

# Song ID 입력과 버튼
st.subheader("Song ID (콤마(,)로 분리)")
col3, col4 = st.columns([4, 1])
with col3:
    song_ids_prompt = st.text_input("Enter Song IDs (comma-separated)")
with col4:
    if st.button("Search by Song ID"):
        song_id_results_placeholder = st.empty()
        search_by_song_id(song_id_results_placeholder)

# Song ID 검색 결과 표시
song_id_results_placeholder = st.empty()  # 결과 표시 공간

# Artist ID 입력과 버튼
st.subheader("Artist ID (콤마(,)로 분리)")
col5, col6 = st.columns([4, 1])
with col5:
    artist_ids_prompt = st.text_input("Enter Artist IDs (comma-separated)")
with col6:
    if st.button("Search by Artist ID"):
        artist_id_results_placeholder = st.empty()
        search_by_artist_id(artist_id_results_placeholder)

# Artist ID 검색 결과 표시
artist_id_results_placeholder = st.empty()  # 결과 표시 공간
