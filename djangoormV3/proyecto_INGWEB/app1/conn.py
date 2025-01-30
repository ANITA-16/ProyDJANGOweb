import mysql.connector
from mysql.connector import Error

try:
    # Parámetros de conexión
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="PIZZA",
        database="muebles"
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"Conectado al servidor MySQL versión {db_info}")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"Conectado a la base de datos: {record[0]}")

except Error as e:
    print(f"Error al conectar a MySQL: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada.")
