import mysql.connector

conn = mysql.connector.connect(
    host="trolley.proxy.rlwy.net",
    user="root",
    password="PASTE_NEW_PASSWORD_HERE",
    database="railway",
    port=17084
)

print("✅ DB Connected Successfully")