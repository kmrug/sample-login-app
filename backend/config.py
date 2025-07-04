import time
import mysql.connector
from mysql.connector import Error
import os

for attempt in range(10):
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("Connected to MySQL")
        break
    except Error as e:
        print(f"⏳ Waiting for MySQL ({attempt+1}/10)...")
        time.sleep(2)
else:
    print("Could not connect to MySQL after 10 attempts")
    exit(1)
