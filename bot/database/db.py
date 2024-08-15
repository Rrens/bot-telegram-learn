import mysql.connector
from mysql.connector import Error
from config.config import db_config

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        return connection

def get_current_data_helpdesk(id):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM helpdesk_bot_swfm WHERE chatid_telegram = '{id}' LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            