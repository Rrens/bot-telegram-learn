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
            
def get_check_admin_or_not(id):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"select position from helpdesk_bot_swfm where chatid_telegram = '{id}' LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        return result['position']
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            
def get_problem_title(id):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"select problem_title from helpdesk_bot_swfm where chatid_telegram = '{id}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result['problem_title']
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            
def alter_problem_title(data_text, id):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"UPDATE helpdesk_bot_swfm SET problem_title = '{data_text}' WHERE chatid_telegram = '{id}'"
        cursor.execute(query)
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()