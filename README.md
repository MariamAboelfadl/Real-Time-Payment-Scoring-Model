# Real-Time Payment Scoring System

## Overview
This project implements a **real-time payment scoring system** designed to detect potentially fraudulent transactions or evaluate customer creditworthiness. It integrates **Apache Kafka** for real-time data streaming, a **pre-trained machine learning model** for scoring, and **MySQL** for storing results.

The system processes incoming payment transactions in real time, applies a scoring model, and stores the results for reporting and analytics.

---

## Architecture
```
 Kafka Producer → ML Model → Kafka Consumer → MySQL Database
```

### Key Components
1. **Apache Kafka** – Streams real-time payment transactions.
2. **Machine Learning Model** – Pre-trained model for fraud/credit scoring.
3. **MySQL** – Stores scored transactions for reporting and monitoring.

---

## Features
- Real-time ingestion with Kafka
- End-to-end ML scoring pipeline
- Automatic storage of scored transactions in MySQL
- Pluggable ML model


---

## Prerequisites
- Python 3.9+
- Apache Kafka (Docker)
- MySQL 8+
- Docker Desktop 

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/MariamAboelfadl/payment-scoring-system.git

```

### 2. Install Dependencies
```bash
# Python Kafka library
pip install confluent-kafka

# Pandas 
pip install pandas

# Scikit-learn for ML model
pip install scikit-learn

# Joblib 
pip install joblib

# MySQL connector
pip install mysql-connector-python
```

### 3. Start Kafka 
```bash
docker-compose up -d
```

## Running the System

### 1. Produce Sample Kafka Messages
```bash
kafka-console-producer --broker-list localhost:9092 --topic payment_transactions
```



### 2. Run the Consumer
```bash
python consumer.py
```

The consumer will:
- Read messages from Kafka  
- Score each transaction  
- Insert results into MySQL  

---

## Future Enhancements

- Model retraining pipeline (Airflow)


