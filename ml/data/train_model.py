# 학습 결과
import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 1. csv 파일 불러오기
df = pd.read_csv("train_data.csv")

# 2. industry(업종) 컬럼 인코딩 -  (handle_unknown='ignore' 설정 => 모르는 컬럼은 빼고 아는걸로 결과 도출)
encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
industry_encoded = encoder.fit_transform(df[['industry']])

# 3. 학습 / 정답 데이터 분리
x = np.hstack([df[['transaction_amount', 'expected_recovery_days']].values, industry_encoded])
y = df[['delayDays']].values.ravel()  # shape 맞추기 위해 ravel

# 4. 학습/ 검증용 데이터셋 분리
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 5. 모델 학습
model = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
model.fit(x_train, y_train)

# 6. 예측 및 평가
y_pred = model.predict(x_test)
mse = mean_squared_error(y_test, y_pred)
print(f"✅ Mean Squared Error: {mse:.2f}")

# 7. 모델 저장
joblib.dump(model, "model.pkl")
joblib.dump(encoder, "industry_encoder.pkl")

print("모델, 인코더 저장 완료")