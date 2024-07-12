import mysql.connector
client = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",    
    database="orderexpress"
)
cursor = client.cursor()

