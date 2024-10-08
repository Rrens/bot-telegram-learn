import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import os
import json
from config.config import *
from utils.helper import edit_message, delete_message
from database.db import alter_problem_title, get_problem_title

def expert_team(update: Update, context: CallbackContext) -> None:
    try:
        query = update.callback_query
        chatid_telegram = query.from_user.id
        select_data = query.data
        data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
        data = json.loads(data)
        for data in data['inline_keyboard']:
            if data['callback_data'] == select_data:
                data_text = str(data['text']).replace(" >>","")
        
        edit_message(query, data_text)
        
        keyboard = [
            [InlineKeyboardButton("Registrasi >>", callback_data=str(REG_EXPERT))],
            [InlineKeyboardButton("Hapus >>", callback_data=str(DEL_EXPERT))],
            [InlineKeyboardButton("Kembali", callback_data=str(MAIN_MENU))],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        query.message.reply_text("Pilih :", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")