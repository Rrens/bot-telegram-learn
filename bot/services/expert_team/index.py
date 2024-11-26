import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import os
import json
from config.config import *
from database.db import get_count_ioms, get_count_ioms, insert_helpdesk_expert, get_expert, get_count_expert_ioms
from utils.helper import edit_message, delete_message
from services.log_bot import log_bot_success_inline, log_bot_success

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
            [InlineKeyboardButton("Hapus >>", callback_data=str(END_EXPERT))],
            [InlineKeyboardButton("Kembali", callback_data=str(MAIN_MENU))],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        query.message.reply_text("Pilih :", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        
def reg_expert(update: Update, _: CallbackContext) -> None:
    try:
        count_data = get_count_ioms()
        query = update.callback_query
        select_data = query.data
        data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
        data = json.loads(data)
        for data in data['inline_keyboard']:
            if data['callback_data'] == select_data:
                data_text = str(data['text']).replace(" >>","")
        edit_message(query, data_text)
        
        if count_data == 0 or count_data == 1 or count_data == 2 or count_data == 3 or count_data == 4 or count_data == 5 or count_data == 6 or count_data == 7 or count_data == 8 or count_data == 9:
            query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 3\nKlik /cancel untuk membatalkan")
            print('yang ini')
            return END_EXPERT
        elif count_data == 10:
            query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 2\nKlik /cancel untuk membatalkan")
            return END_EXPERT
        elif count_data == 11:
            query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 1\nKlik /cancel untuk membatalkan")
            return END_EXPERT
        elif count_data == 12 or count_data == 13:
            query.message.reply_text("Registrasi Tim Ahli telah mencapai maksimum\nKlik /start")
            log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Registrasi telah mencapai maksimum')
            return ConversationHandler.END
            
    except Exception as e:
        print(f"Error: {e}")
        keyboard = [
            [InlineKeyboardButton("Registrasi >>", callback_data=str(REG_EXPERT))],
            [InlineKeyboardButton("Hapus >>", callback_data=str(END_EXPERT))],
            [InlineKeyboardButton("Kembali", callback_data=str(MAIN_MENU))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Anda memilih : *Tim Ahli*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
      
def get_del_fm():
    text = ''
    text += 'Expert Aktif :'
    text += '\n'
    data = get_expert()
    data_list = str(data).split('\\n')
    data_list = str(data_list).replace("['","").replace("']","").split('\\n')
    for data in data_list:
        check_username = f"├ {data}"
        text += check_username
        text += '\n'
    text += '\n'
    return text

def splitting(return_text):
    c, text = 0, ""
    return_list = []
    for line in return_text.splitlines():
        c += len(line)
        if c >= 3000:
            return_list.append(text)
            c, text = 0, ""
        text += line+"\n"
    return_list.append(text)
    return return_list

def del_expert(update: Update, _: CallbackContext) -> None:
    try:
        return_text = get_del_fm()
        query = update.callback_query
        select_data = query.data
        data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
        data = json.loads(data)
        for data in data['inline_keyboard']:
            if data['callback_data'] == select_data:
                data_text = str(data['text']).replace(" >>","")
        edit_message(query, data_text)
        
        check_status = get_count_ioms()
        check_status = check_status == 0
        query = update.callback_query
        query.answer()
        if check_status is True:
            query.message.reply_text("Username ID telegram tidak ditemukan\nKlik /menu", parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
            return ConversationHandler.END
        elif check_status is False:
            for cmdOUT in splitting(return_text):
                query.message.reply_text(cmdOUT, disable_web_page_preview=True)
            query.message.reply_text("Hapus username ID telegram dan gunakan spasi setiap user jika lebih dari satu, maksimum 3 user\nKlik /cancel untuk membatalkan")
            return END_DEL_EXPERT
        
    except Exception as e:
        print(f"Error: {e}")
        
def end_reg_expert(update: Update, _:CallbackContext) -> None:
    count_data = get_count_ioms()
    print(f"Count Data END: {count_data}")
    parameter_user =  update.message.text.split()
    count_user =  len(update.message.text.split())
    print(f"Parameter User: {parameter_user}")
    print(f"Count User: {count_user}")
    try:
        if count_data == 0 or count_data == 1 or count_data == 2 or count_data == 3 or count_data == 4 or count_data == 5 or count_data == 6 or count_data == 7:
            if count_user == 1:
                insert_helpdesk_expert(parameter_user[0])
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /start")
                print(f"PARAMETER USER AFTER: {parameter_user[0]}")
                log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            elif count_user == 2:
                insert_helpdesk_expert(parameter_user[0])
                insert_helpdesk_expert(parameter_user[1])
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /start")
                log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            elif count_user == 3:
                insert_helpdesk_expert(parameter_user[0])
                insert_helpdesk_expert(parameter_user[1])
                insert_helpdesk_expert(parameter_user[2])
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /start")
                log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            else:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 3\nKlik /start")
                log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 3')
        elif count_data == 10:
            try:
                if count_user == 1:
                    insert_helpdesk_expert(parameter_user[0])
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("✅ Berhasil Registrasi\nKlik /start")
                    log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
                elif count_user == 2:
                    insert_helpdesk_expert(parameter_user[0])
                    insert_helpdesk_expert(parameter_user[1])
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("✅ Berhasil Registrasi\nKlik /start")
                    log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 2\nKlik /start")
                    log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 2')
            except:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 2\nKlik /start")
                log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 2')
        elif count_data == 11:
            try:
                if count_user == 1:
                    insert_helpdesk_expert(parameter_user[0])
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("✅ Berhasil Registrasi\nKlik /start")
                    log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 1\nKlik /start")
                    log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 1')
            except:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 1\nKlik /start")
                log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 1')
        elif count_data == 12 or count_data == 13:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, Username ID telah mencapai maksimum 10\nKlik /start")
            log_bot_success_inline(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 10')
        return ConversationHandler.END
    except Exception as e:
        print(f"Error: {e}")
        
def end_del_reg_expert(update: Update, _: CallbackContext) -> None:
    parameter_user =  update.message.text.split()
    count_user =  len(update.message.text.split())
    if count_user == 1:
        check_status = get_count_expert_ioms(parameter_user[0])
        check_status_1 = check_status == 0
        if check_status_1 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
        else:
            # 