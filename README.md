# 🧠 Flask ML 예측 서버

## 📌 개요
이 서버는 회수 지연일 예측을 위한 Flask 기반 머신러닝 서버입니다.  
Spring 백엔드에서 거래 데이터를 전달받아, 학습된 `XGBoost` 회귀 모델을 통해  
예상 회수 지연일을 예측하고, 위험도를 분류하여 JSON 형태로 응답합니다.

---

## 🧠 기능 요약

| 항목 | 설명 |
|------|------|
| 학습 모델 | XGBoost 회귀 모델 (`delayDays` 예측) |
| 입력 데이터 | 거래 금액, 업종, 예상 회수일 등 |
| 전처리 | OneHotEncoder(업종 인코딩), 결측값 처리 |
| 위험도 분류 | 예측 결과 기준으로 LOW / MEDIUM / HIGH 등급 지정 |
| 배포 방식 | Flask + Gunicorn + Docker |
| API 경로 | `/ml/predict` (POST) |

---

## 🔍 예측 API 사용법

### ▶️ 엔드포인트
`POST /ml/predict`

### 📥 요청 형식 (JSON)

```json
[
  {
    "transaction_amount": 4500000,
    "industry": "교육",
    "expected_recovery_days": 15
  },
  ...
]
