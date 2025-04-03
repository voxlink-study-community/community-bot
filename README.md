## FastAPI CRUD
- **Create**: `@app.post("/items")`로 데이터 생성  
- **Read**: `@app.get("/items")`, `@app.get("/items/{item_id}")`로 목록/단일 조회  
- **Update**: `@app.put("/items/{item_id}")`로 데이터 갱신  
- **Delete**: `@app.delete("/items/{item_id}")`로 데이터 삭제  
- 주로 Pydantic 모델과 함께 사용하며, DB 연동 시 ORM(예: SQLAlchemy) 활용

## HTTPException
- FastAPI에서 에러 발생 시 `HTTPException(status_code=..., detail=...)`로 예외 처리
- 주요 HTTP 에러코드 (한 줄 요약)
  - 400 (Bad Request): 요청이 잘못되었음
  - 401 (Unauthorized): 인증이 필요하거나 실패
  - 403 (Forbidden): 인증은 되었으나 권한 없음
  - 404 (Not Found): 요청한 리소스가 존재하지 않음
  - 405 (Method Not Allowed): 지원되지 않는 HTTP 메서드
  - 409 (Conflict): 리소스 충돌
  - 422 (Unprocessable Entity): 형식은 맞으나 처리 불가능
  - 429 (Too Many Requests): 과도한 요청
  - 500 (Internal Server Error): 서버 내부 에러
  - 502 (Bad Gateway): 잘못된 게이트웨이 응답
  - 503 (Service Unavailable): 서버 과부하 또는 점검
  - 504 (Gateway Timeout): 게이트웨이(프록시) 응답 시간 초과

## Uvicorn 아키텍처
- ASGI 서버로, asyncio 기반 비동기 I/O 처리
- 고성능 이벤트 루프(`uvloop`)와 `httptools`를 사용해 빠른 요청/응답
- 싱글 프로세스 + 비동기 구조 권장, 필요 시 멀티 워커 구성 가능
- Gunicorn과 결합해 확장성 있는 배포 가능

## 환경변수(ENV) 사용 이유
- 민감 정보(DB 비밀번호, API 키 등)의 보안을 위해 코드에서 분리
- 개발·테스트·프로덕션 등 환경별 다른 설정을 쉽게 적용
- Docker/Kubernetes 등 컨테이너·클라우드 환경에서 표준적 설정 관리
