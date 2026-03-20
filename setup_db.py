import pymysql

try:
    print("Connecting to MySQL to create database 'patientDB' if it doesn't exist...")
    conn = pymysql.connect(host='localhost', user='root', password='karanhunny8168')
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS patientDB")
    conn.commit()
    conn.close()
    print("Database ready!")
except Exception as e:
    print(f"Error connecting to MySQL: {e}")
