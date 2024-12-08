import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",       # Cambia por tu contraseña
        database="tu_base_de_datos"  # Cambia por el nombre de tu base
    )
