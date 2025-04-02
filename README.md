# community-bot

## 소개
FastAPI 기반의 커뮤니티 관리 자동화 봇 프로젝트입니다.  
사용자 등록, API 서버 실행, Streamlit 연동 등을 포함하며, Docker와 Docker Compose로 구성됩니다.

## 설치 방법

### 기본 설치
```bash
git clone https://github.com/voxlink-study-community/community-bot.git
cd community-bot
pip install -r requirements.txt
```

### Docker 사용 시
```bash
docker-compose up --build
```

## 실행 방법

### FastAPI 실행
```bash
uvicorn api_server:app --reload
```

### Streamlit 실행
```bash
streamlit run streamlit_app.py
```

---

## 학습 정리

### 환경변수 사용 이유  
관련 파일: .env, api_server.py, docker-compose.yml  
환경변수: 운영체제 또는 애플리케이션 레벨에서 설정하는 key-value 설정값

이유:
- 보안: Git에 노출되면 안 되는 비밀번호, API Key 등 정보 노출 방지
- 환경별 설정 분리: 개발, 운영, 테스트 서버 설정 분리, DB 주소, 캐시 서버 주소 등이 환경마다 다름
- 유연한 배포, 유지 보수: 동일한 코드로 개발, 운영 서버에 유연하게 배포 가능, CI/CD에 설정값을 주입하여 코드 재사용성 향상

.env 파일 예시:
```env
DATABASE_URL=postgresql://user:pass@localhost/db
DEBUG=True
```

예시 코드:
```python
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv("DATABASE_URL")
```

### Uvicorn 구조  
관련 파일: api_server.py, dockerfile  
FastAPI 앱을 실행하는 ASGI 서버(Asynchronous Server Gateway Interface)

특징:
- 비동기(async/await) 지원: I/O 작업(예: DB 조회, 외부 API 호출 등)을 기다리는 동안 다른 작업을 동시에 처리
- --reload 옵션: 개발 중 코드 변경 시 자동 재시작
- --workers 옵션: 운영 환경에서 멀티 프로세스 실행 가능

아키텍처 구조:
```
클라이언트 요청
    ↓
Uvicorn (ASGI 서버)
    ↓
FastAPI 애플리케이션
    ↓
라우터 / 미들웨어 / 핸들러
    ↓
응답 반환
```

### HTTPException  
관련 파일: api_server.py  
HTTP 오류 응답을 명확히 전달하기 위해 사용되는 예외 처리 도구  
HTTP 상태 코드와 함께 메시지를 전달할 수 있음.

예시 코드:
```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = get_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

주요 파라미터:
- status_code: 상태 코드 (예: 404, 400, 401 등)
- detail: 에러 메시지 내용
- headers: 응답 헤더 추가 설정 (선택)

### FastAPI CRUD 메서드  
관련 파일: api_server.py

```md
| **HTTP 메서드** | **역할**         | **FastAPI 데코레이터** | **CRUD 관점(Create, Read, Update, Delete)** |
|----------------|------------------|------------------------|----------------------------------------------|
| **GET**        | 데이터 조회       | `@app.get()`           | Read                                         |
| **POST**       | 새 데이터 생성     | `@app.post()`          | Create                                       |
| **PUT**        | 데이터 전체 수정   | `@app.put()`           | Update                                       |
| **PATCH**      | 데이터 부분 수정   | `@app.patch()`         | Partial Update                               |
| **DELETE**     | 데이터 삭제       | `@app.delete()`        | Delete                                       |
| OPTIONS        | 허용된 메서드 조회 | (자동 처리됨)           | 메타 정보                                     |
| HEAD           | 헤더만 요청       | (자동 처리됨)           | 메타 정보                                     |
| TRACE, CONNECT | 디버깅, 터널링     | 없음                   | 일반 웹 API에서는 사용하지 않음              |
```

---

## 참고 명령어 (Docker 설치 관련)

출처: https://velog.io/@hana0627/ec2%EC%97%90-%EB%8F%84%EC%BB%A4-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0

```bash
sudo systemctl status docker
sudo systemctl start docker
docker run hello-world
```

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.33.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'''