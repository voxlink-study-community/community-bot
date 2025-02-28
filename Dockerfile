FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD는 docker-compose.yml에서 지정할 것이므로 여기서는 제거합니다.
