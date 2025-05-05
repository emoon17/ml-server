import joblib
import numpy as np
import traceback
from flask import Flask, request, jsonify

from ml.data.extract_from_db import save_data_to_csv
from ml.data.train_model import load_data_from_csv, train_and_save_model

app = Flask(__name__)

#  1. 학습 API (/ml/train) - 자정 스케줄러가 호출
@app.route("/ml/train", methods=["POST"])
def train_api():
    try:
        save_data_to_csv()
        df = load_data_from_csv()
        train_and_save_model(df)
        return jsonify({
            "status": "success",
            "message": "모델과 인코더가 성공적으로 저장되었습니다."
        }), 200

    except Exception as e:
        print(" 학습 중 예외 발생:")
        traceback.print_exc()  # 전체 에러 로그 터미널에 출력
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


#  2. 예측 API (/ml/predict) - 실시간 예측 요청
@app.route("/ml/predict", methods=["POST"])
def predict_api():
    try:
        # 저장된 모델 및 인코더 로드
        model = joblib.load("model.pkl")
        encoder = joblib.load("industry_encoder.pkl")

        #  요청 데이터 파싱
        data = request.get_json()
        amount = float(data["transactionAmount"])
        industry = data["industry"]
        expected_days = int(data["expectedRecoveryDays"])

        #  입력 데이터 인코딩
        industry_encoded = encoder.transform([[industry]])
        input_data = np.hstack([[amount, expected_days], industry_encoded[0]]).reshape(1, -1)

        #  예측
        predicted_delay = model.predict(input_data)[0]

        #  위험도 해석
        if predicted_delay >= 6:
            risk_level = "HIGH"
            comment = "회수가 지연될 가능성이 매우 높습니다."
        elif predicted_delay >= 3:
            risk_level = "MEDIUM"
            comment = "회수가 지연될 수 있습니다."
        else:
            risk_level = "LOW"
            comment = "회수가 지연될 가능성이 낮습니다."

        return jsonify({
            "predictedDelay": round(predicted_delay),
            "riskLevel": risk_level,
            "comment": comment
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# 헬스 체크
@app.route("/")
def index():
    return " Flask ML API 서버 작동 중 (/ml/train, /ml/predict)"


if __name__ == "__main__":
    app.run(debug=True)
