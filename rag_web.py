import streamlit as st
import requests

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

# Song ID로 Vocal 체크
st.subheader("Song ID로 Vocal 유무 체크")
vocal_check_prompt = st.text_input("Enter Song ID for vocal check")

# 검색 결과 표시 영역
st.subheader("Results")
result = st.empty()

# 검색 함수들
def search_by_artist_id(artist_ids):
    artist_ids = [artist_id.strip() for artist_id in artist_ids.split(',')]
    url = f"{st.experimental_get_query_params().get('origin', ['http://localhost'])[0]}/search?artist_ids={artist_ids}"
    res = requests.get(url).json()
    display_results(res)

def search_by_song_id(song_ids):
    song_ids = [song_id.strip() for song_id in song_ids.split(',')]
    url = f"{st.experimental_get_query_params().get('origin', ['http://localhost'])[0]}/search?song_ids={song_ids}"
    res = requests.get(url).json()
    display_results(res)

def search(prompt):
    url = f"{st.experimental_get_query_params().get('origin', ['http://localhost'])[0]}/search?prompt={prompt}"
    res = requests.get(url).json()
    display_results(res)

def search_vocal(song_id):
    url = f"{st.experimental_get_query_params().get('origin', ['http://localhost'])[0]}/search?song_id_for_vocal={song_id}"
    res = requests.get(url).json()
    if res.get('vocal') == -1:
        result.text("검출 실패")
    else:
        vocal_score = round(res['vocal'] * 100, 2)
        result.text(f"vocal: {res['vocal'] > 0.5}, {vocal_score}%")

def display_results(res):
    songs = res.get("songs", [])
    if not songs:
        result.text("No results found.")
    else:
        for song in songs:
            st.markdown(f"**{song['id']} : {song['artist']} - {song['title']}** (Score: {song['score']}, Vocal: {round(song['vocal'] * 100, 2)}%)")
            st.markdown(f"[Link to song](https://genie.co.kr/detail/songInfo?xgnm={song['id']})")

# 버튼들
if st.button("Search by Prompt"):
    search(prompt)

if st.button("Search by Song ID"):
    search_by_song_id(song_ids_prompt)

if st.button("Search by Artist ID"):
    search_by_artist_id(artist_ids_prompt)

if st.button("Check Vocal by Song ID"):
    search_vocal(vocal_check_prompt)
