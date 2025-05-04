import pandas as pd
from sqlalchemy import create_engine

def save_data_to_csv():
    db_config = {
        "user": "root",
        "password": "root",
        "host": "localhost",
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
    WHERE t.recovered_date IS NOT NULL
      AND t.expected_payment_date IS NOT NULL
      AND DATEDIFF(t.recovered_date, t.expected_payment_date) >= 0
    """

    engine = create_engine(
        f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    df = pd.read_sql(query, engine)
    df.to_csv("train_data.csv", index=False, encoding="utf-8-sig")
