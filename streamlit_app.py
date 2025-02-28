import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# 세션 상태 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

st.title("Discord 커뮤니티 RAG 챗봇")

st.markdown("""
이 앱은 Discord 커뮤니티의 대화 기록을 기반으로 질문에 답변합니다.
- 질문을 입력하고 '질문하기' 버튼을 클릭하세요.
- 이전 대화 기록은 페이지 아래에서 확인할 수 있습니다.
""")

# 환경변수나 Streamlit Secrets를 활용하여 API URL 설정
#API_URL = os.getenv("API_URL", "http://localhost:8000/ask")
API_URL = os.getenv("API_URL", "http://api:8000/ask")

# 사이드바에 컨트롤 배치
with st.sidebar:
    st.markdown("### 설정")
    clear_button = st.button("대화 기록 지우기")
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()

# 메인 채팅 인터페이스
question = st.text_input("질문을 입력하세요:", key="question_input")

# 질문하기 버튼
submit_button = st.button("질문하기", disabled=st.session_state.submitted)

if submit_button and question:
    # 제출 상태를 True로 설정하여 버튼 비활성화
    st.session_state.submitted = True
    with st.spinner('답변을 생성하고 있습니다...'):
        try:
            # API 요청
            response = requests.post(API_URL, json={"question": question}, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # 채팅 기록에 추가
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": data.get("answer"),
                    "context": data.get("context")
                })
                
                # 제출 상태 해제 및 페이지 다시 렌더링
                st.session_state.submitted = False
                st.rerun()
            else:
                st.error(f"오류 발생: {response.status_code} - {response.text}")
                st.session_state.submitted = False
                
        except requests.exceptions.Timeout:
            st.error("요청 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.")
            st.session_state.submitted = False
        except Exception as e:
            st.error(f"요청 중 오류 발생: {e}")
            st.session_state.submitted = False
elif submit_button and not question:
    st.warning("질문을 입력해주세요.")

# 채팅 기록 표시
if st.session_state.chat_history:
    st.markdown("### 대화 기록")
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.container():
            st.markdown("---")
            st.markdown(f"**Q: {chat['question']}**")
            st.markdown(f"**A:** {chat['answer']}")
