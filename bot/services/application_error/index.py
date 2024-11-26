import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config.config import *
from utils.helper import edit_message, delete_message
import json

def application_error(udate: Update, _: CallbackContext) -> None:
    query = Update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    print(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    delete_message(chat_id, message_id)
    edit_message(query, data_text)
    
    keyboard = [
            [InlineKeyboardButton("(Loading Setelah Login)", callback_data=str(MAIN_MENU))],
            [InlineKeyboardButton("Log out Yourself (Logout Sendiri)", callback_data=str(MAIN_MENU))],
            [InlineKeyboardButton("Hang (Gantung)", callback_data=str(MAIN_MENU))],
            # [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(REPORT_PROBLEM))],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Pilih :",reply_markup=reply_markup)

