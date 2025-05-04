from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Flask!"


# api 통신 테스트
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        expected = datetime.strptime(data["expectedPaymentDate"], "%Y-%m-%d")
        recovered = datetime.strptime(data["recoveredDate"], "%Y-%m-%d")
        delay = (recovered - expected).days
        return jsonify({"delayDays" : max(delay, 0)})
    except Exception as e:
        return jsonify({"error" : str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
