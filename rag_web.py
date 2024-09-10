import streamlit as st
import uuid

# 전역변수로 URL 저장
global_playing_song_url = None

# 하드코딩된 URL을 반환하는 함수
def get_downloadurl(song_id):
    # 하드코딩된 MP3 URL 반환
    return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

# 샘플 곡 리스트에서 결과를 표시하는 함수
def display_sample_results():
    global global_playing_song_url  # 전역 변수 선언

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
                
                # 전역 변수에 URL 저장
                global_playing_song_url = get_downloadurl(song_id)
                st.write(f"URL이 전역 변수에 저장되었습니다: {global_playing_song_url}")
                # 즉시 오디오 재생
                st.audio(global_playing_song_url, format="audio/mp3", start_time=0)

# 샘플 결과 표시
display_sample_results()