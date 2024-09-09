import streamlit as st

# 임시 데이터 (나중에 API를 통해 대체 가능)
sample_songs = [
    {"id": 1, "artist": "Artist A", "title": "Song A", "score": 90, "vocal": 0.8},
    {"id": 2, "artist": "Artist B", "title": "Song B", "score": 85, "vocal": 0.7},
    {"id": 3, "artist": "Artist C", "title": "Song C", "score": 80, "vocal": 0.6},
    {"id": 4, "artist": "Artist D", "title": "Song D", "score": 75, "vocal": 0.9},
    {"id": 5, "artist": "Artist E", "title": "Song E", "score": 88, "vocal": 0.65},
]

# 검색 함수들
def search_by_artist_id():
    st.write("Artist ID 검색 결과:")
    display_sample_results()

def search_by_song_id():
    st.write("Song ID 검색 결과:")
    display_sample_results()

def search():
    st.write("Prompt 검색 결과:")
    display_sample_results()

def search_vocal(song_id):
    st.write(f"Vocal 체크 결과 for Song ID {song_id}:")
    st.write("vocal: True, 80.0%")  # 임시 데이터 출력

def display_sample_results():
    for song in sample_songs[:5]:  # 리스트 5개만 출력
        st.markdown(f"**{song['id']} : {song['artist']} - {song['title']}** (Score: {song['score']}, Vocal: {round(song['vocal'] * 100, 2)}%)")
        st.markdown(f"[Link to song](https://genie.co.kr/detail/songInfo?xgnm={song['id']})")

# 레이아웃 시작
st.title("Prompt Search Application")

# Prompt 입력과 버튼
st.subheader("Prompt")
col1, col2 = st.columns([3, 1])
with col1:
    prompt = st.text_area("Enter your prompt")
with col2:
    if st.button("Search by Prompt"):
        search()

# Prompt 결과 표시
st.write("### Prompt Search Results")
display_sample_results()

# Song ID 입력과 버튼
st.subheader("Song ID (콤마(,)로 분리)")
col3, col4 = st.columns([3, 1])
with col3:
    song_ids_prompt = st.text_input("Enter Song IDs (comma-separated)")
with col4:
    if st.button("Search by Song ID"):
        search_by_song_id()

# Song ID 검색 결과 표시
st.write("### Song ID Search Results")
display_sample_results()

# Artist ID 입력과 버튼
st.subheader("Artist ID (콤마(,)로 분리)")
col5, col6 = st.columns([3, 1])
with col5:
    artist_ids_prompt = st.text_input("Enter Artist IDs (comma-separated)")
with col6:
    if st.button("Search by Artist ID"):
        search_by_artist_id()

# Artist ID 검색 결과 표시
st.write("### Artist ID Search Results")
display_sample_results()

# Vocal 체크 입력과 버튼
st.subheader("Song ID로 Vocal 유무 체크")
col7, col8 = st.columns([3, 1])
with col7:
    vocal_check_prompt = st.text_input("Enter Song ID for vocal check")
with col8:
    if st.button("Check Vocal by Song ID"):
        search_vocal(vocal_check_prompt)

# Vocal 체크 결과 표시
st.write("### Vocal Check Results")
search_vocal(vocal_check_prompt)
