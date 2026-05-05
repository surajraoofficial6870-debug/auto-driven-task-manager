from dotenv import load_dotenv
import os
import mysql.connector

# .env file load (local ke liye)
load_dotenv()

# environment variables se values lena
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=int(DB_PORT) if DB_PORT else 3306
    )

    print("✅ DB Connected Successfully")

except Exception as e:
    print("❌ DB Connection Failed:", e)