import pandas as pd
from sqlalchemy import create_engine


db_config = {
    "user" : "root",
    "password" : "root",
    "host" : "localhost",
    "port" : "3306",
    "database" : "recovery"
}

# 학습용 데이터 조회
query = """
SELECT
    t.transaction_id AS tx_id,
    t.transaction_amount,
    c.industry,
    c.expected_recovery_days,
    DATEDIFF(t.recovered_date, t.expected_payment_date) AS delayDays
FROM transaction t
JOIN client c ON t.client_id = c.client_id
WHERE t.recovered_date IS NOT NULL
  AND t.expected_payment_date IS NOT NULL
  AND DATEDIFF(t.recovered_date, t.expected_payment_date) >= 0
"""

# csv 저장
if __name__ == "__main__":
    engine = create_engine(
        f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    df = pd.read_sql(query, engine)
    df.to_csv("train_data.csv", index=False, encoding="utf-8-sig")
    print("학습 데이터 저장 완료: train_data.csv")