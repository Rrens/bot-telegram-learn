import mysql.connector
from mysql.connector import Error
from config.config import db_config
# from utils.helper import check_username_exists

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
            
def insert_user(username, chat_id, grup_type, role):
    grup_type = grup_type.lower()
    username = username.replace('@', '')
    if grup_type == 'swfm':
        registered_swfm = 'True'
        registered_ioms = 'False'
        registered_ipas = 'False'
    elif grup_type == 'ioms':
        registered_swfm = 'False'
        registered_ioms = 'True'
        registered_ipas = 'False'
    elif grup_type == 'scarlett':
        registered_swfm = 'False'
        registered_ioms = 'False'
        registered_ipas = 'True'
    elif grup_type == 'ipas':
        registered_swfm = 'False'
        registered_ioms = 'False'
        registered_ipas = 'True'
    else:
        print("Invalid grup_type")
        return None

    query = f"INSERT INTO helpdesk_bot_swfm VALUES ('None', '{username}', {chat_id}, 'None', 'None', 'None', '{registered_swfm}', '{registered_ioms}', '{registered_ipas}', '{role}', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None')"

    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor()
        print(query)
        cursor.execute(query)
        connection.commit()
        return "True"
    except Error as e:
        print(f"IKI ERROR: {e}")
        return e
    finally:
        if connection:
            connection.close()
        