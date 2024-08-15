import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import os
import json
from utils.helper import *
from config.config import *
import logging
from database.db import insert_user

def create_user(update: Update, context: CallbackContext) -> None:
    # print(f"INI LOO {check_callback_query(update)}")
    try:
        if check_callback_query(update):
            message_text = update.message.text
            username = update.message.from_user.username
            # print(f"INI BUKAN CALLBACK QUERY, DATA USERNAME: {username}")
            # print(update.message)
            _, username_telegram, chat_id, system_type, role = message_text.split(' ')
            # print(f"USERNAME TELEGRAM: {username_telegram}")
            # print(f"CHAT ID: {chat_id}")
            # print(f"SYSTEM TYPE: {system_type}")
            # print(f"SYSTEM TYPE: {system_type}")
            # print(f"ROLE: {role}")
            
            # print(update.message.from_user.id)
            if(is_whitelisted(username)):
                # print('anda berhasil masuk')
                # print(insert_user(username_telegram, chat_id, system_type, role))
                process_insert_user = insert_user(username_telegram, chat_id, system_type, role)
                print(process_insert_user)
                if(process_insert_user == "True"):    
                    safe_username = convert_safe_username(username_telegram)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f"User {safe_username} Successfully added",parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f"User telah tersedia!",parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                print('mohon maaf anda tidak memiliki akses')
        else:
            query = update.callback_query
            query.answer()
            username_telegram = update.callback_query.from_user.username
            
            if(is_whitelisted(username_telegram)):
                print('anda berhasil masuk')
            else:
                query.message.reply_text(f"mohon maaf anda tidak memiliki akses",parse_mode=telegram.ParseMode.MARKDOWN)
                print('mohon maaf anda tidak memiliki akses')
    except Exception as e:
        print(f"Error: {e}")
    
def is_whitelisted(telegram_id: int) -> bool:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        whitelist_path = os.path.join(script_dir, '../whitelist.txt')
        
        os.chmod(whitelist_path, 0o755)
        
        print(f"Path whitelist.txt: {whitelist_path}")
        
        print(check_file_permissions(whitelist_path))
        
        with open(whitelist_path, 'r') as file:
            whitelist = file.read().splitlines()
        
        return str(telegram_id) in whitelist
    except FileNotFoundError:
        print('File whitelist.txt tidak ditemukan.')
        return False
    except Exception as e:
        print(f'Error: {e}')
        return False
    
def check_file_permissions(file_path):
    if os.access(file_path, os.R_OK):
        print("File dapat dibaca.")
    else:
        print("File tidak dapat dibaca.")
    
    if os.access(file_path, os.W_OK):
        print("File dapat ditulis.")
    else:
        print("File tidak dapat ditulis.")
    
    if os.access(file_path, os.X_OK):
        print("File dapat dieksekusi.")
    else:
        print("File tidak dapat dieksekusi.")
