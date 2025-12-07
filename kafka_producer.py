import pandas as pd
from confluent_kafka import Producer

conf = {'bootstrap.servers': "localhost:9092"}  
producer = Producer(conf)
topic = "payment_transactions"


data = pd.read_csv("C:/Users/dell/Desktop/kafka-docker/creditcard.csv")

for idx, row in data.iterrows():
    message = row.to_json()
    producer.produce(topic, key=str(idx), value=message)
    
    if idx % 500 == 0:
        producer.flush()

producer.flush()
print("All messages sent!")
