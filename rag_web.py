# import streamlit as st
# import requests

# # 제목과 입력 필드
# st.title("Prompt Search Application")

# # Prompt 입력
# st.subheader("Prompt")
# prompt = st.text_area("Enter your prompt")

# # Song ID 입력
# st.subheader("Song ID (콤마(,)로 분리)")
# song_ids_prompt = st.text_input("Enter Song IDs (comma-separated)")

# # Artist ID 입력
# st.subheader("Artist ID (콤마(,)로 분리)")
# artist_ids_prompt = st.text_input("Enter Artist IDs (comma-separated)")

# # 검색 결과 표시 영역
# st.subheader("Results")
# result = st.empty()

# # 검색 함수들
# def search_by_artist_id(artist_ids):
#     artist_ids = [artist_id.strip() for artist_id in artist_ids.split(',')]
#     url = f"{st.experimental_get_query_params().get('origin', ['http://localhost'])[0]}/search?artist_ids={artist_ids}"
#     res = requests.get(url).json()
#     display_results(res)

# def search_by_song_id(song_ids):
#     song_ids = [song_id.strip() for song_id in song_ids.split(',')]
#     url = f"{st.experimental_get_query_params().get('origin', ['http://localhost'])[0]}/search?song_ids={song_ids}"
#     res = requests.get(url).json()
#     display_results(res)

# def search(prompt):
#     url = f"{st.experimental_get_query_params().get('origin', ['http://localhost'])[0]}/search?prompt={prompt}"
#     res = requests.get(url).json()
#     display_results(res)

# def display_results(res):
#     songs = res.get("songs", [])
#     if not songs:
#         result.text("No results found.")
#     else:
#         for song in songs:
#             st.markdown(f"**{song['id']} : {song['artist']} - {song['title']}** (Score: {song['score']}, Vocal: {round(song['vocal'] * 100, 2)}%)")
#             st.markdown(f"[Link to song](https://genie.co.kr/detail/songInfo?xgnm={song['id']})")

# # 버튼들
# if st.button("Search by Prompt"):
#     search(prompt)

# if st.button("Search by Song ID"):
#     search_by_song_id(song_ids_prompt)

# if st.button("Search by Artist ID"):
#     search_by_artist_id(artist_ids_prompt)

import streamlit as st

# 제목과 입력 필드
st.title("Prompt Search Application")

# Prompt 입력
st.subheader("Prompt")
prompt = st.text_area("Enter your prompt")

# Song ID 입력
st.subheader("Song ID (콤마(,)로 분리)")
song_ids_prompt = st.text_input("Enter Song IDs (comma-separated)")

# Artist ID 입력
st.subheader("Artist ID (콤마(,)로 분리)")
artist_ids_prompt = st.text_input("Enter Artist IDs (comma-separated)")

# 검색 결과 표시 영역
st.subheader("Results")
result = st.empty()

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
    # API 연결 후 실제 검색 데이터로 대체 가능
    result.write("Artist ID 검색 결과:")
    display_sample_results()

def search_by_song_id():
    # API 연결 후 실제 검색 데이터로 대체 가능
    result.write("Song ID 검색 결과:")
    display_sample_results()

def search():
    # API 연결 후 실제 검색 데이터로 대체 가능
    result.write("Prompt 검색 결과:")
    display_sample_results()

def display_sample_results():
    for song in sample_songs[:5]:  # 리스트 5개만 출력
        st.markdown(f"**{song['id']} : {song['artist']} - {song['title']}** (Score: {song['score']}, Vocal: {round(song['vocal'] * 100, 2)}%)")
        st.markdown(f"[Link to song](https://genie.co.kr/detail/songInfo?xgnm={song['id']})")

# 버튼들
if st.button("Search by Prompt"):
    search()

if st.button("Search by Song ID"):
    search_by_song_id()

if st.button("Search by Artist ID"):
    search_by_artist_id()