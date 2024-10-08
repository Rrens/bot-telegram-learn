import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from dotenv import load_dotenv
import os
load_dotenv()
# TOKEN_BOT = os.getenv('TOKEN_BOT')
TOKEN_BOT = '7048693889:AAHOk6XHLsrFj5vwShHH7Le1CugmjF7t2V0'
bot_log = telegram.Bot(token=TOKEN_BOT)


def edit_message(query, message): 
    return query.edit_message_text(f"Anda memilih : *{message}*",parse_mode=telegram.ParseMode.MARKDOWN)

def delete_message(chat_id, message_id):
    return bot_log.delete_message(chat_id, message_id)