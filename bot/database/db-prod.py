import clickhouse_connect
import pandas as pd

def create_connection():
    try:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        return client
    except Exception as e:
        print(f"Error connecting to ClickHouse: {e}")
        return None

def get_current_data_helpdesk(id):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM helpdesk_bot_swfm WHERE chatid_telegram = '{id}' LIMIT 1"
        cursor.execute(query)
        print('QUERY GET CURRENT DATA')
        result = helper_convert_dict_to_array(cursor.fetchone())
        
        return result
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            
def get_ticket_data_helpdesk(id):
    try:
        print('QUERY GET TICKET DATA')
        return get_current_data_helpdesk(id)[11]
    except Error as e:
        print(f"Error: {e}")
        return None
    
def get_id_data_helpdesk(id):
    try:
        print('QUERY GET ID DATA HELPDESK')
        return get_current_data_helpdesk(id)[3]
    except Error as e:
        print(f"Error: {e}")
        return None
    
            
def get_check_admin_or_not(id):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"select position from helpdesk_bot_swfm where chatid_telegram = '{id}' LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        print('QUERY GET ADMIN OR NOT')
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
        print('QUERY GET PROBLEM TITLE')
        result = cursor.fetchone()
        return result['problem_title']
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            
def get_count_ioms():
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"select count(*) as `count` from helpdesk_expert where application_name = 'IOMS'"
        cursor.execute(query)
        print(f'QUERY GET COUNT IOMS')
        result = cursor.fetchone()
        return result['count']
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            
def get_expert(app):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"select expert from helpdesk_expert where application_name = '{app}'"
        cursor.execute(query)
        print(f'QUERY GET EXPERT {app}')
        result = cursor.fetchone()
        return result
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
        print('QUERY ALTER PROBLEM TITLE')
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            
def alter_problem_summary(ticket, keterangan, date_time, id):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"UPDATE helpdesk_bot_swfm SET channel_chatid = '-1001966245452', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IOMS', status = 'open', fcaps = 'ADMINISTRATION' WHERE chatid_telegram = '{id}'"
        print('QUERY ALTER PROBLEM SUMMARY')
        cursor.execute(query)
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            
def insert_helpdesk_report(data):
    try:
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"INSERT INTO helpdesk_report_swfm select '{data[0]}','{data[1]}','{data[2]}','{data[3]}','{data[4]}','{data[5]}','{data[6]}','{data[7]}','{data[8]}','{data[9]}','{data[10]}','{data[11]}','{data[12]}','{data[13]}','{data[14]}','{data[15]}','{data[16]}','{data[17]}','{data[18]}','{data[19]}','{data[20]}','{data[21]}','{data[22]}','{data[23]}','{data[24]}','{data[25]}'"
        print('QUERY INSERT HELPDESK REPORT')
        cursor.execute(query)
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
            
def helper_convert_dict_to_array(data_dict):
    columns = list(data_dict.keys())
    values = [data_dict.get(col, '') for col in columns]
    
    return values