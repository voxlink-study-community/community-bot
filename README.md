# Discord 커뮤니티 AI 챗봇

이 프로젝트는 FastAPI와 Streamlit을 사용하여 Discord 채팅 기록을 분석하고 질문에 답변하는 AI 챗봇을 제공합니다. FastAPI 서버가 대화 데이터를 처리하고, Streamlit UI가 사용자와 상호작용합니다.

## 📌 기능
- **FastAPI 백엔드**: Discord 대화 데이터를 분석하고 질문에 대한 답변을 생성
- **Streamlit 프론트엔드**: 사용자 질문 입력 및 대화 기록 제공
- **Groq API 연동**: AI 모델을 이용한 답변 생성
- **Docker 기반 배포**: FastAPI와 Streamlit을 컨테이너화하여 쉽게 실행 가능

---

## 📂 프로젝트 구조
```
📂 프로젝트 폴더
├── 📜 api_server.py  # FastAPI 서버 구현
├── 📜 streamlit_app.py  # Streamlit UI 구현
├── 📜 docker-compose.yml  # FastAPI & Streamlit 컨테이너 오케스트레이션
├── 📜 Dockerfile  # FastAPI 앱 컨테이너 빌드 설정
├── 📜 requirements.txt  # Python 종속성 리스트
└── 📜 .env.prod  # 환경 변수 파일 (API 키 등)
```

---

## 🚀 설치 및 실행

### 1️⃣ **환경 설정** (.env.prod 파일 작성)
FastAPI와 Streamlit이 사용할 환경 변수를 `.env.prod` 파일에 저장합니다.

```
GROQ_API_KEY=your_groq_api_key
URL=your_discord_chat_data_url
API_URL=http://fastapi:8000/ask
```

### 2️⃣ **필요한 패키지 설치**

```bash
pip install -r requirements.txt
```

### 3️⃣ **Docker Compose 실행**
FastAPI와 Streamlit을 컨테이너로 실행하려면 다음 명령어를 입력하세요.

```bash
docker-compose up --build
```

이후, 아래 주소에서 서비스에 접근할 수 있습니다:
- **FastAPI**: http://localhost:18000/docs
- **Streamlit UI**: http://localhost:18501

> FastAPI는 기본적으로 8000 포트에서 실행되지만, 기존 애플리케이션과의 충돌을 방지하기 위해 **외부에서 18000 포트로 접근하도록 설정**되었습니다.
> 마찬가지로 Streamlit도 기본적으로 8501 포트를 사용하지만, **외부에서는 18501 포트를 통해 접근**하도록 변경되었습니다.

---

## 🔧 API 엔드포인트

### **1️⃣ 질문하기 (`/ask` 엔드포인트)**
**요청 방식**: `POST`

**엔드포인트**:
```
POST /ask
```

**요청 예시**:
```json
{
  "question": "최근 프로젝트 진행 상황은?"
}
```

**응답 예시**:
```json
{
  "question": "최근 프로젝트 진행 상황은?",
  "answer": "최근 대화에 따르면 프로젝트는 80% 진행되었으며, 다음 주 테스트가 예정되어 있습니다."
}
```

---

## 📜 주요 코드 설명

### 🔹 **FastAPI 백엔드 (`api_server.py`)**
- Discord 대화 데이터를 파싱하고 저장
- 질문을 입력받아 관련 대화를 검색
- Groq API를 호출하여 AI 기반 답변 생성

### 🔹 **Streamlit 프론트엔드 (`streamlit_app.py`)**
- 사용자 질문 입력 및 대화 기록 관리
- FastAPI `/ask` 엔드포인트를 호출하여 답변을 받아 UI에 표시

---

## 📌 참고 사항
- Groq API 키가 필요합니다.
- Discord 대화 데이터는 특정 URL에서 가져와야 합니다.
- 기본적으로 최대 50개의 관련 메시지를 검색하여 응답을 생성합니다.

---

## 📜 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.

