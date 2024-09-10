import streamlit as st

# CSS를 사용하여 배경 이미지를 설정합니다.
page_bg_img = '''
<style>
.stApp {
  background-image: url("https://www.example.com/path/to/your/image.jpg");
  background-size: cover;
}
</style>
'''

# CSS를 적용합니다.
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("AI 큐레이션 TF")

# Prompt 입력
with st.container():
    st.subheader("프롬프트")
    prompt = st.text_area("무슨 노래가 듣고 싶어요?")
    search_button_clicked = st.button("프롬프트 검색")
    if search_button_clicked:
        st.write(f"프롬프트로 '{prompt}' 검색 중...")

# 곡 ID 검색
with st.container():
    st.subheader("유사 곡 검색")
    song_ids_prompt = st.text_input("곡 ID를 입력하세요 (예: 87443133 [아이유 - 가을 아침])")
    song_search_button_clicked = st.button("곡 검색")
    if song_search_button_clicked:
        st.write(f"'{song_ids_prompt}'로 곡 검색 중...")

# 아티스트 ID 검색
with st.container():
    st.subheader("유사 아티스트 검색")
    artist_ids_prompt = st.text_input("아티스트 ID를 입력하세요 (예: 67872918 [아이유])")
    artist_search_button_clicked = st.button("아티스트 검색")
    if artist_search_button_clicked:
        st.write(f"'{artist_ids_prompt}'로 아티스트 검색 중...")
