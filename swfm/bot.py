import logging
import telebot
import os
from telebot import types
from database.db import get_current_data_helpdesk

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

TOKEN_BOT = os.getenv('TOKEN_BOT')

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN_BOT)

@bot.message_handler(commands=['start'])
def start(message):
    full_name = message.from_user.full_name
    username = message.from_user.username
    chatid_telegram = message.from_user.id 
    grup_name = message.chat.title
    
    msg = message.chat.id
    
    syanticbot = 'https://t.me/syanticbot'
    
    info_message = (
        f"Full Name: {full_name}\n"
        f"Username: {username}\n"
        f"Chat ID Telegram: {chatid_telegram}\n"
        f"Group Name: {grup_name}\n"
    )
    
    result = get_current_data_helpdesk(chatid_telegram)
    print(f"INI DATA NYA \n {result}")

    bot.send_chat_action(msg, 'typing')
    button1 = types.InlineKeyboardButton("SYANTIC BOT", url=syanticbot)
    buttons = [[button1]]
    keyboard = types.InlineKeyboardMarkup(buttons)
    
    info_message = '*SYANTIC BOT* hanya bisa diakses melalui private chatBOT. Terima kasih \nKlik tombol di bawah ini'
    bot.send_message(msg, info_message, parse_mode='Markdown', reply_markup=keyboard)
    
print('bot start running')

bot.polling()