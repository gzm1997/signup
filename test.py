import mysql.connector

conn = mysql.connector.connect(user = "root", password = "Gzm20125", database = "ikdeer_user")
cursor = conn.cursor()
cursor.execute("select * from user;")
v = cursor.fetchall()

print(v)

conn.commit()
cursor.close()