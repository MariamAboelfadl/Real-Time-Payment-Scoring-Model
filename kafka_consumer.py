from confluent_kafka import Consumer
import json
import mysql.connector
import joblib
import pandas as pd


model = joblib.load("fraud_model.joblib")
features = ["V1", "V2", "V3"]


conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'payment_group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf)
consumer.subscribe(['payment_transactions'])


db = mysql.connector.connect(
    host="localhost",
    user="cdc_user",
    password="cdc_pass",
    database="cdc_db"
)
cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS payment_scores (
    transaction_id BIGINT PRIMARY KEY,
    score FLOAT
);
""")
db.commit()


cursor.execute("SHOW COLUMNS FROM payment_scores LIKE 'is_fraud';")
result = cursor.fetchone()
if not result:
    cursor.execute("ALTER TABLE payment_scores ADD COLUMN is_fraud INT;")
    db.commit()

batch_counter = 0

while True:
    msg = consumer.poll(0.1)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    data = json.loads(msg.value())

    
    X_new = pd.DataFrame([[data[f] for f in features]], columns=features)
    
    
    score = float(model.predict_proba(X_new)[0][1])
    pred = int(model.predict(X_new)[0])

    
    sql = """
        INSERT INTO payment_scores (transaction_id, score, is_fraud)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE score=%s, is_fraud=%s
    """
    cursor.execute(sql, (data["Time"], score, pred, score, pred))
    batch_counter += 1

    if batch_counter % 200 == 0:
        db.commit()
        print(f"Committed {batch_counter} records")

db.commit()
          

