import joblib
import numpy as np
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Flask!"


# api 통신 테스트
# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.get_json()
#
#     try:
#         expected = datetime.strptime(data["expectedPaymentDate"], "%Y-%m-%d")
#         recovered = datetime.strptime(data["recoveredDate"], "%Y-%m-%d")
#         delay = (recovered - expected).days
#         return jsonify({"delayDays" : max(delay, 0)})
#     except Exception as e:
#         return jsonify({"error" : str(e)}), 400

# 모델, 인코더 불러오기
model = joblib.load("ml/data/model.pkl")
industry_encoder = joblib.load("ml/data/industry_encoder.pkl")


@app.route("/ml/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        # 필드 추출
        amount = int(data["transactionAmount"])
        industry = data["industry"]
        expected_days = int(data["expectedRecoveryDays"])

        # 업종 인코딩 - 2D로 넣어야함ㅁ
        industry_encoded = industry_encoder.transform([[industry]])

        # 입력 벡터 구성
        input_data = np.hstack([[amount, expected_days], industry_encoded[0]])
        input_data = input_data.reshape(1, -1)  # (1, n_features)
        
        # 예측
        predicted_delay = model.predict(input_data)[0]

        # 위험도 분류
        if predicted_delay <= 3:
            risk_level = "LOW"
            comment = "회수가 지연 될 가능성이 낮습니다."
        elif predicted_delay <= 7 :
            risk_level = "MEDIUM"
            comment = "회수가 지연 될 수 있습니다."
        else:
            risk_level = "HIGH"
            comment = "회수가 지연 될 가능성이 매우 높습니다."

        return jsonify({
            "predictedDelay": round(predicted_delay),
            "riskLevel": risk_level,
            "comment": comment
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
