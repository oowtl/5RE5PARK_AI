from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from torch.nn.functional import softmax


app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 Origin 허용
    allow_credentials=True,  # 쿠키나 인증 정보를 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

# 모델 로드
model_path = "JhDev/my-bert-sentiment-multiple"
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# 토크나이저 로드
tokenizer_name = "monologg/kobert"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, trust_remote_code=True)

# 데이터 라벨 정의
label_map = {
    0: "공포",
    1: "놀람",
    2: "분노",
    3: "슬픔",
    4: "중립",
    5: "행복",
    6: "혐오"
}


@app.get("/ai/sentiment")
def sentiment_analysis(text: str, status_code=200):
    print("text : ", text)

    # 텍스트를 토큰화
    inputs = tokenizer(text, return_tensors="pt")

    # 모델에 전달
    output = model(**inputs)
    logits = output.logits

    # logits에서 가장 높은 점수의 인덱스 추출
    predicted_labels = torch.argmax(logits, dim=1)

    # 라벨 매핑
    mapped_labels = [label_map[label.item()] for label in predicted_labels]

    # 결과 리스트
    result = []

    # 확률 구하기
    probabilities = softmax(logits, dim=1)
    for i, (label, prob) in enumerate(zip(mapped_labels, probabilities)):
        result.append({"emotion": label, "probability": prob.max().item() * 100})

    # response 생성하기
    response = {
        "status": status_code,
        "response": result
    }

    # 반환하기
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
