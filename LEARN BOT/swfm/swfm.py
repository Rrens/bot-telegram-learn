import os
import logging
from dotenv import load_dotenv
import telebot
from telebot import types
import mysql.connector
from mysql.connector import Error
# from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup,InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler,CallbackQueryHandler

load_dotenv()

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(os.getenv('TOKEN_BOT'))
# print(bot)

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
    
def get_all_data_helpdesk(id):
    try:
        create_connection()
        
        connection = create_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = f"select * from helpdesk_bot_swfm where chatid_telegram = '{id}' LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except:
        print(f"Error : {e}")
    
@bot.message_handler(commands=['start'])
def start(message):
    full_name = message.from_user.full_name
    username = message.from_user.username
    chatid_telegram  = message.from_user.id 
    grup_name = message.chat.title
    
    msg = message.chat.id
    
    syanticbot = 'https://t.me/syanticbot'
    
    info_message = (
        f"Full Name: {full_name}\n"
        f"Username: {username}\n"
        f"Chat ID Telegram: {chatid_telegram}\n"
        f"Group Name: {grup_name}\n"
    )
    print(info_message)
    
    
    result = get_all_data_helpdesk(chatid_telegram)
    print(f"INI DATA NYA \n {result}")

    bot.send_chat_action(msg, 'typing')
    button1 = types.InlineKeyboardButton("SYANTIC BOT", url=syanticbot)
    buttons = [[button1]]
    keyboard = types.InlineKeyboardMarkup(buttons)
    
    info_message = '*SYANTIC BOT* hanya bisa di akses melalui private chatBOT. Terima kasih \nKlik tombol dibawah ini'
    bot.send_message(msg, info_message, parse_mode='Markdown', reply_markup=keyboard)
    
print('bot start running')

bot.polling()