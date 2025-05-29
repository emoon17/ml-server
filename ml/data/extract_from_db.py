import pandas as pd
from sqlalchemy import create_engine
import pymysql
import cryptography


def save_data_to_csv():
    db_config = {
        "user": "root",
        "password": "Root123!",
        "host": "13.209.126.76",
        "port": "3306",
        "database": "recovery"
    }

    query = """
    SELECT
        t.transaction_amount,
        c.industry,
        c.expected_recovery_days,
        DATEDIFF(t.recovered_date, t.expected_payment_date) AS delayDays
    FROM transaction t
    JOIN client c ON t.client_id = c.client_id
    WHERE DATE(t.expected_payment_date) &lt;= DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND (t.transaction_amount != t.recovered_amount or t.recovered_date is null)
        GROUP BY t.transaction_id
    """

    engine = create_engine("mysql+pymysql://root:Root123!@13.209.126.76:3306/recovery")

    df = pd.read_sql(query, engine)
    df.to_csv("train_data.csv", index=False, encoding="utf-8-sig")
    print("data 저장 완료")
