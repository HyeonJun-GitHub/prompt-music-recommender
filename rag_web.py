import streamlit as st

# 컨테이너 안에 있는 섹션마다 다른 배경색을 지정하는 CSS
container_style_1 = '''
<div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
'''
container_style_2 = '''
<div style="background-color: #faebd7; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
'''
container_style_3 = '''
<div style="background-color: #f5f5dc; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
'''

# Prompt 입력 섹션
st.markdown(container_style_1, unsafe_allow_html=True)
st.subheader("프롬프트")
prompt = st.text_area("무슨 노래가 듣고 싶어요?")
search_button_clicked = st.button("프롬프트 검색")
if search_button_clicked:
    st.write(f"프롬프트로 '{prompt}' 검색 중...")
st.markdown("</div>", unsafe_allow_html=True)  # 컨테이너 끝

# 곡 ID 검색 섹션
st.markdown(container_style_2, unsafe_allow_html=True)
st.subheader("유사 곡 검색")
song_ids_prompt = st.text_input("곡 ID를 입력하세요 (예: 87443133 [아이유 - 가을 아침])")
song_search_button_clicked = st.button("곡 검색")
if song_search_button_clicked:
    st.write(f"'{song_ids_prompt}'로 곡 검색 중...")
st.markdown("</div>", unsafe_allow_html=True)  # 컨테이너 끝

# 아티스트 ID 검색 섹션
st.markdown(container_style_3, unsafe_allow_html=True)
st.subheader("유사 아티스트 검색")
artist_ids_prompt = st.text_input("아티스트 ID를 입력하세요 (예: 67872918 [아이유])")
artist_search_button_clicked = st.button("아티스트 검색")
if artist_search_button_clicked:
    st.write(f"'{artist_ids_prompt}'로 아티스트 검색 중...")
st.markdown("</div>", unsafe_allow_html=True)  # 컨테이너 끝
