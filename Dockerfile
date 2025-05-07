# 1) 베이스 이미지
FROM python:3.10-slim

# 2) 작업 디렉토리
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 3) 의존성 복사 & 설치
RUN pip install --no-cache-dir \
    Flask \
    gunicorn \
    python-dotenv \
    sqlalchemy \
    pymysql \
    pandas \
    joblib \
    scikit-learn \
    xgboost

# 4) Flask 소스 복사
COPY . .

# 5) 실행
#    app.py에 Flask app 변수를 'app'으로 export했다고 가정
CMD ["gunicorn", "app:app", \
     "-b", "0.0.0.0:5000", \
     "--workers", "2", \
     "--timeout", "120"]
