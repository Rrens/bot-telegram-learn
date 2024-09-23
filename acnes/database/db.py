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

def helper_convert_dict_to_array(data_dict):
    columns = list(data_dict.keys())
    values = [data_dict.get(col, '') for col in columns]
    
    return values

def get_app_by_ip_address(ip):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM application_catalog WHERE tautan_url_akses LIKE  '%{ip}%' LIMIT 1"
        cursor.execute(query)
        print('QUERY GET APP BY IP ADDRESS')
        result = helper_convert_dict_to_array(cursor.fetchone())
        
        return result
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            