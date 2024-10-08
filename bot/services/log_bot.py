import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import os
import json
from database.db import get_expert, get_current_data_helpdesk
from config.config import *
import time

bot_log = telegram.Bot(token=TOKEN_BOT)
chatid_app = '-1002137089074'

def log_bot(update: Update):
    data = get_expert('ioms')
    chatid_telegram  = update.message.from_user.id 
    current_app = 'IOMS'
    current_path = os.getcwd()
    log_expert_path = os.path.join(current_path, 'data_log', 'log_expert.txt')
    
    if(os.path.exists(log_expert_path)):
        os.remove(log_expert_path)
        time.sleep(1)
    else:
        print("The file does not exist")
        time.sleep(1)
    
    data = get_expert('IOMS')
    log_bot = open(log_expert_path, 'a')
    log_bot.write(",{}".format(data))
    log_bot.close()
    
    try:    
        if(os.path.exists(log_expert_path)):
            data_expert = open(log_expert_path, 'r')
            data_expert = data_expert.read().split(',')
            del data_expert[0]
            data_expert = str(data_expert).replace("['","").replace("']","").split('\\n')
            count_expert = len(data_expert)
            print(f"COUNT EXPERT {count_expert}")
            if data_expert[0] == '':
                data = get_current_data_helpdesk(chatid_telegram)
                fullname = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 1:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 2:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 3:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 4:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 5:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_name_5 = str(data_expert[4])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                to_5 = 'https://t.me/{}'.format(data_expert[4])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 6:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_name_5 = str(data_expert[4])
                to_name_6 = str(data_expert[5])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                to_5 = 'https://t.me/{}'.format(data_expert[4])
                to_6 = 'https://t.me/{}'.format(data_expert[5])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 7:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_name_5 = str(data_expert[4])
                to_name_6 = str(data_expert[5])
                to_name_7 = str(data_expert[6])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                to_5 = 'https://t.me/{}'.format(data_expert[4])
                to_6 = 'https://t.me/{}'.format(data_expert[5])
                to_7 = 'https://t.me/{}'.format(data_expert[6])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 8:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_name_5 = str(data_expert[4])
                to_name_6 = str(data_expert[5])
                to_name_7 = str(data_expert[6])
                to_name_8 = str(data_expert[7])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                to_5 = 'https://t.me/{}'.format(data_expert[4])
                to_6 = 'https://t.me/{}'.format(data_expert[5])
                to_7 = 'https://t.me/{}'.format(data_expert[6])
                to_8 = 'https://t.me/{}'.format(data_expert[7])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 9:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_name_5 = str(data_expert[4])
                to_name_6 = str(data_expert[5])
                to_name_7 = str(data_expert[6])
                to_name_8 = str(data_expert[7])
                to_name_9 = str(data_expert[8])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                to_5 = 'https://t.me/{}'.format(data_expert[4])
                to_6 = 'https://t.me/{}'.format(data_expert[5])
                to_7 = 'https://t.me/{}'.format(data_expert[6])
                to_8 = 'https://t.me/{}'.format(data_expert[7])
                to_9 = 'https://t.me/{}'.format(data_expert[8])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 10:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_name_5 = str(data_expert[4])
                to_name_6 = str(data_expert[5])
                to_name_7 = str(data_expert[6])
                to_name_8 = str(data_expert[7])
                to_name_9 = str(data_expert[8])
                to_name_10 = str(data_expert[9])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                to_5 = 'https://t.me/{}'.format(data_expert[4])
                to_6 = 'https://t.me/{}'.format(data_expert[5])
                to_7 = 'https://t.me/{}'.format(data_expert[6])
                to_8 = 'https://t.me/{}'.format(data_expert[7])
                to_9 = 'https://t.me/{}'.format(data_expert[8])
                to_10 = 'https://t.me/{}'.format(data_expert[9])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 11:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_name_5 = str(data_expert[4])
                to_name_6 = str(data_expert[5])
                to_name_7 = str(data_expert[6])
                to_name_8 = str(data_expert[7])
                to_name_9 = str(data_expert[8])
                to_name_10 = str(data_expert[9])
                to_name_11 = str(data_expert[10])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                to_5 = 'https://t.me/{}'.format(data_expert[4])
                to_6 = 'https://t.me/{}'.format(data_expert[5])
                to_7 = 'https://t.me/{}'.format(data_expert[6])
                to_8 = 'https://t.me/{}'.format(data_expert[7])
                to_9 = 'https://t.me/{}'.format(data_expert[8])
                to_10 = 'https://t.me/{}'.format(data_expert[9])
                to_11 = 'https://t.me/{}'.format(data_expert[10])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 12:
                data = get_current_data_helpdesk(chatid_telegram)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = current_app
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_name_5 = str(data_expert[4])
                to_name_6 = str(data_expert[5])
                to_name_7 = str(data_expert[6])
                to_name_8 = str(data_expert[7])
                to_name_9 = str(data_expert[8])
                to_name_10 = str(data_expert[9])
                to_name_11 = str(data_expert[10])
                to_name_12 = str(data_expert[11])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                to_5 = 'https://t.me/{}'.format(data_expert[4])
                to_6 = 'https://t.me/{}'.format(data_expert[5])
                to_7 = 'https://t.me/{}'.format(data_expert[6])
                to_8 = 'https://t.me/{}'.format(data_expert[7])
                to_9 = 'https://t.me/{}'.format(data_expert[8])
                to_10 = 'https://t.me/{}'.format(data_expert[9])
                to_11 = 'https://t.me/{}'.format(data_expert[10])
                to_12 = 'https://t.me/{}'.format(data_expert[11])
                bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_app,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11}), [{to_name_12}]({to_12})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)    
    except Exception as e:
        print(f"ERROR: {e}")        
    
def log_bot_success(update: Update, message):
    try:
        username = 'https://t.me/{}'.format(update.message.from_user.username)
        full_name = update.message.from_user.full_name
        grup_name = update.message.chat.title
        if grup_name:
            bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
            bot_log.send_message(chat_id=chatid_app,text=f'🟠 *[#LOG_SUKSES_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {message}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        elif not grup_name:
            bot_log.sendChatAction(chat_id=chatid_app,action=telegram.ChatAction.TYPING)
            bot_log.send_message(chat_id=chatid_app,text=f'🟠 *[#LOG_SUKSES_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {message}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    except Exception as e:
        print(f"ERROR: {e}")  
    