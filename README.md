소개

FastAPI 기반의 커뮤니티 관리 자동화 봇 프로젝트입니다.사용자 등록, API 서버 실행, Streamlit 연동 등을 포함하며, Docker와 Docker Compose로 구성됩니다.

설치 방법

기본 설치

git clone https://github.com/voxlink-study-community/community-bot.git
cd community-bot
pip install -r requirements.txt

Docker 사용 시

docker-compose up --build

실행 방법

FastAPI 실행

uvicorn api_server:app --reload

Streamlit 실행

streamlit run streamlit_app.py

학습 정리

환경변수 사용 이유

관련 파일: .env, api_server.py, docker-compose.yml환경변수: 운영체제 또는 애플리케이션 레벨에서 설정하는 key-value 설정값

이유:

민감 정보(DB 비밀번호, API 키 등)의 보안을 위해 코드에서 분리

개발·운영·테스트 등 환경별 설정을 쉽게 분리

Docker/Kubernetes 등 컨테이너·클라우드 환경에서 표준적 설정 관리

.env 파일 예시:

DATABASE_URL=postgresql://user:pass@localhost/db
DEBUG=True

예시 코드:

from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv("DATABASE_URL")

Uvicorn 구조 및 아키텍처

관련 파일: api_server.py, dockerfile

ASGI 서버로 FastAPI 앱을 실행하는 데 사용

asyncio 기반 비동기 I/O 처리

고성능 이벤트 루프(uvloop)와 httptools를 사용해 빠른 요청/응답

--reload 옵션: 개발 중 코드 변경 시 자동 재시작

--workers 옵션: 운영 환경에서 멀티 프로세스 실행 가능

Gunicorn과 결합해 확장성 있는 배포 가능

아키텍처 구조:

클라이언트 요청
    ↓
Uvicorn (ASGI 서버)
    ↓
FastAPI 애플리케이션
    ↓
라우터 / 미들웨어 / 핸들러
    ↓
응답 반환

HTTPException

관련 파일: api_server.pyHTTP 오류 응답을 명확히 전달하기 위해 사용되는 예외 처리 도구FastAPI에서 에러 발생 시 HTTPException(status_code=..., detail=...)로 예외 처리

예시 코드:

from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = get_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

주요 HTTP 에러코드 요약:

400: Bad Request

401: Unauthorized

403: Forbidden

404: Not Found

405: Method Not Allowed

409: Conflict

422: Unprocessable Entity

429: Too Many Requests

500: Internal Server Error

502: Bad Gateway

503: Service Unavailable

504: Gateway Timeout

FastAPI CRUD 메서드

관련 파일: api_server.py

| **HTTP 메서드** | **역할**         | **FastAPI 데코레이터** | **CRUD 관점(Create, Read, Update, Delete)** |
|----------------|------------------|------------------------|----------------------------------------------|
| **GET**        | 데이터 조회       | `@app.get()`           | Read                                         |
| **POST**       | 새 데이터 생성     | `@app.post()`          | Create                                       |
| **PUT**        | 데이터 전체 수정   | `@app.put()`           | Update                                       |
| **PATCH**      | 데이터 부분 수정   | `@app.patch()`         | Partial Update                               |
| **DELETE**     | 데이터 삭제       | `@app.delete()`        | Delete                                       |

예시:

@app.post("/items")
def create_item(item: Item):
    return item

참고 명령어 (Docker 설치 관련)

출처: https://velog.io/@hana0627/ec2%EC%97%90-%EB%8F%84%EC%BB%A4-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0

sudo systemctl status docker
sudo systemctl start docker
docker run hello-world

sudo curl -L "https://github.com/docker/compose/releases/download/v2.33.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose