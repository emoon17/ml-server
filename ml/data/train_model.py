import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor

def load_data_from_csv(csv_path="train_data.csv"):
    df = pd.read_csv(csv_path)
    return df

def train_and_save_model(df, model_path="model.pkl", encoder_path="industry_encoder.pkl"):
    # 1. 인코딩
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    industry_encoded = encoder.fit_transform(df[['industry']])

    # 2. 입력 / 정답 나누기
    x = np.hstack([
        df[['transaction_amount', 'expected_recovery_days']].values,
        industry_encoded
    ])
    y = df['delayDays'].values

    # 3. 모델 학습
    model = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(x, y)

    # 4. 모델 & 인코더 저장
    joblib.dump(model, model_path)
    joblib.dump(encoder, encoder_path)

    print(" 모델, 인코더 저장 완료")

if __name__ == "__main__":
    df = load_data_from_csv()
    train_and_save_model(df)
