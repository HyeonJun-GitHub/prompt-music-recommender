import streamlit as st
import uuid

# 하드코딩된 URL을 반환하는 함수
def get_downloadurl(song_id):
    # 하드코딩된 MP3 URL
    return "http://www.noiseaddicts.com/samples_1w72b820/4261.mp3"

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
                # 버튼을 클릭하면 바로 해당 곡의 URL을 가져와 재생
                audio_url = get_downloadurl(song_id)
                st.audio(audio_url, format="audio/mp3", start_time=0)

# 샘플 결과 표시
display_sample_results()
