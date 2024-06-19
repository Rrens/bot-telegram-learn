import os
from dotenv import load_dotenv
import telebot
import mysql.connector

load_dotenv()

db_config = {
    'user': os.getenv('db_user'),
    'password': os.getenv('db_pass'),
    'host': os.getenv('db_host'),
    'database': os.getenv('db_name'),
}

# print(os.getenv('db_user'), os.getenv('db_pass'), os.getenv('db_host'), os.getenv('db_name'))

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
    
def save_session(user_id):
    try:
        connection = create_connection()
        if connection is None:
            return False
        
        cursor = connection.cursor()
        insert_query = "INSERT INTO sessions (user_id, is_logged_in) VALUES (%s, %s) ON DUPLICATE KEY UPDATE is_logged_in = VALUES(is_logged_in)"
        cursor.execute(insert_query, (user_id, True))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return True
    except Exception as e:
        print(f"Error Save Session: {e}")
        return None

def is_user_authorized(username, password):
    try:
        connection = create_connection()
        if connection is None:
            return False
        
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return result is not None
    except Exception as e:
        print(f"Error Authorized: {e}")
        return None
    
def get_user_id(username):
    # print(f"SELECT user_id FROM users WHERE username = '{username}'")
    try:
        connection = create_connection()
        if(connection is None):
            return None
        
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        # print(result)
        cursor.close()
        connection.close()
        return result[0] if result else None
    
    except Exception as e:
        print(f"Error get userID: {e}")
        return None
    
def is_user_logged_in(user_id):
    try:
        connection = create_connection()
        if(connection is None):
            return None
        cursor = connection.cursor()
        
        cursor.execute("SELECT is_logged_in FROM sessions WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return result is not None and result[0] == True
    except Exception as e:
        print(f"Error Check User Logged in: {e}")
        return None

# def login_user(user_id):
#     try: 
#         connection = create_connection()
#         if(connection is None):
#             return None
#         cursor = connection.cursor()
        
#         cursor.execute("REPLACE INTO login_status (user_id, status) VALUES (%s, %s)", (user_id, True))
#         connection.commit()
#         cursor.close()
#         connection.close()
#         return True
#     except Exception as e:
#         print(f"Error login user: {e}")
#         return None
    
def logout_user(user_id):
    try:
        connection = create_connection()
        if (connection is None):
            return None
        cursor = connection.cursor()
        cursor.execute("UPDATE sessions SET is_logged_in = False WHERE user_id = %s", (user_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return True
    except Exception as e:
        print(f"Error logout user: {e}")
        return None

bot = telebot.TeleBot(os.getenv('TOKEN_BOT'))

sessions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Selamat datang! Gunakan /login (username)/(password) untuk login.')
    
    
@bot.message_handler(commands=['login'])
def handle_login(message): 
    # print(message)
    # print(message.text.startswith('/login '))
    if message.text.startswith('/login '):
        try:
            _, credentials = message.text.split(' ', 1)
            username, password = credentials.split('/')
        except ValueError:
            bot.reply_to(message.chat.id, "Format Salah, ketik 'login username/password'")
            return
        
        if message.from_user.id in sessions and sessions[message.from_user.id]:
            bot.reply_to(message, "Anda sudah login.")
            return
    
        if is_user_authorized(username, password):
            user_id = get_user_id(username)
            sessions[message.from_user.id] = user_id
            save_session(user_id)
            
            bot.reply_to(message, "Login berhasil.")
            
        else: 
            bot.reply_to(message, "Username atau password salah.")
        # user_id = get_user_id(username)
        # if user_id and is_user_authorized(username, password): 
        #     if login_user(user_id):
        #         bot.send_message(message.chat.id, "Anda Berhasil Login")
        #         print('Login Sukses %s', (username))
        #     else:
        #         bot.send_message(message.chat.id, "Terjadi kesalahan saat login. Coba lagi nanti.")
        #         print('Login Gagal %s', (username))
        # else:
        #     bot.send_message(message.chat.id, "Username atau password salah.")
        #     print('Username/password salah %s/%s', (username, password))
    else:
        bot.send_message(message.chat.id, "Perintah tidak dikenali. Ketik 'login username/password' untuk login.")
        
@bot.message_handler(commands=['logout'])
def handle_logout(message):
    
    try:
        if message.from_user.id in sessions and sessions[message.from_user.id]:
            logout_user(sessions[message.from_user.id])
            sessions[message.from_user.id] = None
            bot.reply_to(message, "Logout berhasil.")
        else:
            bot.reply_to(message, "Anda belum login.")
    except Exception as e:
        print(f"Error handling logout: {e}")
        bot.reply_to(message, "Terjadi kesalahan saat logout. Coba lagi nanti.")
    # user_id = message.from_user.id
    # if is_user_logged_in(user_id):
    #     if logout_user(user_id):
    #         bot.send_message(message.chat.id, "Anda Berhasil Logout")
    #     else:
    #         bot.send_message(message.chat.id, "Terjadi kesalahan saat logout. Coba lagi nanti.")
    # else:
    #     bot.send_message(message.chat.id, "Anda belum login. Ketik /login (username)/(password) untuk login.")
        
        
@bot.message_handler(commands=['check'])
def check_login(message):
    try:
        if message.from_user.id in sessions and sessions[message.from_user.id]:
            bot.reply_to(message, "Anda sudah login.")
        else:
            bot.reply_to(message, "Anda belum login.")
    except Exception as e:
        print(f"Error checking login: {e}")
        bot.reply_to(message, "Terjadi kesalahan saat memeriksa login.")
    # user_id = message.from_user.id
    # if is_user_logged_in(user_id):
    #     bot.send_message(message.chat.id, "Anda sudah login")
    # else:
    #     bot.send_message(message.chat.id, "Anda belum login. Ketik /login (username)/(password) untuk login.")
    
    
print('bot start running')

bot.polling()
