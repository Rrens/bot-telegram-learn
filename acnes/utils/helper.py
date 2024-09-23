import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_BOT')
bot_log = telegram.Bot(token=TOKEN_BOT)

def edit_message(query, message): 
    return query.edit_message_text(f"Anda memilih : *{message}*",parse_mode=telegram.ParseMode.MARKDOWN)

def delete_message(chat_id, message_id):
    return bot_log.delete_message(chat_id, message_id)