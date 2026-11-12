import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="docefuturo1364",  
        database="doce_futuro"
    )