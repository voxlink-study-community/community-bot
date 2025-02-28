from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv
import re
import time
from typing import List, Dict
import requests
from datetime import datetime
from collections import defaultdict

load_dotenv()
app = FastAPI()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Message:
    def __init__(self, timestamp: str, user: str, content: str):
        self.timestamp = timestamp
        self.user = user
        self.content = content

MESSAGES_BY_CHANNEL: Dict[str, List[Message]] = {}

def build_index():
    try:
        response = requests.get(os.getenv("URL"))
        response.raise_for_status()
        
        lines = response.text.split('\n')
        current_channel = None

        for line in lines:
            line = line.strip()
            if line.startswith("--- "):
                current_channel = line.strip("--- ").strip()
                MESSAGES_BY_CHANNEL[current_channel] = []
                continue
            if current_channel and line:
                match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2}) - (.+?): (.+)", line)
                if match:
                    timestamp, user, content = match.groups()
                    message = Message(timestamp, user.strip(), content)
                    MESSAGES_BY_CHANNEL[current_channel].append(message)
                    
    except Exception as e:
        raise RuntimeError(f"데이터 로딩 실패: {str(e)}")

build_index()

def calculate_relevance(message: Message, question: str) -> float:
    # 간단한 관련성 점수 계산 (실제 구현에서는 더 복잡한 알고리즘 사용 가능)
    relevance = sum(word.lower() in message.content.lower() for word in question.split())
    return relevance

def retrieve_relevant_messages(question: str, max_messages=50) -> List[Message]:
    all_messages = []
    for channel in MESSAGES_BY_CHANNEL.values():
        all_messages.extend(channel)
    
    # 관련성에 따라 메시지 정렬
    relevant_messages = sorted(all_messages, key=lambda msg: calculate_relevance(msg, question), reverse=True)
    
    # 시간순으로 재정렬
    return sorted(relevant_messages[:max_messages], key=lambda msg: msg.timestamp)

def generate_context(messages: List[Message]) -> str:
    context = ""
    current_date = None
    for msg in messages:
        msg_date = datetime.strptime(msg.timestamp[:10], "%Y-%m-%d").date()
        if msg_date != current_date:
            context += f"\n[{msg_date}]\n"
            current_date = msg_date
        context += f"{msg.timestamp[11:19]} - {msg.user}: {msg.content}\n"
    return context.strip()

def generate_answer(question: str, context: str) -> str:
    try:
        prompt = f"""
당신은 디스코드 대화 기록을 분석하는 AI 전문가입니다. 다음 지침을 따라 질문에 답변해주세요:

1. 제공된 대화 기록을 주의 깊게 분석하세요.
2. 대화의 전체적인 흐름과 맥락을 파악하세요.
3. 질문과 가장 관련 있는 정보를 중심으로 답변을 구성하세요.
4. 명시적으로 언급되지 않은 내용이라도, 맥락상 추론 가능한 정보는 포함해도 됩니다.
5. 추론 시 "~로 보입니다", "~인 것 같습니다" 등의 표현을 사용하세요.
6. 답변은 한국어로, 존댓말(해요체)을 사용하세요.
7. 구체적인 정보와 예시를 포함하여 상세하게 답변하세요.
8. 답변의 근거가 되는 대화 내용을 인용하여 설명하세요.

대화 기록:
{context}

질문: {question}

답변 과정:
1. 질문 분석:
2. 관련 정보 파악:
3. 맥락 고려:
4. 결론 도출:

최종 답변:
"""
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "당신은 디스코드 대화 기록을 분석하는 AI 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.12,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"오류 발생: {str(e)}"

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    if not query.question:
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")
    relevant_messages = retrieve_relevant_messages(query.question)
    context = generate_context(relevant_messages)
    answer = generate_answer(query.question, context)
    return {"question": query.question, "answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
