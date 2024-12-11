# 베이스 이미지로 Python 3.12 사용
FROM python:3.12-slim
# 작업 디렉토리 설정
#WORKDIR /
# 종속성 파일 복사
COPY requirements.txt requirements.txt
# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt
# 애플리케이션 소스 코드 복사
COPY . .
# Flask 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]