import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv(".env.prod")
# 환경변수 설정
API_URL = os.getenv("API_URL", "http://fastapi:8000/ask")

st.title("Discord 커뮤니티 kangshinwoo-93 전용 챗봇")
st.markdown("---")

# 세션 초기화 (최소화)
if 'history' not in st.session_state:
    st.session_state.history = []

# 사이드바 - 초기화 버튼
with st.sidebar:
    if st.button("대화 초기화"):
        st.session_state.history = []

# 메인 채팅 인터페이스
with st.form("question_form"):
    question = st.text_input("질문 입력:")
    submitted = st.form_submit_button("질문하기")

    if submitted and question:
        try:
            # API 요청
            response = requests.post(API_URL, json={"question": question})
            
            if response.ok:
                answer = response.json().get("answer", "답변을 생성할 수 없습니다")
                st.session_state.history.append((question, answer))
            else:
                st.error(f"API 오류: {response.status_code}")

        except Exception as e:
            st.error(f"연결 오류: {str(e)}")

# 채팅 기록 표시
st.markdown("### 대화 기록")
for q, a in st.session_state.history:
    st.markdown(f"**Q:** {q}") 
    st.markdown(f"**A:** {a}")
    st.markdown("---")
