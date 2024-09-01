import mysql.connector
from mysql.connector import Error


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Kimdavid1.',
            database='users',
            connection_timeout=600
        )
        if connection.is_connected():
            print("Connected to the database")
            return connection
    except Error as e:
        print(f'Error: {e}')
