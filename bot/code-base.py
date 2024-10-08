#!/usr/bin/env python
import logging
import telegram
import ssl
import clickhouse_connect
import os
import requests
import time
import json
import string
import random
import gspread
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import ssl
import re

import pandas as pd
from datetime import datetime
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler,CallbackQueryHandler

# os.environ['https_proxy'] = 'https://10.37.190.29:8080'
os.environ['HTTPS_PROXY'] = 'https://10.37.190.30:8080'

ssl._create_default_https_context = ssl._create_unverified_context
disable_warnings(InsecureRequestWarning)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
token_bot = '6782119374:AAGhKVO2AU10YumwgB7q2I_z9YooyyYqgfU' #SWFMBOT DEV
# token_bot = '1087167235:AAGahG5GsxkffRCbns9S-aXwklzyGYHlpME' #SYANTIC PROD
log_bot = token_bot
chat_id = '-1001817361687'
chatid_user = '-1002081232778'

chatid_ioms = '-1002137089074'
chatid_ipas1 = '-1002088766210'
chatid_ipas2 = '-1002007337700'
chatid_ipas3 = '-1002022820741'
chatid_ipas4 = '-1002050023405'
chatid_ipas6 = '-1002075042626'
chatid_ipas5 = '-1002087638486'
chatid_ipas7 = '-1002249694558'

chatid_1 = '-1002070465118'#BPS Manual
chatid_2 = '-1002139229053'#KPI
chatid_3 = '-1002114331977'#Mobile
chatid_4 = '-1002059298694'#Preventive Maintenance
chatid_5 = '-1002003516591'#Site Refference
chatid_6 = '-1002063164323'#Teritory Operation
chatid_7 = '-1002070624472'#Ticketing Handling
chatid_8 = '-1002143119827'#TS Manual
chatid_9 = '-1002083468096'#User Management
chatid_10 = '-1002040246878'#Other Problems
chatid_11 = '-1002130554661'#CGL (IMBAS PETIR)
chatid_12 = '-1002108737074'#RH Visit
chatid_13 = '-1001803293223'#Cant Check In
chatid_14 = '-1002057172625'#Aplication Error
chatid_15 = '-1002185711816'#ANT
chatid_16 = '-1002186914445'#Master Data Management
chatid_17 = '-1002206801426'#Performance
chatid_18 = '-1002223856855'#TPAS
chatid_19 = '-1002218019812'#TANYA PROSES ?


bot_log = telegram.Bot(token=log_bot)

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

# ssl._create_default_https_context = ssl._create_unverified_context

#LOG
def log_bot_regis_ioms(update: Update, perintah):
    username = update.message.from_user.username
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'⚠️ [#LOG_REGISTRASI_GAGAL_IOMS_SCARLETT] pesan dari @{username} dengan pesan {perintah}', disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'⚠️ [#LOG_REGISTRASI_GAGAL_IOMS_SCARLETT] pesan dari @{username} dengan pesan {perintah}', disable_web_page_preview=True)
def log_bot_fail_ioms_scarlett(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.message.from_user.username)
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🔴 *[#LOG_GAGAL_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🔴 *[#LOG_GAGAL_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_fail_inline_ioms_scarlett(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.callback_query.from_user.username)
    full_name = update.callback_query.from_user.full_name
    bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
    bot_log.send_message(chat_id=chat_id,text=f'🔴 *[#LOG_GAGAL_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_success_ioms_scarlett(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.message.from_user.username)
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟢 *[#LOG_SUKSES_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟢 *[#LOG_SUKSES_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_success_ioms_com(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.message.from_user.username)
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟠 *[#LOG_SUKSES_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟠 *[#LOG_SUKSES_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_success_inline_ioms_scarlett(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.callback_query.from_user.username)
    full_name = update.callback_query.from_user.full_name
    bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
    bot_log.send_message(chat_id=chat_id,text=f'🟢 *[#LOG_SUKSES_IOMS_SCARLETT]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

def log_bot_regis_ipas(update: Update, perintah):
    username = update.message.from_user.username
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'⚠️ [#LOG_REGISTRASI_GAGAL_IPAS] pesan dari @{username} dengan pesan {perintah}', disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'⚠️ [#LOG_REGISTRASI_GAGAL_IPAS] pesan dari @{username} dengan pesan {perintah}', disable_web_page_preview=True)
def log_bot_fail_ipas(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.message.from_user.username)
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🔴 *[#LOG_GAGAL_IPAS]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🔴 *[#LOG_GAGAL_IPAS]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_fail_inline_ipas(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.callback_query.from_user.username)
    full_name = update.callback_query.from_user.full_name
    bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
    bot_log.send_message(chat_id=chat_id,text=f'🔴 *[#LOG_GAGAL_IPAS]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_success_ipas(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.message.from_user.username)
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟢 *[#LOG_SUKSES_IPAS]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟢 *[#LOG_SUKSES_IPAS]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_success_ipas_com(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.message.from_user.username)
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟠 *[#LOG_SUKSES_IPAS]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟠 *[#LOG_SUKSES_IPAS]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_success_inline_ipas(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.callback_query.from_user.username)
    full_name = update.callback_query.from_user.full_name
    bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
    bot_log.send_message(chat_id=chat_id,text=f'🟢 *[#LOG_SUKSES_IPAS]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

def log_bot_regis_swfm(update: Update, perintah):
    username = update.message.from_user.username
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'⚠️ [#LOG_REGISTRASI_GAGAL_SWFM] pesan dari @{username} dengan pesan {perintah}', disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'⚠️ [#LOG_REGISTRASI_GAGAL_SWFM] pesan dari @{username} dengan pesan {perintah}', disable_web_page_preview=True)
def log_bot_fail_swfm(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.message.from_user.username)
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🔴 *[#LOG_GAGAL_SWFM]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🔴 *[#LOG_GAGAL_SWFM]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_fail_inline_swfm(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.callback_query.from_user.username)
    full_name = update.callback_query.from_user.full_name
    bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
    bot_log.send_message(chat_id=chat_id,text=f'🔴 *[#LOG_GAGAL_SWFM]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_success_swfm(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.message.from_user.username)
    print(f"log_bot_success {username}")
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟢 *[#LOG_SUKSES_SWFM]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟢 *[#LOG_SUKSES_SWFM]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_success_swfm_com(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.message.from_user.username)
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    if grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟠 *[#LOG_SUKSES_SWFM]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    elif not grup_name:
        bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
        bot_log.send_message(chat_id=chat_id,text=f'🟠 *[#LOG_SUKSES_SWFM]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
def log_bot_success_inline_swfm(update: Update, perintah):
    username = 'https://t.me/{}'.format(update.callback_query.from_user.username)
    full_name = update.callback_query.from_user.full_name
    bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
    bot_log.send_message(chat_id=chat_id,text=f'🟢 *[#LOG_SUKSES_SWFM]* pesan dari [{full_name}]({username}) dengan pesan {perintah}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)



def log_bot_inline(update: Update, perintah):
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    full_name  = update.callback_query.from_user.full_name 
    chatid_telegram  = update.callback_query.from_user.id 
    tools = str(perintah)
    check_userswfm = tools == 'USER SWFM'

    if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt"):
        os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt")
        time.sleep(1)
    else:
        print("The file does not exist")
        time.sleep(1)

    if check_userswfm is True:
        query = f"select expert from production.helpdesk_expert where application_name = 'SWFM'"
        data = client.command(query)
        log_bot = open('/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt','a')
        log_bot.write(",{}".format(data))
        log_bot.close()
        if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt"):
            data_expert = open('/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt','r')
            data_expert = data_expert.read().split(',')
            del data_expert[0]
            data_expert = str(data_expert).replace("['","").replace("']","").split('\\n')
            count_expert = len(data_expert)
            if data_expert[0] == '' :
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',') 
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : -\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 1:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
                to_name_1 = str(data_expert[0])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 2:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 3:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 4:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 5:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
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
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 6:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
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
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 7:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
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
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 8:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
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
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 9:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
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
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 10:
                today = datetime.now()
                date = today.strftime("%d-%m-%Y %H:%M:%S WIB")
                data_swfm = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','r')
                data_swfm = data_swfm.read().split(',')
                requests = 'https://t.me/{}'.format(data_swfm[1])
                email = (data_swfm[2]).replace('_',' ')
                no_hp = data_swfm[3]
                area = data_swfm[4]
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
                bot_log.sendChatAction(chat_id=chatid_user,action=telegram.ChatAction.TYPING)
                bot_log.send_message(chat_id=chatid_user,text=f'*{full_name}* has Requests Approval User with the following details:\n\nCreation Date : {date}\nNo HP : {no_hp}\nEmail : {email}\nArea : {area}\nRequestor : [{full_name}]({requests})\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nDear Admin : Tolong segera di Approve',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

def log_bot(update: Update, perintah):
    print(perintah)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    chatid_telegram  = update.message.from_user.id 
    tools = str(perintah)
    check_swfm = tools == 'SWFM'
    check_ioms = tools == 'IOMS'
    check_ipas = tools == 'IPAS'
    check_scarlett = tools == 'SCARLETT'
    

    if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt"):
        os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt")
        time.sleep(1)
    else:
        print("The file does not exist")
        time.sleep(1)
    
    if check_swfm is True:
        today = datetime.now()
        hours = today.strftime("%H")
        hours = int(hours)
        day = today.strftime("%d")
        day = int(day)
        gspread_client = gspread.service_account(filename="/home/dimas/baru/helpdeskbot_v2/data/handleby_form_api_spreedsheet.json")
        spreadsheets = gspread_client.openall()
        x_name = []
        if str(day) == '':
            print('Tanggal Tidak ada')
        elif spreadsheets:
            first_spreadsheet = spreadsheets[0]
            worksheet = first_spreadsheet.get_worksheet(0)
            data = worksheet.get_all_values()
            data_select = data[1:]
            
            for data in data_select:
                name = data[0]
                username = 'https://t.me/{}'.format(data[1])
                date = data[2]
                status = data[3]
                if date == str(day):
                    if hours in range(3, 17):
                        if status == 'PAGI' or status == 'WFO':
                            # x_name.append(f'[{name}]({username})')
                            x_name.append(f'{name}')
                            # print(f'Shift Pagi : {name}')
                    else:
                        if status == 'SIANG':
                            # x_name.append(f'[{name}]({username})')
                            x_name.append(f'{name}')
                            # print(f'Shift SIang : {name}')
        else:
            print("No spreadsheets available")
        # handle_with_link = str(x_name).replace("['","").replace("']","").replace("'","")
        # print(handle_with_link)
        handle_no_link = str(x_name).replace("['","").replace("']","").replace("'","")
        
        if handle_no_link == '[]':
            pass
        else:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
            data_select1 = client.command(query)
            data_select = str(data_select1).split(' ➞ ')[0].split('\\n')[0]

            query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
            data = client.command(query)
            full_name = str(data[0]).title()
            requests = 'https://t.me/{}'.format(data[1])
            no_hp = data[3]
            ticket = data[11]
            regional = str(data[13])
            problem_note = str(data[14])
            problem_note = problem_note.split('\\n')[0]
            problem__ = str(data[15]).replace('\\n',' ')
            date = str(data[18]).replace('-',' ')
            category = str(tools)
            # print(data_select)
            
            print('bener')
            print(problem_note.split('\\n')[0])
            
            if data_select == 'BPS Manual':
                bot_log.sendChatAction(chat_id=chatid_1,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'KPI':
                bot_log.sendChatAction(chat_id=chatid_2,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                
                # update.message.reply_text(text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                
            elif data_select == 'Mobile':
                bot_log.sendChatAction(chat_id=chatid_3,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'Preventive Maintenance':
                data_cat = str(data_select1).split(' ➞ ')[1]
                print(data_cat)
                if data_cat == 'Schedule Planning':
                    bot_log.sendChatAction(chat_id=chatid_4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nSOP Link : https://bit.ly/swfm-pm-schedule-planning\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_cat == 'PM Site':
                    bot_log.sendChatAction(chat_id=chatid_4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nSOP Link : https://bit.ly/swfm-pm-site\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_cat == 'PM Genset':
                    bot_log.sendChatAction(chat_id=chatid_4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nSOP Link : https://bit.ly/swfm-pm-genset\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                else:
                    bot_log.sendChatAction(chat_id=chatid_4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'Site Refference':
                bot_log.sendChatAction(chat_id=chatid_5,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'Teritory Operation':
                bot_log.sendChatAction(chat_id=chatid_6,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'Ticketing Handling':
                data_cat = str(data_select1).split(' ➞ ')[1]
                if data_cat == 'Personal Tracking':
                    bot_log.sendChatAction(chat_id=chatid_7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nSOP Link : https://bit.ly/swfm-personel-tracking\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_cat == 'Service Variable Activity':
                    bot_log.sendChatAction(chat_id=chatid_7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nSOP Link : https://bit.ly/swfm-service-variable-activity\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                else:
                    bot_log.sendChatAction(chat_id=chatid_7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'TS Manual':
                bot_log.sendChatAction(chat_id=chatid_8,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_8,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'User Management':
                bot_log.sendChatAction(chat_id=chatid_9,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_9,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, email, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'Other Problems':
                bot_log.sendChatAction(chat_id=chatid_10,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_10,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'CGL (IMBAS PETIR)':
                bot_log.sendChatAction(chat_id=chatid_11,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_11,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'RH Visit':
                bot_log.sendChatAction(chat_id=chatid_12,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_12,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'Cant Check In':
                bot_log.sendChatAction(chat_id=chatid_13,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_13,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'Aplication Error':
                bot_log.sendChatAction(chat_id=chatid_14,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_14,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'ANT':
                bot_log.sendChatAction(chat_id=chatid_15,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_15,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'Master Data Management':
                bot_log.sendChatAction(chat_id=chatid_16,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_16,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'Performance':
                bot_log.sendChatAction(chat_id=chatid_17,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_17,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'TPAS':
                bot_log.sendChatAction(chat_id=chatid_18,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_18,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif data_select == 'TANYA PROSES ?':
                bot_log.sendChatAction(chat_id=chatid_19,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_19,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}\nHandle by : {handle_no_link}\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi *nomor tiket, screenshoot, evidence problem atau eror* pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        id_channel = str(data.sender_chat.id)[4:]
        id_message = data.message_id
        post_link = 'https://t.me/c/{}/{}'.format(id_channel,id_message)
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_report_swfm update post_link = '{post_link}' where ticket = '{ticket}'"
        client.command(query)

    elif check_ioms is True or check_scarlett is True:
        query = f"select expert from production.helpdesk_expert where application_name = 'IOMS'"
        data = client.command(query)
        log_bot = open('/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt','a')
        log_bot.write(",{}".format(data))
        log_bot.close()
        if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt"):
            data_expert = open('/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt','r')
            data_expert = data_expert.read().split(',')
            del data_expert[0]
            data_expert = str(data_expert).replace("['","").replace("']","").split('\\n')
            count_expert = len(data_expert)
            if data_expert[0] == '' :
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 1:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                to_name_1 = str(data_expert[0])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 2:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 3:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 4:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 5:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 6:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 7:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 8:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 9:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 10:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 11:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 12:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                mitra = str(data[12])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                bot_log.sendChatAction(chat_id=chatid_ioms,action=telegram.ChatAction.TYPING)
                data = bot_log.send_message(chat_id=chatid_ioms,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nCompany : {mitra}\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11}), [{to_name_12}]({to_12})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        id_channel = str(data.sender_chat.id)[4:]
        id_message = data.message_id
        post_link = 'https://t.me/c/{}/{}'.format(id_channel,id_message)
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_report_swfm update post_link = '{post_link}' where ticket = '{ticket}'"
        client.command(query)
    
    elif check_ipas is True:
        query = f"select expert from production.helpdesk_expert where application_name = 'IPAS'"
        data = client.command(query)
        log_bot = open('/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt','a')
        log_bot.write(",{}".format(data))
        log_bot.close()
        if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt"):
            data_expert = open('/home/dimas/baru/helpdeskbot_v2/data_log/log_expert.txt','r')
            data_expert = data_expert.read().split(',')
            del data_expert[0]
            data_expert = str(data_expert).replace("['","").replace("']","").split('\\n')
            count_expert = len(data_expert)
            if data_expert[0] == '' :
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                data_select = str(data_select1).split(' ➞ ')[0].split('\\n')[0]
                print(f"================================== {data_select} ==================================")
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    query.message.reply_text(f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                    # data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : -\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 1:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                to_name_1 = str(data_expert[0])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 2:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 3:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 4:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
                to_name_1 = str(data_expert[0])
                to_name_2 = str(data_expert[1])
                to_name_3 = str(data_expert[2])
                to_name_4 = str(data_expert[3])
                to_1 = 'https://t.me/{}'.format(data_expert[0])
                to_2 = 'https://t.me/{}'.format(data_expert[1])
                to_3 = 'https://t.me/{}'.format(data_expert[2])
                to_4 = 'https://t.me/{}'.format(data_expert[3])
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 5:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 6:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 7:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 8:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 9:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 10:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 11:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            elif count_expert == 12:
                query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                data = client.command(query)
                full_name = str(data[0]).title()
                requests = 'https://t.me/{}'.format(data[1])
                no_hp = data[3]
                ticket = data[11]
                regional = str(data[13])
                problem_note = str(data[14])
                problem__ = str(data[15]).replace('\\n',' ')
                date = str(data[18]).replace('-',' ')
                category = str(tools)
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
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
                data_select = client.command(query)
                data_select = str(data_select).split(' ➞ ')[0]
                if data_select == 'Transport':
                    bot_log.sendChatAction(chat_id=chatid_ipas1,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas1,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11}), [{to_name_12}]({to_12})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Power':
                    bot_log.sendChatAction(chat_id=chatid_ipas2,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas2,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11}), [{to_name_12}]({to_12})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'ISR':
                    bot_log.sendChatAction(chat_id=chatid_ipas3,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas3,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11}), [{to_name_12}]({to_12})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Milik':
                    bot_log.sendChatAction(chat_id=chatid_ipas4,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas4,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11}), [{to_name_12}]({to_12})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Tower Sewa':
                    bot_log.sendChatAction(chat_id=chatid_ipas6,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas6,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11}), [{to_name_12}]({to_12})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'TANYA PROSES ?':
                    bot_log.sendChatAction(chat_id=chatid_ipas5,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas5,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11}), [{to_name_12}]({to_12})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif data_select == 'Aplication Error':
                    bot_log.sendChatAction(chat_id=chatid_ipas7,action=telegram.ChatAction.TYPING)
                    data = bot_log.send_message(chat_id=chatid_ipas7,text=f'*{full_name}* has open ticket with the following details:\n\nCreation Date : {date}\nApplication : #{category}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nHandle by : [{to_name_1}]({to_1}), [{to_name_2}]({to_2}), [{to_name_3}]({to_3}), [{to_name_4}]({to_4}), [{to_name_5}]({to_5}), [{to_name_6}]({to_6}), [{to_name_7}]({to_7}), [{to_name_8}]({to_8}), [{to_name_9}]({to_9}), [{to_name_10}]({to_10}), [{to_name_11}]({to_11}), [{to_name_12}]({to_12})\n\nMohon bantuan kak [{full_name}]({requests}), untuk melengkapi nomor tiket, screenshoot, evidence problem atau eror pada room diskusi !!!',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        id_channel = str(data.sender_chat.id)[4:]
        id_message = data.message_id
        post_link = 'https://t.me/c/{}/{}'.format(id_channel,id_message)
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_report_swfm update post_link = '{post_link}' where ticket = '{ticket}'"
        client.command(query)

    
### Button Commands
#KONDISI
def cancel_registration(update: Update, _: CallbackContext) -> int:
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Terima kasih telah akses di *SYANTIC BOT*\nKlik /start',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
def cancel_approval(update: Update, _: CallbackContext) -> int:
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Terima kasih telah akses di *SYANTIC BOT*\nKlik /start',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
def cancel_home(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    try:
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text="Terima kasih telah akses di *SYANTIC BOT*\nKlik /menu",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        query.edit_message_text(text="Terima kasih telah akses di *SYANTIC BOT*\nKlik /menu",parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END
def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Terima kasih telah akses di *SYANTIC BOT*\nKlik /menu', reply_markup=ReplyKeyboardRemove(),parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END
def timeout(update, context):
    try:
        first_name = update.message.from_user.first_name
        message_id = update.message.message_id+3
        chat_id = update.message.from_user.id
        bot_log.delete_message(chat_id,message_id)
        first_name = update.message.from_user.first_name
        message_id = update.message.message_id+2
        chat_id = update.message.from_user.id
        bot_log.delete_message(chat_id,message_id)
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text('Maaf Kak *{}*, session Anda sudah habis\nKlik /menu'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    except:
        try:
            first_name = update.message.from_user.first_name
            message_id = update.message.message_id+2
            chat_id = update.message.from_user.id
            bot_log.delete_message(chat_id,message_id)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Maaf Kak *{}*, session Anda sudah habis\nKlik /menu'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        except:
            try:
                first_name = update.message.from_user.first_name
                message_id = update.message.message_id+1
                chat_id = update.message.from_user.id
                bot_log.delete_message(chat_id,message_id)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text('Maaf Kak *{}*, session Anda sudah habis\nKlik /menu'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
            except:
                first_name = update.message.from_user.first_name
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text('Maaf Kak *{}*, session Anda sudah habis\nKlik /menu'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
def timeout_with_inline(update, context):
    try:
        first_name = update.callback_query.from_user.first_name
        chat_id = update.callback_query.message.chat_id
        message_id_1 = update.callback_query.message.message_id+1
        message_id_2 = update.callback_query.message.message_id+2
        bot_log.delete_message(chat_id,message_id_1)
        bot_log.delete_message(chat_id,message_id_2)
        query = update.callback_query
        query.answer()
        query.message.reply_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /menu'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)
    except telegram.error.BadRequest:
        try:
            first_name = update.callback_query.from_user.first_name
            chat_id = update.callback_query.message.chat_id
            message_id_3 = update.callback_query.message.message_id+3
            message_id_2 = update.callback_query.message.message_id+2
            bot_log.delete_message(chat_id,message_id_3)
            bot_log.delete_message(chat_id,message_id_2)
            query = update.callback_query
            query.answer()
            query.message.reply_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /menu'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)
        except telegram.error.BadRequest:
            try:
                first_name = update.callback_query.from_user.first_name
                chat_id = update.callback_query.message.chat_id
                message_id_2 = update.callback_query.message.message_id+2
                bot_log.delete_message(chat_id,message_id_2)
                query = update.callback_query
                query.answer()
                query.message.reply_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /menu'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)
            except telegram.error.BadRequest:
                try:
                    first_name = update.callback_query.from_user.first_name
                    query = update.callback_query
                    query.edit_message_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /menu'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)
                except telegram.error.BadRequest:
                    first_name = update.callback_query.from_user.first_name
                    chat_id = update.callback_query.message.chat_id
                    message_id_2 = update.callback_query.message.message_id+0
                    bot_log.delete_message(chat_id,message_id_2)
                    query = update.callback_query
                    query.answer()
                    query.message.reply_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /menu'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)

MENU_REGISTRATION, MENU_APPROVAL, MENU, PANDUAN,END_IOMS, REGISTRATION_IOMS_END, REGISTRATION_IPAS_END, END_SWFM, IOMS_BROADCAST_END, IPAS_BROADCAST_END, SWFM_BROADCAST_END, SWFM_MAKEADMIN_END, SWFM_USERBOT_END, END_REG_EXPERT_SWFM, END_DEL_EXPERT_SWFM, SWFM_MYTICKET_CLOSED, SWFM_MYTICKET_CLOSED_END, REGISTRATION_NOHP_SWFM,REGISTRATION_EMAILS_IOMS, REGISTRATION_EMAILS_IPAS, REGISTRATION_PWD_IOMS, REGISTRATION_EMAIL_SWFM, SWFM_MYTICKET_ERROR, SWFM_MYTICKET_PROCESS, END_REG_EXPERT_IOMS, END_DEL_EXPERT_IOMS, IOMS_MYTICKET_PROCESS, IOMS_MYTICKET_CLOSED, IOMS_MYTICKET_CLOSED_END, IPAS_MYTICKET_PROCESS, IPAS_MYTICKET_CLOSED, IPAS_MYTICKET_CLOSED_END, END_REG_EXPERT_IPAS, END_DEL_EXPERT_IPAS, END_IPAS,SWFM_COMPLAINT_END, IOMS_COMPLAINT_END, IPAS_COMPLAINT_END, IOMS_MAKEADMIN_END, IPAS_MAKEADMIN_END, END_SCARLETT, SCARLETT_MYTICKET_PROCESS, SCARLETT_MYTICKET_CLOSED, SCARLETT_MYTICKET_CLOSED_END, SCARLETT_COMPLAINT_END, REGISTRATION_PWD_IPAS, LDAP_NO_IPAS  = range(47)

REGISTRATION_TOOLS_IOMS, REGISTRATION_TOOLS_IPAS, REGISTRATION_IPAS, REGISTRATION_IPAS_END,REGISTRATION_TOOLS_SWFM, REGISTRATION_SWFM, REGISTRATION_IOMS, REGISTRATION_IOMS_MITRA, REGISTRATION_IPAS_MITRA, LDAP_NO_IOMS, CANCEL_HOME, MENU_SWFM, MENU_IOMS, MENU_IOMS_, MENU_IPAS, MENU_IPAS_, MENU_SCARLETT, MENU_SCARLETT_, MENU_UTAMA, IOMS_REQTICKET, IOMS_REQTICKET_, IOMS_CAT1, IOMS_CAT2, IOMS_CAT3, IOMS_CAT4, IOMS_CAT5, IOMS_CAT6, IOMS_CAT7, IOMS_CAT8, IOMS_CAT9, IOMS_CAT10, IOMS_CAT12, IOMS_CAT13, IOMS_CAT14, IOMS_CAT1_1, IOMS_CAT1_2, IOMS_CAT1_3, IOMS_CAT1_4, IOMS_CAT1_5, IOMS_CAT1_6, IOMS_CAT1_7, IOMS_CAT1_8, IOMS_CAT1_9, IOMS_CAT1_10, IOMS_CAT1_11, IOMS_CAT1_12, IOMS_CAT1_13, IOMS_CAT1_CASE_A_1, IOMS_CAT1_CASE_A_2, IOMS_CAT1_CASE_A_3, IOMS_CAT1_CASE_A_4, IOMS_CAT1_CASE_A_5, IOMS_CAT1_CASE_A_6, IOMS_CAT1_CASE_A_7, IOMS_CAT1_CASE_A_8, IOMS_CAT1_CASE_A_9, IOMS_CAT1_CASE_A1_1, IOMS_CAT1_CASE_A1_2, IOMS_CAT1_CASE_A1_3, IOMS_CAT1_CASE_A2_1, IOMS_CAT1_CASE_A2_2, IOMS_CAT1_CASE_A2_3, IOMS_CAT1_CASE_A2_4, IOMS_CAT1_CASE_A3_1, IOMS_CAT1_CASE_A3_2, IOMS_CAT1_CASE_A3_3, IOMS_CAT1_CASE_A4_1, IOMS_CAT1_CASE_A4_2, IOMS_CAT1_CASE_A4_3, IOMS_CAT1_CASE_A4_4, IOMS_CAT1_CASE_A5_1, IOMS_CAT1_CASE_A5_2, IOMS_CAT1_CASE_A5_3, IOMS_CAT1_CASE_A5_4, IOMS_CAT1_CASE_A5_5, IOMS_CAT1_CASE_A5_6, IOMS_CAT1_CASE_A5_7, IOMS_CAT1_CASE_A5_8, IOMS_CAT1_CASE_A5_9, IOMS_CAT1_CASE_A5_10, IOMS_CAT1_CASE_A5_11, IOMS_CAT1_CASE_A5_12, IOMS_CAT1_CASE_A5_13, IOMS_CAT1_CASE_A5_14, IOMS_CAT1_CASE_A5_15, IOMS_CAT1_CASE_A6_1, IOMS_CAT1_CASE_A6_2, IOMS_CAT1_CASE_A6_3, IOMS_CAT1_CASE_A6_4, IOMS_CAT1_CASE_A7_1, IOMS_CAT1_CASE_A7_2, IOMS_CAT1_CASE_A7_3, IOMS_CAT1_CASE_A7_4, IOMS_CAT1_CASE_A7_5, IOMS_CAT1_CASE_A7_6, IOMS_CAT1_CASE_A7_7, IOMS_CAT1_CASE_A7_8, IOMS_CAT1_CASE_A7_9, IOMS_CAT1_CASE_A7_10, IOMS_CAT1_CASE_A8_1, IOMS_CAT1_CASE_A8_2, IOMS_CAT1_CASE_A8_3, IOMS_CAT1_CASE_A9_1, IOMS_CAT1_CASE_A9_2, IOMS_CAT1_CASE_A9_3, IOMS_CAT1_CASE_A9_4, IOMS_CAT1_CASE_A9_5, IOMS_CAT1_CASE_A9_6, IOMS_CAT1_CASE_A9_7, IOMS_CAT1_CASE_A9_8, IOMS_CAT2_1, IOMS_CAT2_2, IOMS_CAT2_3, IOMS_CAT2_4, IOMS_CAT2_5, IOMS_CAT2_6, IOMS_CAT2_7, IOMS_CAT2_8, IOMS_CAT2_9, IOMS_CAT2_10, IOMS_CAT2_11, IOMS_CAT2_12, IOMS_CAT3_1, IOMS_CAT3_2, IOMS_CAT3_3, IOMS_CAT4_1, IOMS_CAT4_2, IOMS_CAT5_1, IOMS_CAT5_2, IOMS_CAT5_3, IOMS_CAT6_1, IOMS_CAT6_2, IOMS_CAT6_3, IOMS_CAT6_4, IOMS_CAT6_5, IOMS_CAT6_5, IOMS_CAT6_6, IOMS_CAT7_1, IOMS_CAT7_2, IOMS_CAT7_3, IOMS_CAT7_4, IOMS_CAT7_5, IOMS_CAT7_6, IOMS_CAT7_7, IOMS_CAT7_8, IOMS_CAT8_1, IOMS_CAT8_2, IOMS_CAT8_3, IOMS_CAT8_4, IOMS_CAT8_5, IOMS_CAT8_6, IOMS_CAT8_7, IOMS_CAT8_8, IOMS_CAT8_9, IOMS_CAT9_1, IOMS_CAT9_2, IOMS_CAT10_1, IOMS_CAT10_2, IOMS_CAT12_1, IOMS_CAT12_2, IOMS_CAT12_3, IOMS_CAT13_1, IOMS_CAT13_2, IOMS_CAT13_3, IOMS_CAT13_4, IOMS_CAT13_5, IOMS_CAT13_6, IOMS_CAT14_1, IOMS_CAT14_2, IOMS_CAT14_3, IOMS_CAT14_4, IOMS_CAT14_5, IOMS_CAT14_6, IOMS_CAT14_7, IOMS_CAT14_8, IOMS_CAT14_9, IOMS_CAT14_10, IOMS_CAT14_11, IOMS_EXPERT, IOMS_MYTICKET, IOMS_BROADCAST, IOMS_MAKEADMIN, IOMS_POSTLINK, IOMS_DOWNLOAD_EXCEL, IOMS_COMPLAINT, SWFM_REQTICKET, SWFM_EXPERT, SWFM_MYTICKET,SWFM_BROADCAST, SWFM_MAKEADMIN, SWFM_BANTUAN, DEL_USERBOT, SWFM_DOWNLOAD_EXCEL, SWFM_POSTLINK, SWFM_COMPLAINT, SWFM_BANTUAN_1, SWFM_BANTUAN_2, SWFM_BANTUAN_3, SWFM_BANTUAN_4, SWFM_BANTUAN_5, SWFM_BANTUAN_6, SWFM_BANTUAN_7, SWFM_BANTUAN_SPV_1, SWFM_BANTUAN_SPV_2, SWFM_BANTUAN_SPV_3, SWFM_BANTUAN_SPV_4,SWFM_BANTUAN_SPV_5, SWFM_BANTUAN_SPV_6, SWFM_BANTUAN_SPV_7, SWFM_BANTUAN_SPV_8, SWFM_BANTUAN_SPV_9, SWFM_BANTUAN_SPV_10, SWFM_BANTUAN_SPV_11, SWFM_BANTUAN_SPV_12, SWFM_BANTUAN_SPV_13, SWFM_BANTUAN_SPV_14, SWFM_BANTUAN_SPV_15, SWFM_BANTUAN_SPV_16, SWFM_REQTICKET1, SWFM_REQTICKET2, SWFM_REQTICKET3, SWFM_REQTICKET4, SWFM_REQTICKET5, SWFM_REQTICKET6, SWFM_REQTICKET7, SWFM_REQTICKET8, SWFM_REQTICKET9, SWFM_REQTICKET10, SWFM_REQTICKET11, SWFM_REQTICKET12, SWFM_REQTICKET13, SWFM_CAT1, SWFM_CAT2, SWFM_CAT3, SWFM_CAT4, SWFM_CAT5, SWFM_CAT6, SWFM_CAT7, SWFM_CAT8, SWFM_CAT9, SWFM_CAT10, SWFM_CAT11, SWFM_CAT11_1, SWFM_CAT11_2, SWFM_CAT11_3, SWFM_CAT11_4, SWFM_CAT12, SWFM_CAT13, SWFM_CAT12_1, SWFM_CAT12_2, SWFM_CAT12_3, SWFM_CAT12_4, SWFM_CAT12_5, SWFM_CAT13_1, SWFM_CAT13_2, SWFM_CAT13_3, SWFM_CAT13_4, SWFM_CAT13_5, SWFM_CAT14, SWFM_CAT15, SWFM_CAT16, SWFM_CAT17, SWFM_CAT19, SWFM_CAT14_1, SWFM_CAT14_2, SWFM_CAT14_3, SWFM_CAT14_4, SWFM_CAT1_1, SWFM_CAT1_2, SWFM_CAT1_3, SWFM_CAT1_4, SWFM_CAT1_5, SWFM_CAT2_1, SWFM_CAT2_2, SWFM_CAT2_3, SWFM_CAT2_4, SWFM_CAT2_5, SWFM_CAT3_1, SWFM_CAT3_2, SWFM_CAT3_3, SWFM_CAT3_4, SWFM_CAT3_5, SWFM_CAT3_6, SWFM_CAT3_7, SWFM_CAT3_8, SWFM_CAT3_9,SWFM_CAT3_10, SWFM_CAT4_1, SWFM_CAT4_2, SWFM_CAT4_3, SWFM_CAT5_1, SWFM_CAT5_2, SWFM_CAT5_3, SWFM_CAT5_4, SWFM_CAT6_1, SWFM_CAT6_2, SWFM_CAT6_3, SWFM_CAT6_4, SWFM_CAT6_5, SWFM_CAT6_6, SWFM_CAT6_7, SWFM_CAT6_8, SWFM_CAT6_9, SWFM_CAT7_1, SWFM_CAT7_2, SWFM_CAT8_1, SWFM_CAT8_2, SWFM_CAT8_3, SWFM_CAT8_4, SWFM_CAT8_5, SWFM_CAT8_6, SWFM_CAT8_7, SWFM_CAT8_8, SWFM_CAT8_9, SWFM_CAT8_10, SWFM_CAT8_11, SWFM_CAT8_12, SWFM_CAT8_13, SWFM_CAT8_14, SWFM_CAT9_1, SWFM_CAT9_2, SWFM_CAT9_3, SWFM_CAT9_4, SWFM_CAT9_5, SWFM_CAT9_6, SWFM_CAT9_7, SWFM_CAT9_8, SWFM_CAT9_9,SWFM_CAT9_10, SWFM_CAT9_11, SWFM_CAT9_12, SWFM_CAT9_13, SWFM_CAT9_14, SWFM_CAT9_15, SWFM_CAT9_16, SWFM_CAT9_17, SWFM_CAT9_18, SWFM_CAT9_19, SWFM_CAT9_20, SWFM_CAT9_21, SWFM_CAT9_PMSITE, SWFM_CAT9_PMGENSET, SWFM_CAT9_PMSAMPLING, SWFM_CAT9_PMSITE_1 , SWFM_CAT9_PMSITE_2,SWFM_CAT9_PMSITE_3, SWFM_CAT9_PMSITE_4, SWFM_CAT9_PMSITE_5, SWFM_CAT9_PMSITE_6,SWFM_CAT9_PMGENSET_1, SWFM_CAT9_PMGENSET_2, SWFM_CAT9_PMGENSET_3, SWFM_CAT9_PMGENSET_4, SWFM_CAT9_PMGENSET_5, SWFM_CAT9_PMGENSET_6, SWFM_CAT9_PMGENSET_7, SWFM_CAT9_PMSAMPLING_1, SWFM_CAT9_PMSAMPLING_2, SWFM_CAT9_PMSAMPLING_3, SWFM_CAT9_PMSAMPLING_4, SWFM_CAT9_PMSAMPLING_5, REG_EXPERT_SWFM, DEL_EXPERT_SWFM, REGISTRATION_SWFM_END, SWFM_CAT3_5, SWFM_CAT3_6, SWFM_CAT6_10, SWFM_CAT6_11, SWFM_CAT6_12, SWFM_CAT6_13, SWFM_CAT6_14, SWFM_CAT6_15, SWFM_CAT6_16, SWFM_CAT6_17, SWFM_CAT6_18, SWFM_CAT6_19, SWFM_CAT6_20, SWFM_CAT6_21, SWFM_CAT6_22, SWFM_CAT6_23, SWFM_CAT6_24, SWFM_CAT6_25, SWFM_CAT15_1, SWFM_CAT15_2, SWFM_CAT15_3, SWFM_CAT15_4, SWFM_CAT15_5, SWFM_CAT16_1, SWFM_CAT16_2, SWFM_CAT16_3, SWFM_CAT16_4, SWFM_CAT16_5, SWFM_CAT16_6, SWFM_CAT16_7, SWFM_CAT16_8, SWFM_CAT16_9, SWFM_CAT16_10, SWFM_CAT17_1, SWFM_CAT17_2, SWFM_CAT17_3, SWFM_CAT17_4, SWFM_CAT17_5, SWFM_CAT17_6, SWFM_CAT17_7, SWFM_CAT18_1, SWFM_CAT18_2, SWFM_CAT18_3, SWFM_CAT18_4, SWFM_CAT18_5, SWFM_CAT19_1, SWFM_CAT19_2, SWFM_CAT19_3, SWFM_CAT19_4, SWFM_CAT19_5, SWFM_CAT19_6, SWFM_CAT19_7, SWFM_CAT19_8, SWFM_CAT19_9, SWFM_CAT19_10, SWFM_CAT19_11, SWFM_CAT19_12, SWFM_CAT19_13, SWFM_CAT19_14, SWFM_CAT19_15, SWFM_CAT19_16, PANDUAN_SWFM, PANDUAN_IOMS, PANDUAN_IPAS, SWFM_MYTICKET_PROCESS_END, REG_EXPERT_IOMS, DEL_EXPERT_IOMS, IOMS_MYTICKET_PROCESS_END, IPAS_REQTICKET, IPAS_CAT1, IPAS_CAT2, IPAS_CAT3, IPAS_CAT4, IPAS_CAT5, IPAS_CAT6, IPAS_CAT7, IPAS_CAT1_1, IPAS_CAT1_2, IPAS_CAT1_3, IPAS_CAT1_4, IPAS_CAT1_5, IPAS_CAT1_6, IPAS_CAT2_1, IPAS_CAT2_2, IPAS_CAT2_3, IPAS_CAT3_1, IPAS_CAT3_2, IPAS_CAT3_3, IPAS_CAT4_1, IPAS_CAT4_2, IPAS_CAT4_3, IPAS_CAT4_4, IPAS_CAT5_1, IPAS_CAT5_2, IPAS_CAT5_3, IPAS_CAT5_4, IPAS_CAT6_1, IPAS_CAT6_2, IPAS_CAT6_3, IPAS_CAT6_4, IPAS_CAT6_5, IPAS_CAT7_1, IPAS_CAT7_2, IPAS_CAT7_3, IPAS_CAT7_4, IPAS_TICKET_CAT4_1, IPAS_TICKET_CAT4_2, IPAS_TICKET_CAT4_3, IPAS_TICKET_CAT4_4, IPAS_TICKET_CAT1_1, IPAS_TICKET_CAT1_2, IPAS_TICKET_CAT1_3, IPAS_TICKET_CAT1_4, IPAS_TICKET_CAT1_5, IPAS_TICKET_CAT1_6, IPAS_TICKET_CAT1_7, IPAS_TICKET_CAT1_8, IPAS_TICKET_CAT1_9, IPAS_TICKET_CAT1_10, IPAS_TICKET_CAT1_11, IPAS_TICKET_CAT1_12, IPAS_TICKET_CAT1_13, IPAS_TICKET_CAT1_14, IPAS_TICKET_CAT1_15, IPAS_TICKET_CAT1_16, IPAS_TICKET_CAT1_17, IPAS_TICKET_CAT1_18, IPAS_TICKET_CAT1_19, IPAS_TICKET_CAT1_20, IPAS_TICKET_CAT1_21, IPAS_TICKET_CAT1_22, IPAS_TICKET_CAT1_23, IPAS_TICKET_CAT1_24, IPAS_TICKET_CAT1_25, IPAS_TICKET_CAT1_26, IPAS_TICKET_CAT2_1, IPAS_TICKET_CAT2_2, IPAS_TICKET_CAT2_3, IPAS_TICKET_CAT2_4, IPAS_TICKET_CAT2_5, IPAS_TICKET_CAT2_6, IPAS_TICKET_CAT2_7, IPAS_TICKET_CAT2_8, IPAS_TICKET_CAT2_9, IPAS_TICKET_CAT2_10, IPAS_TICKET_CAT3_1, IPAS_TICKET_CAT3_2, IPAS_TICKET_CAT3_3, IPAS_TICKET_CAT3_4, IPAS_TICKET_CAT3_5, IPAS_TICKET_CAT3_6, IPAS_TICKET_CAT3_7, IPAS_TICKET_CAT3_8, IPAS_TICKET_CAT3_9, IPAS_TICKET_CAT3_10, IPAS_TICKET_CAT3_11, IPAS_TICKET_CAT5_1, IPAS_TICKET_CAT5_2, IPAS_TICKET_CAT5_3, IPAS_TICKET_CAT5_4, IPAS_TICKET_CAT5_5, IPAS_TICKET_CAT5_6, IPAS_TICKET_CAT5_7, IPAS_TICKET_CAT5_8, IPAS_TICKET_CAT5_9, IPAS_TICKET_CAT5_10, IPAS_TICKET_CAT5_11, IPAS_TICKET_CAT5_12, IPAS_TICKET_CAT5_13, IPAS_TICKET_CAT5_14, IPAS_TICKET_CAT5_15, IPAS_TICKET_CAT5_16, IPAS_TICKET_CAT5_17, IPAS_TICKET_CAT5_18, IPAS_TICKET_CAT5_19, IPAS_TICKET_CAT5_20, IPAS_EXPERT, IPAS_MYTICKET, IPAS_BROADCAST, IPAS_MAKEADMIN, IPAS_POSTLINK, IPAS_DOWNLOAD_EXCEL, IPAS_COMPLAINT, IPAS_MYTICKET_PROCESS_END, REG_EXPERT_IPAS, DEL_EXPERT_IPAS, SWFM_MYTICKET_ACTION_MENU1, SWFM_MYTICKET_ACTION_MENU2, SWFM_MYTICKET_ACTION_MENU3, SWFM_MYTICKET_ACTION_MENU4, SWFM_MYTICKET_ACTION_CAT1, SWFM_MYTICKET_ACTION_CAT2, SWFM_MYTICKET_ACTION_CAT3, SWFM_MYTICKET_ACTION_CAT4, SWFM_MYTICKET_ACTION_CAT5, SWFM_MYTICKET_ACTION_CAT6, SWFM_MYTICKET_ACTION_CAT7, SWFM_MYTICKET_ACTION_CAT8, SWFM_MYTICKET_ACTION_CAT9, SWFM_MYTICKET_ACTION_CAT10, SWFM_MYTICKET_ACTION_CAT11, SWFM_MYTICKET_ACTION_CAT12, SWFM_MYTICKET_ACTION_CAT13, SWFM_MYTICKET_ACTION_CAT14, SWFM_MYTICKET_ACTION_CAT15, SWFM_MYTICKET_ACTION_CAT16, SWFM_MYTICKET_ACTION_CAT17, SWFM_MYTICKET_ACTION_CAT18, SWFM_MYTICKET_ACTION_CAT19, SWFM_MYTICKET_ACTION_CAT20, SWFM_MYTICKET_ACTION_CAT21, SWFM_MYTICKET_ACTION_CAT22,SWFM_MYTICKET_ACTION_CAT23, SWFM_MYTICKET_ACTION_CAT24,SWFM_MYTICKET_ACTION_CAT25, SWFM_MYTICKET_ACTION_CAT26, SWFM_MYTICKET_ACTION_CAT27, SWFM_MYTICKET_ACTION_CAT28, SWFM_MYTICKET_ACTION_CAT29, SWFM_MYTICKET_ACTION_CAT30, SWFM_MYTICKET_ACTION_CAT31, SCARLETT_REQTICKET, SCARLETT_CAT1, SCARLETT_CAT1_1, SCARLETT_CAT1_2, SCARLETT_CAT1_3, SCARLETT_CAT2, SCARLETT_CAT3, SCARLETT_CAT4, SCARLETT_CAT5, SCARLETT_CAT6, SCARLETT_CAT7, SCARLETT_CAT8, SCARLETT_CAT10, SCARLETT_MYTICKET, SCARLETT_POSTLINK, SCARLETT_DOWNLOAD_EXCEL, SCARLETT_COMPLAINT, SCARLETT_MYTICKET_PROCESS_END = range(603)

def start(update: Update, _: CallbackContext) -> None: 
    full_name = update.message.from_user.full_name
    username = update.message.from_user.username
    chatid_telegram  = update.message.from_user.id 
    grup_name = update.message.chat.title
    syanticbot = 'https://t.me/syanticbot'
    ##acces
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    check_status = client.command(query)
    
    if grup_name:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        button1 = InlineKeyboardButton("SYANTIC BOT", url=syanticbot)
        buttons = [[button1]]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text('*SYANTIC BOT* hanya bisa di akses melalui private chatBOT. Terima kasih \nKlik tombol dibawah ini',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        log_bot_fail_swfm(update, '*Start* ➞ Akses melaui Grup')
        return ConversationHandler.END
    elif not grup_name:
        check_status = check_status == 0
        if not username:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f"Hallo Kak *{full_name}*, Mohon membuat *Username ID Telegram *terlebih dahulu", parse_mode=telegram.ParseMode.MARKDOWN)
            update.message.reply_text('https://drive.google.com/file/d/1T5TRaQZs-fFU7IicI5TyudczL3ZKJxAx/view?usp=drivesdk',parse_mode=telegram.ParseMode.HTML)
            update.message.reply_text('Berikut adalah Link panduan Video Tutorial membuat Usernama ID Telegram, terima kasih',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_fail_swfm(update, '*Start* ➞ Belum membuat username ID telegram')
            return ConversationHandler.END
        elif check_status is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f"Hallo Kak *{full_name}*,\nSelamat datang di *BOT*\nSYANTIC : System Analyzer Network and Tool Incident Center\n\nSebuat BOT untuk para pejuang dan Tentara Langit di seluruh Indonesia, kami tidak se-manis harapan tapi setiap hari berusaha manis aja agar hidup bahagia. By OCHABOT Team.", parse_mode=telegram.ParseMode.MARKDOWN)
            keyboard = [
                [InlineKeyboardButton("IOMS", callback_data=str(REGISTRATION_TOOLS_IOMS))],
                [InlineKeyboardButton("IPAS", callback_data=str(REGISTRATION_TOOLS_IPAS))],
                [InlineKeyboardButton("SCARLETT", callback_data=str(REGISTRATION_TOOLS_IOMS))],
                [InlineKeyboardButton("SWFM", callback_data=str(REGISTRATION_TOOLS_SWFM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Klik Tools dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
            return MENU_REGISTRATION
            
        elif check_status is False:

                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f"Hallo Kak *{full_name}*,\nSelamat datang di *BOT*\nSYANTIC : System Analyzer Network and Tool Incident Center\n\nSebuat BOT untuk para pejuang dan Tentara Langit di seluruh Indonesia, kami tidak se-manis harapan tapi setiap hari berusaha manis aja agar hidup bahagia. By OCHABOT Team.", parse_mode=telegram.ParseMode.MARKDOWN)
                
                keyboard = [
                [InlineKeyboardButton("IOMS", callback_data=str(REGISTRATION_TOOLS_IOMS))],
                [InlineKeyboardButton("IPAS", callback_data=str(REGISTRATION_TOOLS_IPAS))],
                [InlineKeyboardButton("SCARLETT", callback_data=str(REGISTRATION_TOOLS_IOMS))],
                [InlineKeyboardButton("SWFM", callback_data=str(REGISTRATION_TOOLS_SWFM))],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Klik Tools dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
                return MENU_REGISTRATION
        
################################################REGISTRASI IOMS#######################################
def registration_tools_ioms(update: Update, _: CallbackContext) -> None:
    try:
        chatid_telegram  = update.callback_query.from_user.id
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"select registered_swfm, registered_ioms, registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        check_data = client.command(query)
        check_ioms = check_data[1]
        query = update.callback_query
        query.answer()
        if check_ioms == 'False':
            keyboard = [
                [InlineKeyboardButton("Registrasi", callback_data=str(REGISTRATION_IOMS))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
            return MENU_REGISTRATION
        else:
            query.edit_message_text("✅ *Akun sudah terdaftar* untuk di Menu SYANTICBOT. klik /menu", parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_ioms_scarlett(update, '*Start* ➞ Akun Sudah Terdaftar di Menu IOMS SYANTICBOT')
            return ConversationHandler.END
    except:
        keyboard = [
            [InlineKeyboardButton("Registrasi", callback_data=str(REGISTRATION_IOMS))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        return MENU_REGISTRATION
        

def registration_check_ioms(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_ioms from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    query = update.callback_query
    query.answer()
    if data_select == "False":
        query.edit_message_text('Anda memilih : *Registrasi*',parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Cukup ketik Email LDAP atau pribadi",parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        query.edit_message_text('Anda memilih : *Registrasi*',parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("*Langkah Pertama*\n\nEmail LDAP atau pribadi",parse_mode=telegram.ParseMode.MARKDOWN)
    return REGISTRATION_EMAILS_IOMS

def registration_emails_ioms(update: Update, _: CallbackContext) -> None:
    ull_name = update.message.from_user.full_name
    chatid_telegram = update.message.from_user.id 
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Harap menunggu dalam beberapa detik....',parse_mode=telegram.ParseMode.MARKDOWN)
    email_params = update.message.text
    email_paramater = update.message.text.split('@')[1]
    if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/ioms_email.txt"):
        os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/ioms_email.txt")
        time.sleep(1)
    else:
        print("The file does not exist")
        time.sleep(1)
    if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/ioms_nohp.txt"):
        os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/ioms_nohp.txt")
        time.sleep(1)
    else:
        print("The file does not exist")
        time.sleep(1)
    if email_paramater == 'telkomsel.co.id':
        try:
            vendor_email = email_params.split('_x@telkomsel')[1]
            if vendor_email == '.co.id':
                data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_email.txt','a')
                data_add.write("{}".format(email_params))
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text('Silahkan masukkan password LDAP',parse_mode=telegram.ParseMode.MARKDOWN)
                return REGISTRATION_PWD_IOMS
        except:
            data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_email.txt','a')
            data_add.write("{}".format(email_params))
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Silahkan masukkan password LDAP',parse_mode=telegram.ParseMode.MARKDOWN)
            return REGISTRATION_PWD_IOMS
    else:
        gspread_client = gspread.service_account(filename="/home/dimas/baru/helpdeskbot_v2/data/credential_ioms_ipas.json")
        spreadsheets = gspread_client.openall()
        if spreadsheets:
            first_spreadsheet = spreadsheets[0]
            worksheet = first_spreadsheet.get_worksheet(0)
            data = worksheet.get_all_values()
            try:
                notfound = []
                found = []
                for row in data:
                    data_list = str(row).replace("[","").replace("]","").replace("'","").replace('±','').replace('+','').replace("\\\\n",' ').split('\\n')
                    for data in data_list:
                        data = str(data).split(', ')
                        fullname = str(data[2]).replace('"','').replace('.','').title()
                        email = str(data[3])
                        nohp = str(data[4])
                        check = email == email_params
                        data_all = []
                        if check is True:
                            found.append('Email ada')
                            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                            query = f"select registered_ioms from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                            data_select = client.command(query)
                            if data_select == "False":
                                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                                query = f"select email from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                                data = client.command(query)
                                if str(data) == str(email_params):
                                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                                    query = f"select count(*) as `count` from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                                    check_status = client.command(query)
                                    check_status = check_status == 0
                                    if check_status is True:
                                        data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_email.txt','a')
                                        data_add.write("{}".format(email_params))
                                        data_add.close()
                                        data_add_ = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_nohp.txt','a')
                                        data_add_.write("{}".format(nohp))
                                        data_add_.close()
                                        keyboard = [
                                            [InlineKeyboardButton("Iya", callback_data=str(REGISTRATION_IOMS_MITRA))],
                                            [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                                        ]
                                        reply_markup = InlineKeyboardMarkup(keyboard)
                                        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                        update.message.reply_text("Nama : {}\nEmail : {}\nNo HP : {}\nRegistrasi Status : ✅".format(fullname,email,nohp))
                                        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                        update.message.reply_text(f"Silahkan konfirmasi, Pilih Iya jika Benar", reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
                                        return MENU_REGISTRATION
                                    else:
                                        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                                        query = f"ALTER TABLE production.helpdesk_bot_swfm update registered_ioms = 'True' where chatid_telegram = '{chatid_telegram}'"
                                        client.command(query)
                                        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                        update.message.reply_text(f"Terima kasih, anda berhasil terdaftar MENU",parse_mode=telegram.ParseMode.MARKDOWN)
                                        log_bot_success_ipas(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IOMS di SYANTIC BOT 🆕')
                                        return ConversationHandler.END
                                else:
                                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                    update.message.reply_text(f"Email anda tidak cocok dengan BOT Registrasi, gunakan email : *{data}*\nSilahkan masukkan email diatas",parse_mode=telegram.ParseMode.MARKDOWN)
                                    log_bot_success_ioms_scarlett(update, '*Registrasi* ➞ Email anda tidak cocok di Bot Registrasi')
                                    return ConversationHandler.END
                            else:
                                data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_email.txt','a')
                                data_add.write("{}".format(email_params))
                                data_add.close()
                                data_add_ = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_nohp.txt','a')
                                data_add_.write("{}".format(nohp))
                                data_add_.close()
                                keyboard = [
                                    [InlineKeyboardButton("Iya", callback_data=str(REGISTRATION_IOMS_MITRA))],
                                    [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                                ]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                update.message.reply_text("Nama : {}\nEmail : {}\nNo HP : {}\nRegistrasi Status : ✅".format(fullname,email,nohp))
                                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                update.message.reply_text(f"Silahkan konfirmasi, Pilih Iya jika Benar", reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
                                return MENU_REGISTRATION
                        else:
                            notfound.append('Email tidak ada')
                list(set(notfound))
                found[0] == 'Email ada'
            except:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Maaf, Email anda tidak cocok dengan Form, Silahkan berkordinasi dengan atasan masing-masing (SPV TO)",parse_mode=telegram.ParseMode.MARKDOWN)
                log_bot_fail_ioms_scarlett(update, '*Registrasi* ➞ Email tidak cocok')
                return ConversationHandler.END

    
def registration_pwd_ioms(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id 
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Harap menunggu dalam beberapa detik....',parse_mode=telegram.ParseMode.MARKDOWN)

    def check_word(string):
        if len(string) < 8:
            return False
        word_b = re.search(r'[A-Z]', string) is not None
        word_k = re.search(r'[a-z]', string) is not None
        ada_karakter_spesial = re.search(r'[!@#$%^&*(),.?":{}|<>]', string) is not None
        return word_b and word_k and ada_karakter_spesial


    pwd_paramater = update.message.text
    hasil = check_word(pwd_paramater)
    if hasil is True:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("✅ Akun LDAP sesuai, langkah terakhir masukkan No HP\nContoh *628xxxxxxxxxx*",parse_mode=telegram.ParseMode.MARKDOWN)
        return LDAP_NO_IOMS
    else:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("Maaf, Passward LDAP anda tidak cocok, silahkan coba lagi /start",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_fail_ioms_scarlett(update, '*Registrasi* ➞ Passward LDAP tidak cocok')
        return ConversationHandler.END
    

def ldap_no_ioms(update: Update, _: CallbackContext) -> None:
    chat_id = update.message.from_user.id 
    full_name = update.message.from_user.full_name
    username = update.message.from_user.username
    nohp_parameter = update.message.text

    if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/ioms_nohp.txt"):
        os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/ioms_nohp.txt")
        time.sleep(1)
    else:
        print("The file does not exist")
        time.sleep(1)

    email = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_email.txt','r')
    email = email.read()
    try:
        vendor_email = email.split('_x@telkomsel')[1]
        if vendor_email == '.co.id':
            data_add_ = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_nohp.txt','a')
            data_add_.write("{}".format(nohp_parameter))
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Silahkan ketik nama mitra atau perusahaan')
            return REGISTRATION_IOMS_END
    except:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"select no_hp from production.helpdesk_bot_swfm where chatid_telegram = '{chat_id}'"
        data = client.command(query)
        data_nohp = data
        data_all = [f'{data}']

        if nohp_parameter in data_all:
            query = f"select email from production.helpdesk_bot_swfm where chatid_telegram = '{chat_id}'"
            data = client.command(query)
            if str(data) != str(email):
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f"Email anda tidak cocok dengan BOT Registrasi, gunakan email : *{data}*\nSilahkan masukkan email diatas",parse_mode=telegram.ParseMode.MARKDOWN)
                log_bot_success_ioms_scarlett(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IOMS di SYANTIC BOT 🆕')
            else:
                query = f"ALTER TABLE production.helpdesk_bot_swfm update registered_ioms = 'True' where chatid_telegram = '{chat_id}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f"Terima kasih, anda berhasil terdaftar MENU",parse_mode=telegram.ParseMode.MARKDOWN)
                log_bot_success_ioms_scarlett(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IOMS di SYANTIC BOT 🆕')
            return ConversationHandler.END
        else:
            query = f"select count(*) as `count` from production.helpdesk_bot_swfm where chatid_telegram = '{chat_id}' or no_hp = '{nohp_parameter}' or email = '{email}'"
            check_status = client.command(query)
            check_status = check_status == 1
            if check_status is True:
                print('no hp dan email salah')
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f"No HP anda tidak cocok di Bot Registrasi, gunakan No HP : {data_nohp}\nSilahkan masukkan No HP diatas",parse_mode=telegram.ParseMode.MARKDOWN)
                log_bot_success_ioms_scarlett(update, '*Registrasi* ➞ No HP anda tidak cocok di Bot Registrasi')
            else:
                query = f"INSERT INTO production.helpdesk_bot_swfm select '{full_name}','{username}','{chat_id}','{nohp_parameter}','{email}','Done','False','True','False','user','None','None','Telkomsel','None','None','None','None','None','None','None','None','None','None','None','None','None'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text('Terima kasih, anda berhasil terdaftar MENU')
                log_bot_success_ioms_scarlett(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IOMS di SYANTIC BOT 🆕')
            return ConversationHandler.END

    
def registration_ioms_mitra(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text('Silahkan ketik nama mitra atau perusahaan')
    return REGISTRATION_IOMS_END

def registration_ioms_end(update: Update, _: CallbackContext) -> None:
    full_name = update.message.from_user.full_name
    username = update.message.from_user.username
    chat_id = update.message.from_user.id
    mitra = update.message.text.replace('PT.','').replace('pt.','').replace('Pt.','').replace('PT. ','').replace('pt. ','').replace('Pt. ','').title()
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    no_hp = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_nohp.txt','r')
    no_hp = no_hp.read()
    email = open('/home/dimas/baru/helpdeskbot_v2/data_log/ioms_email.txt','r')
    email = email.read()

    query = f"INSERT INTO production.helpdesk_bot_swfm select '{full_name}','{username}','{chat_id}','{no_hp}','{email}','Done','False','True','False','user','None','None','{mitra}','None','None','None','None','None','None','None','None','None','None','None','None','None'"
    client.command(query)
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Terima kasih, anda berhasil terdaftar MENU')
    log_bot_success_ioms_scarlett(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IOMS di SYANTIC BOT 🆕')
    return ConversationHandler.END
################################################REGISTRASI END IOMS#######################################

################################################REGISTRASI IPAS#######################################
def registration_tools_ipas(update: Update, _: CallbackContext) -> None:
    try:
        chatid_telegram  = update.callback_query.from_user.id
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"select registered_swfm, registered_ioms, registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        check_data = client.command(query)
        check_ipas = check_data[2]
        query = update.callback_query
        query.answer()
        if check_ipas == 'False':
            keyboard = [
                [InlineKeyboardButton("Registrasi", callback_data=str(REGISTRATION_IPAS))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
            return MENU_REGISTRATION
        else:
            query.edit_message_text("✅ *Akun sudah terdaftar* untuk di Menu SYANTICBOT. klik /menu", parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_ipas(update, '*Start* ➞ Akun Sudah Terdaftar di Menu IPAS SYANTICBOT')
            return ConversationHandler.END
    except:
        keyboard = [
            [InlineKeyboardButton("Registrasi", callback_data=str(REGISTRATION_IPAS))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        return MENU_REGISTRATION

def registration_check_ipas(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    query = update.callback_query
    query.answer()
    if data_select == "False":
        query.edit_message_text('Anda memilih : *Registrasi*',parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Cukup ketik Email LDAP atau pribadi",parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        query.edit_message_text('Anda memilih : *Registrasi*',parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("*Langkah Pertama*\n\nEmail LDAP atau pribadi",parse_mode=telegram.ParseMode.MARKDOWN)
    return REGISTRATION_EMAILS_IPAS

def registration_emails_ipas(update: Update, _: CallbackContext) -> None:
    full_name = update.message.from_user.full_name
    chatid_telegram = update.message.from_user.id 
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Harap menunggu dalam beberapa detik....',parse_mode=telegram.ParseMode.MARKDOWN)
    email_params = update.message.text
    email_paramater = update.message.text.split('@')[1]
    if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/ipas_email.txt"):
        os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/ipas_email.txt")
        time.sleep(1)
    else:
        print("The file does not exist")
        time.sleep(1)
    if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/ipas_nohp.txt"):
        os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/ipas_nohp.txt")
        time.sleep(1)
    else:
        print("The file does not exist")
        time.sleep(1)
    if email_paramater == 'telkomsel.co.id':
        try:
            vendor_email = email_params.split('_x@telkomsel')[1]
            if vendor_email == '.co.id':
                data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_email.txt','a')
                data_add.write("{}".format(email_params))
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text('Silahkan masukkan password LDAP',parse_mode=telegram.ParseMode.MARKDOWN)
                return REGISTRATION_PWD_IPAS
        except:
            data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_email.txt','a')
            data_add.write("{}".format(email_params))
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Silahkan masukkan password LDAP',parse_mode=telegram.ParseMode.MARKDOWN)
            return REGISTRATION_PWD_IPAS
    else:
        gspread_client = gspread.service_account(filename="/home/dimas/baru/helpdeskbot_v2/data/credential_ioms_ipas.json")
        spreadsheets = gspread_client.openall()
        if spreadsheets:
            first_spreadsheet = spreadsheets[0]
            worksheet = first_spreadsheet.get_worksheet(0)
            data = worksheet.get_all_values()
            try:
                notfound = []
                found = []
                for row in data:
                    data_list = str(row).replace("[","").replace("]","").replace("'","").replace('±','').replace('+','').replace("\\\\n",' ').split('\\n')
                    for data in data_list:
                        data = str(data).split(', ')
                        fullname = str(data[2]).replace('"','').replace('.','').title()
                        email = str(data[3])
                        nohp = str(data[4])
                        check = email == email_params
                        data_all = []
                        if check is True:
                            found.append('Email ada')
                            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                            query = f"select registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                            data_select = client.command(query)
                            if data_select == "False":
                                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                                query = f"select email from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                                data = client.command(query)
                                if str(data) == str(email_params):
                                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                                    query = f"select count(*) as `count` from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                                    check_status = client.command(query)
                                    check_status = check_status == 0
                                    if check_status is True:
                                        data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_email.txt','a')
                                        data_add.write("{}".format(email_params))
                                        data_add.close()
                                        data_add_ = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_nohp.txt','a')
                                        data_add_.write("{}".format(nohp))
                                        data_add_.close()
                                        keyboard = [
                                            [InlineKeyboardButton("Iya", callback_data=str(REGISTRATION_IPAS_MITRA))],
                                            [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                                        ]
                                        reply_markup = InlineKeyboardMarkup(keyboard)
                                        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                        update.message.reply_text("Nama : {}\nEmail : {}\nNo HP : {}\nRegistrasi Status : ✅".format(fullname,email,nohp))
                                        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                        update.message.reply_text(f"Silahkan konfirmasi, Pilih Iya jika Benar", reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
                                        return MENU_REGISTRATION
                                    else:
                                        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                                        query = f"ALTER TABLE production.helpdesk_bot_swfm update registered_ipas = 'True' where chatid_telegram = '{chatid_telegram}'"
                                        client.command(query)
                                        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                        update.message.reply_text(f"Terima kasih, anda berhasil terdaftar MENU",parse_mode=telegram.ParseMode.MARKDOWN)
                                        log_bot_success_ipas(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IPAS di SYANTIC BOT 🆕')
                                        return ConversationHandler.END
                                else:
                                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                    update.message.reply_text(f"Email anda tidak cocok dengan BOT Registrasi, gunakan email : *{data}*\nSilahkan masukkan email diatas",parse_mode=telegram.ParseMode.MARKDOWN)
                                    log_bot_success_ipas(update, '*Registrasi* ➞ Email anda tidak cocok di Bot Registrasi')
                                    return ConversationHandler.END
                            else:
                                data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_email.txt','a')
                                data_add.write("{}".format(email_params))
                                data_add.close()
                                data_add_ = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_nohp.txt','a')
                                data_add_.write("{}".format(nohp))
                                data_add_.close()
                                keyboard = [
                                    [InlineKeyboardButton("Iya", callback_data=str(REGISTRATION_IPAS_MITRA))],
                                    [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                                ]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                update.message.reply_text("Nama : {}\nEmail : {}\nNo HP : {}\nRegistrasi Status : ✅".format(fullname,email,nohp))
                                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                update.message.reply_text(f"Silahkan konfirmasi, Pilih Iya jika Benar", reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
                                return MENU_REGISTRATION
                        else:
                            notfound.append('Email tidak ada')
                list(set(notfound))
                found[0] == 'Email ada'
            except:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Maaf, Email anda tidak cocok dengan Form, Silahkan berkordinasi dengan atasan masing-masing (SPV TO)",parse_mode=telegram.ParseMode.MARKDOWN)
                log_bot_fail_ipas(update, '*Registrasi* ➞ Email tidak cocok')
                return ConversationHandler.END

def registration_pwd_ipas(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id 
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Harap menunggu dalam beberapa detik....',parse_mode=telegram.ParseMode.MARKDOWN)

    def check_word(string):
        if len(string) < 8:
            return False
        word_b = re.search(r'[A-Z]', string) is not None
        word_k = re.search(r'[a-z]', string) is not None
        ada_karakter_spesial = re.search(r'[!@#$%^&*(),.?":{}|<>]', string) is not None
        return word_b and word_k and ada_karakter_spesial


    pwd_paramater = update.message.text
    hasil = check_word(pwd_paramater)
    if hasil is True:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("✅ Akun LDAP sesuai, langkah terakhir masukkan No HP\nContoh *628xxxxxxxxxx*",parse_mode=telegram.ParseMode.MARKDOWN)
        return LDAP_NO_IPAS
    else:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("Maaf, Passward LDAP anda tidak cocok, silahkan coba lagi /start",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_fail_ipas(update, '*Registrasi* ➞ Passward LDAP tidak cocok')
        return ConversationHandler.END

def ldap_no_ipas(update: Update, _: CallbackContext) -> None:
    chat_id = update.message.from_user.id 
    full_name = update.message.from_user.full_name
    username = update.message.from_user.username
    nohp_parameter = update.message.text
    
    if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/ipas_nohp.txt"):
        os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/ipas_nohp.txt")
        time.sleep(1)
    else:
        print("The file does not exist")
        time.sleep(1)

    email = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_email.txt','r')
    email = email.read()
    try:
        vendor_email = email.split('_x@telkomsel')[1]
        if vendor_email == '.co.id':
            data_add_ = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_nohp.txt','a')
            data_add_.write("{}".format(nohp_parameter))
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Silahkan ketik nama mitra atau perusahaan')
            return REGISTRATION_IPAS_END
    except:

        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"select no_hp from production.helpdesk_bot_swfm where chatid_telegram = '{chat_id}'"
        data = client.command(query)
        data_nohp = data
        data_all = [f'{data}']

        if nohp_parameter in data_all:
            query = f"select email from production.helpdesk_bot_swfm where chatid_telegram = '{chat_id}'"
            data = client.command(query)
            if str(data) != str(email):
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f"Email anda tidak cocok dengan BOT Registrasi, gunakan email : *{data}*\nSilahkan masukkan email diatas",parse_mode=telegram.ParseMode.MARKDOWN)
                log_bot_success_ipas(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IPAS di SYANTIC BOT 🆕')
            else:
                query = f"ALTER TABLE production.helpdesk_bot_swfm update registered_ipas = 'True' where chatid_telegram = '{chat_id}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f"Terima kasih, anda berhasil terdaftar MENU",parse_mode=telegram.ParseMode.MARKDOWN)
                log_bot_success_ipas(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IPAS di SYANTIC BOT 🆕')
            return ConversationHandler.END
        else:
            query = f"select count(*) as `count` from production.helpdesk_bot_swfm where chatid_telegram = '{chat_id}' or no_hp = '{nohp_parameter}' or email = '{email}'"
            check_status = client.command(query)
            check_status = check_status == 1
            if check_status is True:
                print('no hp dan email salah')
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f"No HP anda tidak cocok di Bot Registrasi, gunakan No HP : {data_nohp}\nSilahkan masukkan No HP diatas",parse_mode=telegram.ParseMode.MARKDOWN)
                log_bot_success_ipas(update, '*Registrasi* ➞ No HP anda tidak cocok di Bot Registrasi')
            else:
                query = f"INSERT INTO production.helpdesk_bot_swfm select '{full_name}','{username}','{chat_id}','{nohp_parameter}','{email}','Done','False','False','True','user','None','None','Telkomsel','None','None','None','None','None','None','None','None','None','None','None','None','None'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text('Terima kasih, anda berhasil terdaftar MENU')
                log_bot_success_ipas(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IPAS di SYANTIC BOT 🆕')
            return ConversationHandler.END
    

def registration_ipas_mitra(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text('Silahkan ketik nama mitra atau perusahaan')
    return REGISTRATION_IPAS_END

def registration_ipas_end(update: Update, _: CallbackContext) -> None:
    full_name = update.message.from_user.full_name
    username = update.message.from_user.username
    chat_id = update.message.from_user.id
    mitra = update.message.text.replace('PT.','').replace('pt.','').replace('Pt.','').replace('PT. ','').replace('pt. ','').replace('Pt. ','').title()
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    no_hp = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_nohp.txt','r')
    no_hp = no_hp.read()
    email = open('/home/dimas/baru/helpdeskbot_v2/data_log/ipas_email.txt','r')
    email = email.read()

    query = f"INSERT INTO production.helpdesk_bot_swfm select '{full_name}','{username}','{chat_id}','{no_hp}','{email}','Done','False','False','True','user','None','None','{mitra}','None','None','None','None','None','None','None','None','None','None','None','None','None'"
    client.command(query)
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Terima kasih, anda berhasil terdaftar MENU')
    log_bot_success_ipas(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU IPAS di SYANTIC BOT 🆕')
    return ConversationHandler.END
################################################REGISTRASI END IPAS#######################################

################################################REGISTRASI SWFM#######################################
def registration_tools_swfm(update: Update, _: CallbackContext) -> None:
    try:
        chatid_telegram  = update.callback_query.from_user.id
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"select registered_swfm, registered_ioms, registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        check_data = client.command(query)
        check_swfm = check_data[0]
        query = update.callback_query
        query.answer()
        if check_swfm == 'False':
            keyboard = [
                [InlineKeyboardButton("Registrasi", callback_data=str(REGISTRATION_SWFM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
            return MENU_REGISTRATION
        else:
            query.edit_message_text("✅ *Akun sudah terdaftar* untuk di Menu SYANTICBOT. klik /menu", parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_swfm(update, '*Start* ➞ Akun Sudah Terdaftar di Menu SWFM SYANTICBOT')
            return ConversationHandler.END
    except:
        keyboard = [
            [InlineKeyboardButton("Registrasi", callback_data=str(REGISTRATION_SWFM))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        return MENU_REGISTRATION
def registration_check_swfm(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_swfm from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    query = update.callback_query
    query.answer()
    if data_select == "False":
        query.edit_message_text('Anda memilih : *Registrasi*',parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("*Cukup ketik No Hp* yang telah Registrasi BOT sebelumnya\nContoh *628xxxxxxxxxx*",parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        query.edit_message_text('Anda memilih : *Registrasi*',parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("*Langkah Pertama*\n\nKetik No HP yang sudah terdaftar di Form Registrasi SWFM di Grup Wa per Region\nContoh *628xxxxxxxxxx*",parse_mode=telegram.ParseMode.MARKDOWN)
    return REGISTRATION_NOHP_SWFM
def registration_nohp_swfm(update: Update, _: CallbackContext) -> None:
    full_name = update.message.from_user.full_name
    chatid_telegram = update.message.from_user.id 
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Harap menunggu dalam beberapa detik....',parse_mode=telegram.ParseMode.MARKDOWN)
    nohp_paramater = update.message.text.replace('+','').replace('-','').replace(' ','')
    new_nohp_paramater = []
    if nohp_paramater[0] == '0':
        new_nohp_paramater.append('62'+nohp_paramater[1:])
    else:
        new_nohp_paramater.append(nohp_paramater)
    new_nohp_paramater = new_nohp_paramater[0]

    gspread_client = gspread.service_account(filename="/home/dimas/baru/helpdeskbot_v2/data/credential_swfm_form_user.json")
    spreadsheets = gspread_client.openall()
    if spreadsheets:
        first_spreadsheet = spreadsheets[0]
        worksheet = first_spreadsheet.get_worksheet(0)
        data = worksheet.get_all_values()
        try:
            notfound = []
            found = []
            for row in data:
                data_list = str(row).replace("[","").replace("]","").replace("'","").replace('±','').replace('+','').replace("\\\\n",' ').split('\\n')
                for data in data_list:
                    data = str(data).split(', ')
                    fullname = str(data[1]).replace('"','').replace('.','').title()
                    email = str(data[2])
                    nohp = str(data[3])
                    area = str(data[4])
                    remark = str(data[-1]).replace(' Done','Done')
                    check = nohp == new_nohp_paramater
                    data_all = []
                    if check is True:
                        found.append('No HP ada')
                        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                        query = f"select no_hp from production.helpdesk_bot_swfm"
                        data = client.command(query)
                        data_all.append(data)
                        check_data = str(data_all).replace('[','').replace(']','').replace("'","").replace("\\n",",").split(',')
                        if nohp in check_data:
                            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                            query = f"select registered_swfm from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                            data_select = client.command(query)
                            if data_select == "False":
                                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                                query = f"select no_hp from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                                data = client.command(query)
                                if str(data) == str(nohp):
                                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                                    query = f"ALTER TABLE production.helpdesk_bot_swfm update registered_swfm = 'True' where chatid_telegram = '{chatid_telegram}'"
                                    client.command(query)
                                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                    update.message.reply_text(f"Terima kasih, anda berhasil terdaftar MENU",parse_mode=telegram.ParseMode.MARKDOWN)
                                    log_bot_success_swfm(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU SWFM di SYANTIC BOT 🆕')
                                    return ConversationHandler.END
                                else:
                                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                    update.message.reply_text("No HP anda tidak cocok di Bot Registrasi, Silahkan masukkan No HP yang sesuai",parse_mode=telegram.ParseMode.MARKDOWN)
                                    log_bot_fail_swfm(update, '*Registrasi* ➞ No HP anda tidak cocok di Bot Registrasi')
                                    return ConversationHandler.END
                            else:
                                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                update.message.reply_text(f"Maaf, No HP sudah terdaftar di BOT, silahkan ketik No HP lainnya\nKlik /start",parse_mode=telegram.ParseMode.MARKDOWN)

                                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                                query = f"select * from production.helpdesk_bot_swfm he where no_hp ='{nohp}'"
                                data = client.command(query)
                                data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
                                for data in data_list:
                                    data = str(data).split(', ')
                                    namas = data[0]
                                    nohps = data[3]
                                    emails = data[4]
                                data_check = f'\nPenjelasan:\n\nRequestor : {full_name}\n\nForm Registrasi :\nNama Lengkap : {fullname}\nNo HP : {nohp}\nEmail : {email}\n\nBot Registrasi : \nNama Lengkap : {namas}\nNo HP : {nohps}\nEmail : {emails}\n\nSilahkan crose cek kembali'

                                log_bot_regis_swfm(update, 'Registrasi ➞ No HP sudah terdaftar di BOT '+data_check)
                            return ConversationHandler.END
                        else:
                            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                            query = f"select count(*) as `count` from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                            check_status = client.command(query)
                            check_status = check_status == 1
                            if check_status is False:
                                if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/swfm_nohp.txt"):
                                    os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/swfm_nohp.txt")
                                    time.sleep(1)
                                else:
                                    print("The file does not exist")
                                    time.sleep(1)
                                data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/swfm_nohp.txt','a')
                                data_add.write("{}".format(new_nohp_paramater))
                                data_add.close()
                                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                update.message.reply_text(f"✅ Cek No Hp OK\n\n*Langkah terakhir*\n\nketik Email yang sudah terdaftar di Form Registrasi SWFM",parse_mode=telegram.ParseMode.MARKDOWN)
                                return REGISTRATION_EMAIL_SWFM
                            elif check_status is True:
                                query = f"select no_hp from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
                                data = client.command(query)
                                if data == nohp and data == '':
                                    if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/swfm_nohp.txt"):
                                        os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/swfm_nohp.txt")
                                        time.sleep(1)
                                    else:
                                        print("The file does not exist")
                                        time.sleep(1)
                                    data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/swfm_nohp.txt','a')
                                    data_add.write("{}".format(new_nohp_paramater))
                                    data_add.close()
                                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                    update.message.reply_text(f"✅ Cek No Hp OK\n\n*Langkah terakhir*\n\nketik Email yang sudah terdaftar di Form Registrasi SWFM",parse_mode=telegram.ParseMode.MARKDOWN)
                                    return REGISTRATION_EMAIL_SWFM
                                else:
                                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                                    update.message.reply_text("No HP anda tidak cocok di Bot Registrasi, Silahkan masukkan No HP yang sesuai",parse_mode=telegram.ParseMode.MARKDOWN)
                                    log_bot_fail_swfm(update, '*Registrasi* ➞ No HP anda tidak cocok di Bot Registrasi')
                                    return ConversationHandler.END
                            
                    else:
                        notfound.append('No HP tidak ada')
            not_found = list(set(notfound))
            check_data = found[0] == 'No HP ada'
        except:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("No HP anda belum terdaftar atau tidak cocok di Form Registrasi SWFM di Grup Wa per Region, Silahkan berkordinasi dengan atasan masing-masing (SPV TO)",parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_fail_swfm(update, '*Registrasi* ➞ No HP belum terdaftar di Form Registrasi SWFM di Grup Wa per Region')
            return ConversationHandler.END
    else:
        print("No spreadsheets available")
        return ConversationHandler.END
def registration_email_swfm(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id 
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Harap menunggu dalam beberapa detik....',parse_mode=telegram.ParseMode.MARKDOWN)
    email_paramater = update.message.text
    gspread_client = gspread.service_account(filename="/home/dimas/baru/helpdeskbot_v2/data/credential_swfm_form_user.json")
    spreadsheets = gspread_client.openall()
    if spreadsheets:
        first_spreadsheet = spreadsheets[0]
        worksheet = first_spreadsheet.get_worksheet(0)
        data = worksheet.get_all_values()
        try:
            notfound = []
            found = []
            for row in data:
                data_list = str(row).replace("[","").replace("]","").replace("'","").replace('±','').replace('+','').replace("\\\\n",' ').split('\\n')
                for data in data_list:
                    data = str(data).split(', ')
                    fullname = str(data[1]).replace('"','').replace('.','').title()
                    email = str(data[2])
                    nohp = str(data[3])
                    area = str(data[4])
                    remark = str(data[-1]).replace(' Done','Done')
                    check = email == email_paramater
                    if check is True:
                        found.append('Email ada')
                        check_remark_1 = remark == 'Done'
                        check_remark_2 = remark == 'TiaDone'
                        if check_remark_1 is True or check_remark_2 is True:
                            if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/swfm_email.txt"):
                                os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/swfm_email.txt")
                                time.sleep(1)
                            else:
                                print("The file does not exist")
                                time.sleep(1)
                            data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/swfm_email.txt','a')
                            data_add.write("{}".format(email_paramater))
                            data_add.close()
                            keyboard = [
                                [InlineKeyboardButton("Iya", callback_data=str(REGISTRATION_SWFM_END))],
                                [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                            ]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                            update.message.reply_text("Nama : {}\nEmail : {}\nNo HP : {}\nArea : {}\nRegistrasi Status : {}".format(fullname,email,nohp, area, str(remark).replace('TiaDone','✅').replace('Done','✅')))
                            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                            update.message.reply_text(f"Silahkan konfirmasi, Pilih Iya jika Benar", reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
                            return MENU_REGISTRATION
                        else:
                            target_value = nohp
                            cell_list = worksheet.findall(target_value)
                            if cell_list:
                                row_index = cell_list[0].row
                                row_data = worksheet.row_values(row_index)
                                next_column_index = len(row_data) + 1
                                new_value = "Done"
                                worksheet.update_cell(row_index, next_column_index, new_value)
                            else:
                                print("Tidak ada baris yang sesuai dengan kondisi.")
                            time.sleep(1)
                            if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/swfm_email.txt"):
                                os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/swfm_email.txt")
                                time.sleep(1)
                            else:
                                print("The file does not exist")
                                time.sleep(1)
                            data_add = open('/home/dimas/baru/helpdeskbot_v2/data_log/swfm_email.txt','a')
                            data_add.write("{}".format(email_paramater))
                            data_add.close()
                            keyboard = [
                                [InlineKeyboardButton("Iya", callback_data=str(REGISTRATION_SWFM_END))],
                                [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                            ]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                            update.message.reply_text("Nama : {}\nEmail : {}\nNo HP : {}\nArea : {}\nRegistrasi Status : ✅".format(fullname,email,nohp, area))
                            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                            update.message.reply_text(f"Silahkan konfirmasi, Pilih Iya jika Benar", reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
                            return MENU_REGISTRATION

                            # username = update.message.from_user.username
                            # if os.path.exists("/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt"):
                            #     os.remove("/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt")
                            #     time.sleep(1)
                            # else:
                            #     print("The file does not exist")
                            #     time.sleep(1)
                            # update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                            # update.message.reply_text("Nama : {}\nEmail : {}\nNo HP : {}\nArea : {}\nRegistrasi Status : {}".format(fullname,email,nohp, area, str(remark).replace('','❌')))
                            # update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                            # update.message.reply_text("Maaf, Akun belum ter-Verifkasi Admin",parse_mode=telegram.ParseMode.MARKDOWN)
                            # keyboard = [
                            #     [InlineKeyboardButton("Iya", callback_data=str(REGISTRATION_END_APPROVAL))],
                            #     [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                            # ]
                            # reply_markup = InlineKeyboardMarkup(keyboard)
                            # update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                            # update.message.reply_text(f"Pilih Iya jika membuat permintaan persetujuan Registrasi SWFM", reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
                            # log_bot = open('/home/dimas/baru/helpdeskbot_v2/data_log/approval_swfm.txt','a')
                            # log_bot.write("{},{},{},{},{}".format(fullname, username, email, nohp, area))
                            # log_bot.close()
                            # return MENU_REGISTRATION
                    else:
                        notfound.append('Email tidak ada')
            not_found = list(set(notfound))
            check_data = found[0] == 'Email ada'
        except:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Maaf, Email anda tidak cocok, Silahkan berkordinasi dengan atasan masing-masing (SPV TO)",parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_fail_swfm(update, '*Registrasi* ➞ Email tidak cocok')
            return ConversationHandler.END
    else:
        print("No spreadsheets available")
        return ConversationHandler.END

# def registration_end_approval(update: Update, _: CallbackContext) -> None:
#     query = update.callback_query
#     query.answer()
#     query.edit_message_text('Terima kasih, anda sudah terdaftar di SYANTIC BOT\nSilahkan ketik /menu untuk mengetahui menu kami')
#     username_grup = 'https://t.me/+X0NhX08BtgxiNThl'
#     button1 = InlineKeyboardButton("#Helpdesk Requests User SWFM" , url=username_grup)
#     buttons = [[button1]]
#     keyboard = InlineKeyboardMarkup(buttons)
#     query.message.reply_text('Silahkan konfirmasi melalui Admin dibawah ini', reply_markup=keyboard)
#     log_bot_inline(update, 'USER SWFM')
#     log_bot_success_inline_swfm(update, '*Registrasi* ➞ Membuat permintaan persetujuan Registrasi SWFM')
#     return ConversationHandler.END

def registration_swfm_end(update: Update, _: CallbackContext) -> None:
    full_name = update.callback_query.from_user.full_name
    username = update.callback_query.from_user.username
    chat_id = update.callback_query.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    no_hp = open('/home/dimas/baru/helpdeskbot_v2/data_log/swfm_nohp.txt','r')
    no_hp = no_hp.read()
    email = open('/home/dimas/baru/helpdeskbot_v2/data_log/swfm_email.txt','r')
    email = email.read()

    query = f"INSERT INTO production.helpdesk_bot_swfm select '{full_name}','{username}','{chat_id}','{no_hp}','{email}','Done','True','False','False','user','None','None','None','None','None','None','None','None','None','None','None','None','None','None','None','None'"
    client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text('Terima kasih, anda berhasil terdaftar MENU')
    log_bot_success_inline_swfm(update, '*Registrasi* ➞ Akun Berhasil Terdaftar MENU SWFM di SYANTIC BOT 🆕')
    return ConversationHandler.END
################################################REGISTRASI END SWFM#######################################

def panduan(update: Update, _: CallbackContext) -> None:
    grup_name = update.message.chat.title
    chatid_telegram = update.message.from_user.id 
    syanticbot = 'https://t.me/syanticbot'
    ##access
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    check_status = client.command(query)
    if grup_name:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        button1 = InlineKeyboardButton("SYANTIC BOT", url=syanticbot)
        buttons = [[button1]]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text('*SYANTIC BOT* hanya bisa di akses melalui private chatBOT. Terima kasih \nKlik tombol dibawah ini',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        log_bot_fail_swfm(update, '*Panduan* ➞ Akses melaui Grup')
        return ConversationHandler.END
    elif not grup_name:
        check_status = check_status == 1
        if check_status is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            keyboard = [
                [InlineKeyboardButton("SWFM", callback_data=str(PANDUAN_SWFM))],
                [InlineKeyboardButton("IOMS", callback_data=str(PANDUAN_IOMS))],
                [InlineKeyboardButton("IPAS", callback_data=str(PANDUAN_IPAS))],
                [InlineKeyboardButton("Batal", callback_data=str(CANCEL_HOME))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Selamat datang di Panduan")
            update.message.reply_text("Pilih :", reply_markup=reply_markup)
            return PANDUAN

        elif check_status is False:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f"Mohon registrasi terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_fail_swfm(update, '*Panduan* ➞ Akun Belum terdaftar di BOT')
            return ConversationHandler.END
def panduan_swfm(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda memilih : *SWFM*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text("https://drive.google.com/file/d/1hdQddSgdoeguui56Hg4du9tNILRgbRV9/view?usp=drive_link",parse_mode=telegram.ParseMode.HTML)
    query.message.reply_text(text="Berikut adalah Link panduan Video Tutorial penggunaan BOT, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_inline_swfm(update, '*Panduan* ➞ Panduan Tutorial BOT')
    return ConversationHandler.END
def panduan_ioms(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda memilih : *IOMS*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text("https://drive.google.com/file/d/1hlpkDE-cjw4NbtyntxmTzBZZia1OrJYk/view?usp=drive_link",parse_mode=telegram.ParseMode.HTML)
    query.message.reply_text(text="Berikut adalah Link panduan Video Tutorial penggunaan BOT, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_inline_ioms_scarlett(update, '*Panduan* ➞ Panduan Tutorial BOT')
    return ConversationHandler.END
def panduan_ipas(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda memilih : *IPAS*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text("https://drive.google.com/file/d/1hni9zflK5a15sNMDx8bl22PIRtPKqqPn/view?usp=drive_link",parse_mode=telegram.ParseMode.HTML)
    query.message.reply_text(text="Berikut adalah Link panduan Video Tutorial penggunaan BOT, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_inline_ipas(update, '*Panduan* ➞ Panduan Tutorial BOT')
    return ConversationHandler.END

#######################################################################################

def menu(update: Update, _: CallbackContext) -> None:
    full_name = update.message.from_user.full_name
    grup_name = update.message.chat.title
    chatid_telegram = update.message.from_user.id
    username = update.message.from_user.username
    syanticbot = 'https://t.me/syanticbot'
    ##access
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    # query = f"select count(*) as `count` from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    query = f"SELECT EXISTS (SELECT 1 FROM production.helpdesk_bot_swfm WHERE chatid_telegram = '{chatid_telegram}') AS user_exists"
    check_status = client.command(query)
    if grup_name:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        button1 = InlineKeyboardButton("SYANTIC BOT", url=syanticbot)
        buttons = [[button1]]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text('*SYANTIC BOT* hanya bisa di akses melalui private chatBOT. Terima kasih \nKlik tombol dibawah ini',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        log_bot_fail_swfm(update, '*Menu* ➞ Akses melaui Grup')
        return ConversationHandler.END
    elif not grup_name:
        check_status = check_status == 1
        # print(check_status)
        if not username:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f"Hallo Kak *{full_name}*, Mohon membuat *Username ID Telegram *terlebih dahulu", parse_mode=telegram.ParseMode.MARKDOWN)
            update.message.reply_text('https://drive.google.com/file/d/1T5TRaQZs-fFU7IicI5TyudczL3ZKJxAx/view?usp=drivesdk',parse_mode=telegram.ParseMode.HTML)
            update.message.reply_text('Berikut adalah Link panduan Video Tutorial membuat Usernama ID Telegram, terima kasih',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_fail_swfm(update, '*Menu* ➞ Belum membuat username ID telegram')
            return ConversationHandler.END
        elif check_status is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            keyboard = [
                [InlineKeyboardButton("IOMS", callback_data=str(MENU_IOMS))],
                [InlineKeyboardButton("IPAS", callback_data=str(MENU_IPAS))],
                [InlineKeyboardButton("SCARLETT", callback_data=str(MENU_SCARLETT))],
                [InlineKeyboardButton("SWFM", callback_data=str(MENU_SWFM))],
                [InlineKeyboardButton("Batal", callback_data=str(CANCEL_HOME))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Selamat datang di Menu")
            update.message.reply_text("Pilih dan klik aplikasi dibawah :", reply_markup=reply_markup)
            return MENU

        elif check_status is False:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f"Mohon registrasi terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_fail_swfm(update, '*Menu* ➞ Akun Belum terdaftar di BOT')
            return ConversationHandler.END
def menu_utama(update: Update, _: CallbackContext) -> None:
    ##accessMENU_IPAS
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda kembali ke *HOME*",parse_mode=telegram.ParseMode.MARKDOWN)
    keyboard = [
        [InlineKeyboardButton("IOMS", callback_data=str(MENU_IOMS))],
        [InlineKeyboardButton("IPAS", callback_data=str(MENU_IPAS))],
        [InlineKeyboardButton("SCARLETT", callback_data=str(MENU_SCARLETT))],
        [InlineKeyboardButton("SWFM", callback_data=str(MENU_SWFM))],
        [InlineKeyboardButton("Batal", callback_data=str(CANCEL_HOME))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.message.reply_text("Pilih :", reply_markup=reply_markup)

################################################MENU IPAS#######################################
def menu_scarlett(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    ##access
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_ioms from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *SCARLETT*",parse_mode=telegram.ParseMode.MARKDOWN)
    if data == 'True':
        query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
        data = client.command(query)
        query = update.callback_query
        query.answer()
        position = data == 'admin'
        if position is True: ##ADMIN
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(SCARLETT_REQTICKET))],
                [InlineKeyboardButton("Tim Ahli >>", callback_data=str(IOMS_EXPERT))],
                [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(SCARLETT_MYTICKET))],
                [InlineKeyboardButton("Broadcast Pesan", callback_data=str(IOMS_BROADCAST))],
                [InlineKeyboardButton("Jadikan Admin", callback_data=str(IOMS_MAKEADMIN))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(SCARLETT_POSTLINK))],
                [InlineKeyboardButton("Download Laporan Tiket", callback_data=str(SCARLETT_DOWNLOAD_EXCEL))],
                [InlineKeyboardButton("Hapus UserBot", callback_data=str(DEL_USERBOT))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(SCARLETT_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        elif position is False: ##USER
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(SCARLETT_REQTICKET))],
                [InlineKeyboardButton("Status Laporan", callback_data=str(SCARLETT_MYTICKET))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(SCARLETT_POSTLINK))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(SCARLETT_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        return MENU
    elif data == 'False':
        query = update.callback_query
        query.answer()
        query.message.reply_text(f"Mohon registrasi Menu SCARLETT terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_fail_inline_ioms_scarlett(update, '*Menu* ➞ Akun Belum registrasi Menu SCARLETT')
    return ConversationHandler.END
def menu_scarlett_(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    ##access
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_ioms from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *SCARLETT*",parse_mode=telegram.ParseMode.MARKDOWN)
    if data == 'True':
        query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
        data = client.command(query)
        query = update.callback_query
        query.answer()
        position = data == 'admin'
        if position is True: ##ADMIN
            try:
                message_id = query.message.message_id-1
                chat_id = update.callback_query.from_user.id
                bot_log.delete_message(chat_id,message_id)
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(SCARLETT_REQTICKET))],
                    [InlineKeyboardButton("Tim Ahli >>", callback_data=str(IOMS_EXPERT))],
                    [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(SCARLETT_MYTICKET))],
                    [InlineKeyboardButton("Broadcast Pesan", callback_data=str(IOMS_BROADCAST))],
                    [InlineKeyboardButton("Jadikan Admin", callback_data=str(IOMS_MAKEADMIN))],
                    [InlineKeyboardButton("My Ticket List", callback_data=str(SCARLETT_POSTLINK))],
                    [InlineKeyboardButton("Download Laporan Tiket", callback_data=str(SCARLETT_DOWNLOAD_EXCEL))],
                    [InlineKeyboardButton("Hapus UserBot", callback_data=str(DEL_USERBOT))],
                    [InlineKeyboardButton("Eskalasi Case", callback_data=str(SCARLETT_COMPLAINT))],
                    [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text("Pilih :", reply_markup=reply_markup)
            except:
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(SCARLETT_REQTICKET))],
                    [InlineKeyboardButton("Tim Ahli >>", callback_data=str(IOMS_EXPERT))],
                    [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(SCARLETT_MYTICKET))],
                    [InlineKeyboardButton("Broadcast Pesan", callback_data=str(IOMS_BROADCAST))],
                    [InlineKeyboardButton("Jadikan Admin", callback_data=str(IOMS_MAKEADMIN))],
                    [InlineKeyboardButton("My Ticket List", callback_data=str(SCARLETT_POSTLINK))],
                    [InlineKeyboardButton("Download Laporan Tiket", callback_data=str(SCARLETT_DOWNLOAD_EXCEL))],
                    [InlineKeyboardButton("Hapus UserBot", callback_data=str(DEL_USERBOT))],
                    [InlineKeyboardButton("Eskalasi Case", callback_data=str(SCARLETT_COMPLAINT))],
                    [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text("Pilih :", reply_markup=reply_markup)
        elif position is False: ##USER
            try:
                message_id = query.message.message_id-1
                chat_id = update.callback_query.from_user.id
                bot_log.delete_message(chat_id,message_id)
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(SCARLETT_REQTICKET))],
                    [InlineKeyboardButton("Status Laporan", callback_data=str(SCARLETT_MYTICKET))],
                    [InlineKeyboardButton("My Ticket List", callback_data=str(SCARLETT_POSTLINK))],
                    [InlineKeyboardButton("Eskalasi Case", callback_data=str(SCARLETT_COMPLAINT))],
                    [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text("Pilih :", reply_markup=reply_markup)
            except:
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(SCARLETT_REQTICKET))],
                    [InlineKeyboardButton("Status Laporan", callback_data=str(SCARLETT_MYTICKET))],
                    [InlineKeyboardButton("My Ticket List", callback_data=str(SCARLETT_POSTLINK))],
                    [InlineKeyboardButton("Eskalasi Case", callback_data=str(SCARLETT_COMPLAINT))],
                    [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text("Pilih :", reply_markup=reply_markup)
        return MENU
    elif data == 'False':
        query = update.callback_query
        query.answer()
        query.message.reply_text(f"Mohon registrasi Menu SCARLETT terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_fail_inline_ioms_scarlett(update, '*Menu* ➞ Akun Belum registrasi Menu SCARLETT')
    return ConversationHandler.END

def scarlett_reqticket(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    try:
        keyboard = [
            [InlineKeyboardButton("PreBaut >>", callback_data=str(SCARLETT_CAT1))],
            [InlineKeyboardButton("ATP Not Synchrone", callback_data=str(SCARLETT_CAT2))],
            [InlineKeyboardButton("QC button Does Not Appear", callback_data=str(SCARLETT_CAT3))],
            [InlineKeyboardButton("eLV button Does Not Appeare", callback_data=str(SCARLETT_CAT4))],
            [InlineKeyboardButton("Update PO", callback_data=str(SCARLETT_CAT5))],
            [InlineKeyboardButton("Update WBS", callback_data=str(SCARLETT_CAT6))],
            [InlineKeyboardButton("Create User", callback_data=str(SCARLETT_CAT7))],
            [InlineKeyboardButton("User Change", callback_data=str(SCARLETT_CAT8))],
            # [InlineKeyboardButton("Other Problems", callback_data=str(SCARLETT_CAT9))],
            [InlineKeyboardButton("TANYA PROSES ?", callback_data=str(SCARLETT_CAT10))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_SCARLETT_))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id-1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Penjelasan Kategori: \n*PreBaut :* Milestone Not Updated, Data Not Available\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    except:
        keyboard = [
            [InlineKeyboardButton("PreBaut >>", callback_data=str(SCARLETT_CAT1))],
            [InlineKeyboardButton("ATP Not Synchrone", callback_data=str(SCARLETT_CAT2))],
            [InlineKeyboardButton("QC button Does Not Appear", callback_data=str(SCARLETT_CAT3))],
            [InlineKeyboardButton("eLV button Does Not Appeare", callback_data=str(SCARLETT_CAT4))],
            [InlineKeyboardButton("Update PO", callback_data=str(SCARLETT_CAT5))],
            [InlineKeyboardButton("Update WBS", callback_data=str(SCARLETT_CAT6))],
            [InlineKeyboardButton("Create User", callback_data=str(SCARLETT_CAT7))],
            [InlineKeyboardButton("User Change", callback_data=str(SCARLETT_CAT8))],
            # [InlineKeyboardButton("Other Problems", callback_data=str(SCARLETT_CAT9))],
            [InlineKeyboardButton("TANYA PROSES ?", callback_data=str(SCARLETT_CAT10))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_SCARLETT_))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Penjelasan Kategori: \n*PreBaut :* Milestone Not Updated, Data Not Available\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def scarlett_reqticket_add1(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    print(data_text)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    chat_id = update.callback_query.message.chat_id
    message_id_1 = update.callback_query.message.message_id-1
    bot_log.delete_message(chat_id,message_id_1)
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'PreBaut' in data_text:
        keyboard = [
            [InlineKeyboardButton("Milestone Not Updated (Tonggak Pencapaian Tidak Diperbarui)", callback_data=str(SCARLETT_CAT1_1))],
            [InlineKeyboardButton("Data Not Available (Data Tidak Tersedia)", callback_data=str(SCARLETT_CAT1_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SCARLETT_CAT1_3))],
            [InlineKeyboardButton("Kembali", callback_data=str(SCARLETT_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def scarlett_reqticket_add2(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    try:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_SCARLETT
    except:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_SCARLETT

def scarlett_reqticket_add(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    message_id = query.message.message_id-1
    chat_id = update.callback_query.from_user.id
    bot_log.delete_message(chat_id,message_id)
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    try:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_SCARLETT
    except:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_SCARLETT

def end_scarlett(update: Update, _: CallbackContext) -> None:
    username = update.message.from_user.username
    chatid_telegram  = update.message.from_user.id 
    now = datetime.now() # current date and time
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    keterangan = update.message.text.replace(',',' ').replace(', ',' ').replace("'","").replace('"',"")
    ##Create Ticket
    characters = list(string.digits)
    length = 10
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    ticket = "SCA"+"".join(password)
    status = []
    query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data = client.command(query)
    val_check_ticket = data[3] == ticket
    problem_title = str(data[14])
    status.append(val_check_ticket)
    if status[0] is False:
        data_select = problem_title
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001966245452', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SCARLETT', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        

        time.sleep(2)
        query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data_select = client.command(query)
        query = f"INSERT INTO production.helpdesk_report_swfm select '{data_select[0]}','{data_select[1]}','{data_select[2]}','{data_select[3]}','{data_select[4]}','{data_select[5]}','{data_select[6]}','{data_select[7]}','{data_select[8]}','{data_select[9]}','{data_select[10]}','{data_select[11]}','{data_select[12]}','{data_select[13]}','{data_select[14]}','{data_select[15]}','{data_select[16]}','{data_select[17]}','{data_select[18]}','{data_select[19]}','{data_select[20]}','{data_select[21]}','{data_select[22]}','{data_select[23]}','{data_select[24]}','{data_select[25]}'"
        client.command(query)
        time.sleep(2)

        query = f"select ticket from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data = client.command(query)
        ticket_status = data
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SCARLETT'"
        check_count = client.command(query)
        check_count = check_count == 0
        if check_count is True:
            username_expert = 'https://t.me/puang_ocha'
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        else: 
            expert = []
            query = f"select expert from production.helpdesk_expert where application_name = 'SCARLETT'"
            data = client.command(query)
            expert.append(data)          
            expert = str(expert).replace('[','').replace(']','').replace("'",'').split('\\n')
            expert = expert[0]
            username_expert = 'https://t.me/{}'.format(expert)
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        log_bot(update, 'SCARLETT')
        log_bot_success_ioms_scarlett(update, '*Tiket* ➞ Telah Membuat Tiket 🎟')
    elif status[0] is True:
        characters = list(string.digits)
        length = 10
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        ticket = "SCA"+"".join(password)

        data_select = problem_title
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001966245452', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SCARLETT', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)

        time.sleep(2)
        query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data_select = client.command(query)
        query = f"INSERT INTO production.helpdesk_report_swfm select '{data_select[0]}','{data_select[1]}','{data_select[2]}','{data_select[3]}','{data_select[4]}','{data_select[5]}','{data_select[6]}','{data_select[7]}','{data_select[8]}','{data_select[9]}','{data_select[10]}','{data_select[11]}','{data_select[12]}','{data_select[13]}','{data_select[14]}','{data_select[15]}','{data_select[16]}','{data_select[17]}','{data_select[18]}','{data_select[19]}','{data_select[20]}','{data_select[21]}','{data_select[22]}','{data_select[23]}','{data_select[24]}','{data_select[25]}'"
        client.command(query)
        time.sleep(2)

        query = f"select ticket from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data = client.command(query)
        ticket_status = data
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SCARLETT'"
        check_count = client.command(query)
        check_count = check_count == 0
        if check_count is True:
            username_expert = 'https://t.me/puang_ocha'
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        else: 
            expert = []
            query = f"select expert from production.helpdesk_expert where application_name = 'SCARLETT'"
            data = client.command(query)
            expert.append(data)          
            expert = str(expert).replace('[','').replace(']','').replace("'",'').split('\\n')
            expert = expert[0]
            username_expert = 'https://t.me/{}'.format(expert)
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        log_bot(update, 'SCARLETT')
        log_bot_success_ioms_scarlett(update, '*Tiket* ➞ Telah Membuat Tiket 🎟')
    return ConversationHandler.END

def scarlett_myticket(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)

    query = update.callback_query
    query.answer()
    position = data == 'admin'
    if position is True: ##ADMIN
        query.edit_message_text(f"Anda memilih : *Status Laporan (Admin)*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text(text="Silahkan masukkan Nomor Tiket\nContoh : SCAXXXXXXXXXXX\nKlik /cancel untuk membatalkan",parse_mode=telegram.ParseMode.MARKDOWN)
    elif position is False: ##USER
        query.edit_message_text(f"Anda memilih : *Status Laporan*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text(text="Silahkan masukkan Nomor Tiket\nContoh : SCAXXXXXXXXXXX\nKlik /cancel untuk membatalkan",parse_mode=telegram.ParseMode.MARKDOWN)
    return SCARLETT_MYTICKET_PROCESS

def scarlett_myticket_process(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(f"Harap menunggu dalam beberapa detik...")
    ticket_check = update.message.text
    chatid_telegram = update.message.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    position = data == 'admin'
    if position is True: ##ADMIN
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
            check_status = client.command(query)
            check_status = check_status == 0
            if check_status is True:
                update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
                log_bot_success_ioms_scarlett(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
                return ConversationHandler.END
            elif check_status is False:
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select status from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                data_check = client.command(query)
                if data_check == 'closed':
                    update.message.reply_text(f"Maaf Ticket sudah closed\nKlik /menu")
                    log_bot_success_ioms_scarlett(update, '*Status Laporan* ➞ Ticket sudah di closed')
                    return ConversationHandler.END
                elif data_check == 'open':
                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
                    client.command(query)
                    query = f"INSERT INTO production.action_swfm select '{chatid_telegram}','{ticket_check}','None','None','None'"
                    client.command(query)
                    query = f"select * from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                    data = client.command(query)
                    full_name = str(data[0]).title()
                    requests = 'https://t.me/{}'.format(data[1])
                    no_hp = data[3]
                    ticket = data[11]
                    regional = str(data[13])
                    problem_note = str(data[14])
                    problem__ = str(data[15]).replace('\\n',' ')
                    app = data[17]
                    date = str(data[18]).replace('-',' ')
                    update.message.reply_text(f'Creation Date : {date}\nApplication : #{app}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                    
                    keyboard = [
                        [InlineKeyboardButton("Iya", callback_data=str(SCARLETT_MYTICKET_PROCESS_END))],
                        [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Pilih Iya jika benar :", reply_markup=reply_markup)
                    return SCARLETT_MYTICKET_CLOSED
        except:
            update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
            return ConversationHandler.END
    elif position is False: ##USER
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select count(*) as `count` from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and ticket = '{ticket_check}'"
            check_status = client.command(query)
            check_status = check_status == 0
            if check_status is True:
                update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
                log_bot_success_ioms_scarlett(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
                return ConversationHandler.END
            elif check_status is False:
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select status from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                data_check = client.command(query)
                if data_check == 'closed':
                    update.message.reply_text(f"Maaf Ticket sudah closed\nKlik /menu")
                    log_bot_success_ioms_scarlett(update, '*Status Laporan* ➞ Ticket sudah di closed')
                    return ConversationHandler.END
                elif data_check == 'open':
                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
                    client.command(query)
                    query = f"INSERT INTO production.action_swfm select '{chatid_telegram}','{ticket_check}','None','None','None'"
                    client.command(query)
                    query = f"select * from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                    data = client.command(query)
                    full_name = str(data[0]).title()
                    requests = 'https://t.me/{}'.format(data[1])
                    no_hp = data[3]
                    ticket = data[11]
                    regional = str(data[13])
                    problem_note = str(data[14])
                    problem__ = str(data[15]).replace('\\n',' ')
                    app = data[17]
                    date = str(data[18]).replace('-',' ')
                    update.message.reply_text(f'Creation Date : {date}\nApplication : #{app}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                    
                    keyboard = [
                        [InlineKeyboardButton("Iya", callback_data=str(SCARLETT_MYTICKET_PROCESS_END))],
                        [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Pilih Iya jika benar :", reply_markup=reply_markup)
                    return SCARLETT_MYTICKET_CLOSED
        except:
            update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Status Laporan* ➞ Tidak memiliki laporan')
            return ConversationHandler.END
def scarlett_myticket_closed(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Masukkan resolution action :",parse_mode=telegram.ParseMode.MARKDOWN)
    return SCARLETT_MYTICKET_CLOSED_END

def scarlett_myticket_closed_end(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id
    full_name_closed = update.message.from_user.full_name
    handle_by = update.message.from_user.username
    now = datetime.now()
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    parameter = update.message.text.replace(',','.')
    update.message.reply_text("Proses closed tiket ...")
    time.sleep(3)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select * from production.action_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    data_list = str(data_select).replace("[","").replace("]","").replace("'","").replace('±','').replace('+','').replace("\\\\n",' ').split('\\n')
    for data in data_list:
        data = str(data).split(', ')
        ticket_log = data[1]

    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_report_swfm update  action_handle_by = '{handle_by}', action_resolution = '{parameter}', close_ticket_date = '{date_time}', status = 'closed' WHERE ticket = '{ticket_log}'"
    client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select username_telegram,fullname_telegram from production.helpdesk_report_swfm where ticket = '{ticket_log}'"
    data = client.command(query)
    requests = 'https://t.me/{}'.format(data[0])
    full_name = str(data[1]).title()
    update.message.reply_text(f"✅ Tiket [{full_name}]({requests}) telah closed\nKlik /menu", parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select username_telegram, fullname_telegram, channel_chatid, open_ticket_date, close_ticket_date, chatid_telegram from production.helpdesk_report_swfm where ticket = '{ticket_log}'"
    check_ticket = client.command(query)
    data_list = str(check_ticket).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    x = []
    for data in data_list:
        data = str(data).split(', ')

        open_str = f'{data[3]}, {data[4]}'
        closed_str = f'{data[5]}, {data[6]}'
        full_name = data[1]
        # Parsing string menjadi objek datetime
        open_date = datetime.strptime(open_str, "%d-%B-%Y, %H:%M:%S WIB")
        closed_date = datetime.strptime(closed_str, "%d-%B-%Y, %H:%M:%S WIB")
        # Menghitung selisih waktu
        selisih_waktu = closed_date - open_date
        # Mengambil selisih dalam bentuk hari
        day_difference = selisih_waktu
        
        #grup
        bot_log.send_message(chat_id=data[2],text=f'✅ Tiket *{ticket_log}* dari [{data[1]}]({data[0]}) telah *Terclosed* oleh {full_name_closed} dengan durasi → *{day_difference}*',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        ##user
        bot_log.send_message(chat_id=data[7],text=f'✅ Tiket anda *{ticket_log}* telah *Terclosed* oleh Admin HD {full_name_closed} dengan durasi → *{day_difference}*',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        log_bot_success_ioms_scarlett(update, '*Tiket* ➞ Closed Tiket ✅')
    #HAPUS
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    return ConversationHandler.END

def scarlett_postlink(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Anda memilih : *My Ticket List*',parse_mode=telegram.ParseMode.MARKDOWN)
    try:
        query = f"select fullname_telegram, username_telegram, ticket, problem_title, post_link from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' and category = 'SCARLETT' and status = 'open'"
        data = client.command(query)
        query = f"select count(*) as `count` from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and category = 'SCARLETT' and status = 'open'"
        count_query = client.command(query)
        query = update.callback_query
        query.answer()
        check_status = count_query == 0
        if check_status is True:
            query.message.reply_text(f'Maaf anda tidak mempunyai My Ticket List',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_ioms_scarlett(update, '*My Ticket List* ➞ My Ticket List Tidak Ditemukan')
        elif check_status is False:
            query = f"select fullname_telegram, username_telegram, ticket, problem_title, post_link from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and category = 'SCARLETT' and status = 'open'"
            data1 = client.command(query)
            query = update.callback_query
            query.answer()
            data_list = str(data1).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
            output_text = ''
            output_text += '*Berikut adalah My Ticket List anda*\n\n'
            output_text += '*Category - Ticket - Post Link*\n'
            for data in data_list:
                data = str(data).split(', ')
                ticket = data[2]
                problem_title = str(data[3]).split(' ➞ ')[0]
                post_link = data[4]
                output_text += f"{problem_title} - {ticket} - {post_link}\n"
            output_text += '\n'
            output_text += 'Regards\nOCHABOT & Team'
            query.message.reply_text(f'{output_text}',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_ioms_scarlett(update, '*My Ticket List* ➞ My Ticket List Ditemukan')
        return ConversationHandler.END
    except:
        query = update.callback_query
        query.answer()
        query.message.reply_text(f'Maaf anda tidak mempunyai My Ticket List',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_ioms_scarlett(update, '*My Ticket List* ➞ My Ticket List Tidak Ditemukan')
        return ConversationHandler.END

def scarlett_download_excel(update: Update, _: CallbackContext) -> None: 
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Mohon menunggu dalam beberapa detik...",parse_mode=telegram.ParseMode.MARKDOWN)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select * from production.helpdesk_report_swfm hrs  where status = 'open' and category = 'SCARLETT'"
    data = client.command(query)
    try:
        data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
        array_data = []
        for data in data_list:
            data = str(data).split(', ')
            dub_data = {'Nama': f'{data[0]}', 'Username Telegram': f'{data[1]}', 'Chatid Telegram': f'{data[2]}', 'No HP': f'{data[3]}', 'Email': f'{data[4]}', 'Remark': f'{data[5]}', 'Position' : f'{data[9]}', 'Channel Chatid': f'{data[10]}', 'Ticket': f'{data[11]}', 'Divison': f'{data[12]}', 'Regional': f'{data[13]}', 'Problem Title': f'{data[14]}', 'Problem Summary': f'{data[15]}', 'Status': f'{data[16]}', 'Category': f'{data[17]}', 'Open Ticket Date': f'{data[18]}, {data[19]}', 'Closed Ticket Date': f'{data[20]}', 'FCAPS': f'{data[21]}', 'Action Menu': f'{data[22]}', 'Action Category': f'{data[23]}', 'Action Handle By': f'{data[24]}', 'Action Resolution': f'{data[25]}', 'Post Link': f'{data[26]}'}
            array_data.append(dub_data)
    except:
        array_data = [{'Nama': '-', 'Username Telegram': '-', 'Chatid Telegram': '-', 'No HP': '-', 'Email': '-', 'Remark': '-', 'Position' : '-', 'Channel Chatid': '-', 'Ticket': '-', 'Divison': '-', 'Regional': '-', 'Problem Title': '-', 'Problem Summary': '-', 'Status': '-', 'Category': '-', 'Open Ticket Date': '- -', 'Closed Ticket Date': '-', 'FCAPS': '-', 'Action Menu': '-', 'Action Category': '-', 'Action Handle By': '-', 'Action Resolution': '-', 'Post Link': '-'}]
    query = f"select * from production.helpdesk_report_swfm hrs  where status = 'closed' and category = 'SCARLETT'"
    data = client.command(query)
    data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    array_data1 = []
    for data in data_list:
        data = str(data).split(', ')
        dub_data = {'Nama': f'{data[0]}', 'Username Telegram': f'{data[1]}', 'Chatid Telegram': f'{data[2]}', 'No HP': f'{data[3]}', 'Email': f'{data[4]}', 'Remark': f'{data[5]}', 'Position' : f'{data[9]}', 'Channel Chatid': f'{data[10]}', 'Ticket': f'{data[11]}', 'Divison': f'{data[12]}', 'Regional': f'{data[13]}', 'Problem Title': f'{data[14]}', 'Problem Summary': f'{data[15]}', 'Status': f'{data[16]}', 'Category': f'{data[17]}', 'Open Ticket Date': f'{data[18]}, {data[19]}', 'Closed Ticket Date': f'{data[20]},{data[21]}', 'FCAPS': f'{data[22]}', 'Action Menu': f'{data[23]}', 'Action Category': f'{data[24]}', 'Action Handle By': f'{data[25]}', 'Action Resolution': f'{data[26]}', 'Post Link': f'{data[27]}'}
        array_data1.append(dub_data)

    df1 = pd.DataFrame(array_data)
    df2 = pd.DataFrame(array_data1)
    writer = pd.ExcelWriter('/home/dimas/baru/helpdeskbot_v2/data/data_report_open_ticket_scarlett.xlsx', engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Open Ticket', index=False)
    df2.to_excel(writer, sheet_name='Closed Ticket', index=False)
    writer.save()
    print('Sukses')
    syanticbot = telegram.Bot(token_bot) #SYANTICBOT
    syanticbot.sendDocument(chat_id = chatid_telegram, document=open('/home/dimas/baru/helpdeskbot_v2/data/data_report_open_ticket_scarlett.xlsx','rb'), filename="Report Ticket SCARLETT.xlsx",caption='Ready to download Report Ticket SCARLETT')
    query = update.callback_query
    query.answer()
    query.message.reply_text(text="Berikut adalah link Download Aplikasi SCARLETT, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_inline_ioms_scarlett(update, '*Download* ➞ Laporan Tiket Excel')
    return ConversationHandler.END

def scarlett_complaint(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Anda memilih : *Eskalasi Case*',parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(f'Ketik nomor ticket anda SCAXXXXXX',parse_mode=telegram.ParseMode.MARKDOWN)
    return SCARLETT_COMPLAINT_END

def scarlett_complaint_end(update: Update, _: CallbackContext) -> None: 
    parameter_ticket = update.message.text
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{parameter_ticket}' and category = 'SCARLETT'"
    check_status = client.command(query)
    check_status = check_status == 0
    if check_status is True:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f"Nomor tiket tidak sesuai kategori atau salah", parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_ioms_scarlett(update, '*Eskalasi Case* ➞ Nomor Tiket Tidak Ditemukan')
    elif check_status is False:
        query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{parameter_ticket}' and category = 'SCARLETT' and status = 'closed'"
        check_status = client.command(query)
        check_status = check_status == 0
        if check_status is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f"Nomor tiket telah closed", parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_ioms_scarlett(update, '*Eskalasi Case* ➞ Nomor Tiket Telah Closed')
        elif check_status is False:
            chatid_1 = '1464528446'
            chatid_2 = '1745401090'
            query = f"select ticket, post_link from production.helpdesk_report_swfm where ticket = '{parameter_ticket}'"
            data_redirect = client.command(query)
            post_link = data_redirect[1]
            bot_log.send_message(chat_id=chatid_1,text=f'Semangat Pagi Rekan...\n\nNomor Tiket  {parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_2,text=f'Semangat Pagi Rekan...\n\nNomor Tiket  {parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            log_bot_success_ioms_com(update, '*Eskalasi Case* ➞ Eskalasi Case Berhasil dengan Nomor Tiket '+parameter_ticket)
            update.message.reply_text(f"Anda berhasil membuat Eskalasi Case, Mohon ditunggu sampai Team HD merespon di room diskusi. Terima Kasih", parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END

################################################MENU IOMS#######################################
def menu_ioms(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    ##access
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_ioms from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *IOMS*",parse_mode=telegram.ParseMode.MARKDOWN)
    if data == 'True':
        query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
        data = client.command(query)
        query = update.callback_query
        query.answer()
        position = data == 'admin'
        if position is True: ##ADMIN
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IOMS_REQTICKET))],
                [InlineKeyboardButton("Tim Ahli >>", callback_data=str(IOMS_EXPERT))],
                [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(IOMS_MYTICKET))],
                [InlineKeyboardButton("Broadcast Pesan", callback_data=str(IOMS_BROADCAST))],
                [InlineKeyboardButton("Jadikan Admin", callback_data=str(IOMS_MAKEADMIN))],
                [InlineKeyboardButton("Hapus UserBot", callback_data=str(DEL_USERBOT))],[InlineKeyboardButton("Download Laporan Tiket", callback_data=str(IOMS_DOWNLOAD_EXCEL))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(IOMS_POSTLINK))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(IOMS_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        elif position is False: ##USER
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IOMS_REQTICKET))],
                [InlineKeyboardButton("Status Laporan", callback_data=str(IOMS_MYTICKET))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(IOMS_POSTLINK))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(IOMS_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        return MENU
    elif data == 'False':
        query = update.callback_query
        query.answer()
        query.message.reply_text(f"Mohon registrasi Menu IOMS terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_fail_inline_ioms_scarlett(update, '*Menu* ➞ Akun Belum registrasi Menu IOMS')
    return ConversationHandler.END
def menu_ioms_(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    ##access
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_ioms from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *IOMS*",parse_mode=telegram.ParseMode.MARKDOWN)
    if data == 'True':
        query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
        data = client.command(query)
        query = update.callback_query
        query.answer()
        position = data == 'admin'
        if position is True: ##ADMIN
            message_id = query.message.message_id-1
            chat_id = update.callback_query.from_user.id
            bot_log.delete_message(chat_id,message_id)
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IOMS_REQTICKET))],
                [InlineKeyboardButton("Tim Ahli >>", callback_data=str(IOMS_EXPERT))],
                [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(IOMS_MYTICKET))],
                [InlineKeyboardButton("Broadcast Pesan", callback_data=str(IOMS_BROADCAST))],
                [InlineKeyboardButton("Jadikan Admin", callback_data=str(IOMS_MAKEADMIN))],
                [InlineKeyboardButton("Hapus UserBot", callback_data=str(DEL_USERBOT))],[InlineKeyboardButton("Download Laporan Tiket", callback_data=str(IOMS_DOWNLOAD_EXCEL))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(IOMS_POSTLINK))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(IOMS_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        elif position is False: ##USER
            message_id = query.message.message_id-1
            chat_id = update.callback_query.from_user.id
            bot_log.delete_message(chat_id,message_id)
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IOMS_REQTICKET))],
                [InlineKeyboardButton("Status Laporan", callback_data=str(IOMS_MYTICKET))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(IOMS_POSTLINK))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(IOMS_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        return MENU
    elif data == 'False':
        query = update.callback_query
        query.answer()
        query.message.reply_text(f"Mohon registrasi Menu IOMS terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_fail_inline_ioms_scarlett(update, '*Menu* ➞ Akun Belum registrasi Menu IOMS')
    return ConversationHandler.END

def ioms_reqticket(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    try:
        keyboard = [
            [InlineKeyboardButton("Aplication Error >>", callback_data=str(IOMS_CAT12))],
            [InlineKeyboardButton("Acceptance >>", callback_data=str(IOMS_CAT1))],
            [InlineKeyboardButton("Budget >>", callback_data=str(IOMS_CAT13))],
            [InlineKeyboardButton("Deployment >>", callback_data=str(IOMS_CAT2))],
            [InlineKeyboardButton("Issue Partial Baut >>", callback_data=str(IOMS_CAT4))],
            [InlineKeyboardButton("Process >>", callback_data=str(IOMS_CAT3))],
            [InlineKeyboardButton("Login >>", callback_data=str(IOMS_CAT5))],
            [InlineKeyboardButton("Dashboard >>", callback_data=str(IOMS_CAT6))],
            [InlineKeyboardButton("Tasklist >>", callback_data=str(IOMS_CAT7))],
            [InlineKeyboardButton("Planning >>", callback_data=str(IOMS_CAT8))],
            [InlineKeyboardButton("Knowledge >>", callback_data=str(IOMS_CAT9))],
            [InlineKeyboardButton("Eligibility Check >>", callback_data=str(IOMS_CAT10))],
            # [InlineKeyboardButton("Other Problems", callback_data=str(IOMS_CAT11))],
            [InlineKeyboardButton("TANYA PROSES ?", callback_data=str(IOMS_CAT14))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_IOMS_))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Penjelasan Kategori: \n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*Acceptance :* Add Case, Cancel Case, Change Case, Document Case, Error Case, Generate Case, Requests Case, Submit & Resubmit Case, Update Case, Approval RFI, BOQ List Empty, Data Not Synchrone, Database Timeout Query, Duplicate SOWID, Fallback Status eOA, Guideline, Propose Milestone, Request OA, Reviewer User, Signature Blank, Status Workflow, Sync NEID\n*Budget :* Capex Balance, Justification, FBP (KBR/KPAA), Corsec, Reporting\n*Deployment :* Add Menu, Data Not Synchrone, Document Workflow, Error Data, Error Download Data, Error Export Data, Error Login, Error Menu, Request Delete Milestone, Request New Menu, Status Workflow\n*Issue Partial Baut :* Request Milestone\n*Process :* Data Not Synchrone, Request Mapping SOWID\n*Login :* Add User, Cant Login\n*Dashboard :* Data Not Synchrone, Duplicate Site, Duplicate SOWID, Request New Menu, Status Workflow\n*Tasklist :* Data Not Synchrone, Document Workflow, Duplicate eLV, Duplicate eOA, Error Duplicate ATP, Error Menu, Status Workflow\n*Planning :* Data Not Synchronice, Document Workflow, Request Delete eMOM, Request Delete Site List, Request Take Out eKKST, Update Data, Update Menu, Update NE ID\n*Knowledge :* Update Menu\n*Eligibility Check :* Data Not Synchrone\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    except:
        keyboard = [
            [InlineKeyboardButton("Aplication Error >>", callback_data=str(IOMS_CAT12))],
            [InlineKeyboardButton("Acceptance >>", callback_data=str(IOMS_CAT1))],
            [InlineKeyboardButton("Budget >>", callback_data=str(IOMS_CAT13))],
            [InlineKeyboardButton("Deployment >>", callback_data=str(IOMS_CAT2))],
            [InlineKeyboardButton("Issue Partial Baut >>", callback_data=str(IOMS_CAT4))],
            [InlineKeyboardButton("Process >>", callback_data=str(IOMS_CAT3))],
            [InlineKeyboardButton("Login >>", callback_data=str(IOMS_CAT5))],
            [InlineKeyboardButton("Dashboard >>", callback_data=str(IOMS_CAT6))],
            [InlineKeyboardButton("Tasklist >>", callback_data=str(IOMS_CAT7))],
            [InlineKeyboardButton("Planning >>", callback_data=str(IOMS_CAT8))],
            [InlineKeyboardButton("Knowledge >>", callback_data=str(IOMS_CAT9))],
            [InlineKeyboardButton("Eligibility Check >>", callback_data=str(IOMS_CAT10))],
            # [InlineKeyboardButton("Other Problems", callback_data=str(IOMS_CAT11))],
            [InlineKeyboardButton("TANYA PROSES ?", callback_data=str(IOMS_CAT14))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_IOMS_))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Penjelasan Kategori: \n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*Acceptance :* Add Case, Cancel Case, Change Case, Document Case, Error Case, Generate Case, Requests Case, Submit & Resubmit Case, Update Case, Approval RFI, BOQ List Empty, Data Not Synchrone, Database Timeout Query, Duplicate SOWID, Fallback Status eOA, Guideline, Propose Milestone, Request OA, Reviewer User, Signature Blank, Status Workflow, Sync NEID\n*Budget :* Capex Balance, Justification, FBP (KBR/KPAA), Corsec, Reporting\n*Deployment :* Add Menu, Data Not Synchrone, Document Workflow, Error Data, Error Download Data, Error Export Data, Error Login, Error Menu, Request Delete Milestone, Request New Menu, Status Workflow\n*Issue Partial Baut :* Request Milestone\n*Process :* Data Not Synchrone, Request Mapping SOWID\n*Login :* Add User, Cant Login\n*Dashboard :* Data Not Synchrone, Duplicate Site, Duplicate SOWID, Request New Menu, Status Workflow\n*Tasklist :* Data Not Synchrone, Document Workflow, Duplicate eLV, Duplicate eOA, Error Duplicate ATP, Error Menu, Status Workflow\n*Planning :* Data Not Synchronice, Document Workflow, Request Delete eMOM, Request Delete Site List, Request Take Out eKKST, Update Data, Update Menu, Update NE ID\n*Knowledge :* Update Menu\n*Eligibility Check :* Data Not Synchrone\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def ioms_reqticket_(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    keyboard = [
            [InlineKeyboardButton("Aplication Error >>", callback_data=str(IOMS_CAT12))],
            [InlineKeyboardButton("Acceptance >>", callback_data=str(IOMS_CAT1))],
            [InlineKeyboardButton("Budget >>", callback_data=str(IOMS_CAT13))],
            [InlineKeyboardButton("Deployment >>", callback_data=str(IOMS_CAT2))],
            [InlineKeyboardButton("Issue Partial Baut >>", callback_data=str(IOMS_CAT4))],
            [InlineKeyboardButton("Process >>", callback_data=str(IOMS_CAT3))],
            [InlineKeyboardButton("Login >>", callback_data=str(IOMS_CAT5))],
            [InlineKeyboardButton("Dashboard >>", callback_data=str(IOMS_CAT6))],
            [InlineKeyboardButton("Tasklist >>", callback_data=str(IOMS_CAT7))],
            [InlineKeyboardButton("Planning >>", callback_data=str(IOMS_CAT8))],
            [InlineKeyboardButton("Knowledge >>", callback_data=str(IOMS_CAT9))],
            [InlineKeyboardButton("Eligibility Check >>", callback_data=str(IOMS_CAT10))],
            # [InlineKeyboardButton("Other Problems", callback_data=str(IOMS_CAT11))],
            [InlineKeyboardButton("TANYA PROSES ?", callback_data=str(IOMS_CAT14))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_IOMS))],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    message_id = query.message.message_id-1
    chat_id = update.callback_query.from_user.id
    bot_log.delete_message(chat_id,message_id)
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text("Penjelasan Kategori: \n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*Acceptance :* Add Case, Cancel Case, Change Case, Document Case, Error Case, Generate Case, Requests Case, Submit & Resubmit Case, Update Case, Approval RFI, BOQ List Empty, Data Not Synchrone, Database Timeout Query, Duplicate SOWID, Fallback Status eOA, Guideline, Propose Milestone, Request OA, Reviewer User, Signature Blank, Status Workflow, Sync NEID\n*Budget :* Capex Balance, Justification, FBP (KBR/KPAA), Corsec, Reporting\n*Deployment :* Add Menu, Data Not Synchrone, Document Workflow, Error Data, Error Download Data, Error Export Data, Error Login, Error Menu, Request Delete Milestone, Request New Menu, Status Workflow\n*Issue Partial Baut :* Request Milestone\n*Process :* Data Not Synchrone, Request Mapping SOWID\n*Login :* Add User, Cant Login\n*Dashboard :* Data Not Synchrone, Duplicate Site, Duplicate SOWID, Request New Menu, Status Workflow\n*Tasklist :* Data Not Synchrone, Document Workflow, Duplicate eLV, Duplicate eOA, Error Duplicate ATP, Error Menu, Status Workflow\n*Planning :* Data Not Synchronice, Document Workflow, Request Delete eMOM, Request Delete Site List, Request Take Out eKKST, Update Data, Update Menu, Update NE ID\n*Knowledge :* Update Menu\n*Eligibility Check :* Data Not Synchrone\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text("Pilih :",reply_markup=reply_markup)

def ioms_reqticket_add(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    chat_id = update.callback_query.message.chat_id
    message_id_1 = update.callback_query.message.message_id-1
    bot_log.delete_message(chat_id,message_id_1)
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'Acceptance' in data_text:
        keyboard = [
            [InlineKeyboardButton("Add Case (Semua Kasus Tambah) >>", callback_data=str(IOMS_CAT1_CASE_A_1))],
            [InlineKeyboardButton("Cancel Case (Semua Kasus Batal) >>", callback_data=str(IOMS_CAT1_CASE_A_2))],
            [InlineKeyboardButton("Change Case (Semua Kasus Perubahan) >>", callback_data=str(IOMS_CAT1_CASE_A_3))],
            [InlineKeyboardButton("Document Case (Semua Kasus Dokumen) >>", callback_data=str(IOMS_CAT1_CASE_A_4))],
            [InlineKeyboardButton("Error Case (Semua Kasus Kesalahan) >>", callback_data=str(IOMS_CAT1_CASE_A_5))],
            [InlineKeyboardButton("Generate Case (Semua Kasus Generate) >>", callback_data=str(IOMS_CAT1_CASE_A_6))],
            [InlineKeyboardButton("Requests Case (Semua Kasus Permintaan) >>", callback_data=str(IOMS_CAT1_CASE_A_7))],
            [InlineKeyboardButton("Submit & Resubmit Case (Semua Kasus Kirim & Kirim Ulang) >>", callback_data=str(IOMS_CAT1_CASE_A_8))],
            [InlineKeyboardButton("Update Case (Semua Kasus Update) >>", callback_data=str(IOMS_CAT1_CASE_A_9))],
            [InlineKeyboardButton("Approval RFI (Persetujuan RFI)", callback_data=str(IOMS_CAT1_1))],
            [InlineKeyboardButton("BOQ List Empty (Daftar BOQ Kosong)", callback_data=str(IOMS_CAT1_2))],
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(IOMS_CAT1_3))],
            [InlineKeyboardButton("Database Timeout Query (Kueri Batas Waktu Database)", callback_data=str(IOMS_CAT1_4))],
            [InlineKeyboardButton("Duplicate SOWID (Duplikat SOWID)", callback_data=str(IOMS_CAT1_5))],
            [InlineKeyboardButton("Fallback Status eOA (Status Penggantian eOA)", callback_data=str(IOMS_CAT1_6))],
            [InlineKeyboardButton("Guideline (Pedoman)", callback_data=str(IOMS_CAT1_7))],
            [InlineKeyboardButton("Propose Milestone (Usulkan Tonggak Pencapaian)", callback_data=str(IOMS_CAT1_8))],
            [InlineKeyboardButton("Request OA (Permintaan OA)", callback_data=str(IOMS_CAT1_9))],
            [InlineKeyboardButton("Reviewer User (Pengguna Peninjau)", callback_data=str(IOMS_CAT1_10))],
            [InlineKeyboardButton("Signature Blank (Tanda Tangan Kosong)", callback_data=str(IOMS_CAT1_11))],
            [InlineKeyboardButton("Status Workflow (Alur Kerja Status)", callback_data=str(IOMS_CAT1_12))],
            [InlineKeyboardButton("Sync NEID (Sinkronkan NEID)", callback_data=str(IOMS_CAT1_13))],
            # [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_14))],
            
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET_))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Penjelasan Kategori: \n*Add Case :* Add Menu, Add User\n*Cancel Case :* Cancel ATP, Cancel BOQ, Cancel eATP\n*Change Case :* Change Approval QC, Change BOQ\n*Document Case :* Document Not Appearing, Document Not Synchrone, Document Workflow \n*Error Case :* Error Data, Error Database, Error Document, Error Download Data, Error Export Data, Error Generate ATP, Error Generate QC, Error Generate SQAC, Error Input Data, Error Menu, Error Submit ATP, Error Submit ELV, Error Upload BOQ, Error User\n*Generate Case :* Cant Generate QC, Cant Generate ATP, Cant Generata eOA, Cant Generata QC\n*Requests Case :* Request BOQ, Request Cancel, Request Delete eMOM, Request Delete LV, Request Delete MOS, Request Mapping SOWID, Request New Menu, Request Reupload ATP, Request User\n*Submit & Resubmit Case :* Cant Submit eLV, Cant Resubmit OA\n*Update Case :* Update ATP, Update Data, Update Database, Update Menu, Update NE ID, Update PO, Update SOW\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Aplication Error' in data_text:
        keyboard = [
            [InlineKeyboardButton("Loading after Login (Loading Setelah Login)", callback_data=str(IOMS_CAT12_1))],
            [InlineKeyboardButton("Log out Yourself (Logout Sendiri)", callback_data=str(IOMS_CAT12_2))],
            [InlineKeyboardButton("Hang (Gantung)", callback_data=str(IOMS_CAT12_3))],
            # [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT12_4))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Deployment' in data_text:
        keyboard = [
            [InlineKeyboardButton("Add Menu (Tambah Menu)", callback_data=str(IOMS_CAT2_1))],
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(IOMS_CAT2_2))],
            [InlineKeyboardButton("Document Workflow (Alur Kerja Dokumen)", callback_data=str(IOMS_CAT2_3))],
            [InlineKeyboardButton("Error Data (Kesalahan Data)", callback_data=str(IOMS_CAT2_4))],
            [InlineKeyboardButton("Error Download Data (Kesalahan Unduh Data)", callback_data=str(IOMS_CAT2_5))],
            [InlineKeyboardButton("Error Export Data (Kesalahan Ekspor Data)", callback_data=str(IOMS_CAT2_6))],
            [InlineKeyboardButton("Error Login (Kesalahan Gabung)", callback_data=str(IOMS_CAT2_7))],
            [InlineKeyboardButton("Error Menu (Kesalahan Menu)", callback_data=str(IOMS_CAT2_8))],
            [InlineKeyboardButton("Request Delete Milestone (Permintaan Hapus Tonggak Pencapaian)", callback_data=str(IOMS_CAT2_9))],
            [InlineKeyboardButton("Request New Menu (Permintaan Menu Baru)", callback_data=str(IOMS_CAT2_10))],
            [InlineKeyboardButton("Status Workflow (Alur Kerja Status)", callback_data=str(IOMS_CAT2_11))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT2_12))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Process' in data_text:
        keyboard = [
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(IOMS_CAT3_1))],
            [InlineKeyboardButton("Request Mapping SOWID (Permintaan Pemetaan SOWID)", callback_data=str(IOMS_CAT3_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT3_3))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Issue Partial Baut' in data_text:
        keyboard = [
            [InlineKeyboardButton("Request Milestone (Permintaan Tonggak Pencapaian)", callback_data=str(IOMS_CAT4_1))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT4_2))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Login' in data_text:
        keyboard = [
            [InlineKeyboardButton("Add User (Tambah User)", callback_data=str(IOMS_CAT5_1))],
            [InlineKeyboardButton("Cant Login (Tidak Dapat Gabung)", callback_data=str(IOMS_CAT5_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT5_3))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Dashboard' in data_text:
        keyboard = [
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(IOMS_CAT6_1))],
            [InlineKeyboardButton("Duplicate Site (Situs Duplikat)", callback_data=str(IOMS_CAT6_2))],
            [InlineKeyboardButton("Duplicate SOWID (Duplikat SOWID)", callback_data=str(IOMS_CAT6_3))],
            [InlineKeyboardButton("Request New Menu (Permintaan Menu Baru)", callback_data=str(IOMS_CAT6_4))],
            [InlineKeyboardButton("Status Workflow (Alur Kerja Status)", callback_data=str(IOMS_CAT6_5))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT6_6))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Tasklist' in data_text:
        keyboard = [
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(IOMS_CAT7_1))],
            [InlineKeyboardButton("Document Workflow (Alur Kerja Dokumen)", callback_data=str(IOMS_CAT7_2))],
            [InlineKeyboardButton("Duplicate eLV (Duplikat eLV)", callback_data=str(IOMS_CAT7_3))],
            [InlineKeyboardButton("Duplicate eOA (Duplikat eOA)", callback_data=str(IOMS_CAT7_4))],
            [InlineKeyboardButton("Error Duplicate ATP (Kesalahan Duplikat ATP)", callback_data=str(IOMS_CAT7_5))],
            [InlineKeyboardButton("Error Menu (Kesalahan Menu)", callback_data=str(IOMS_CAT7_6))],
            [InlineKeyboardButton("Status Workflow (Alur Kerja Status)", callback_data=str(IOMS_CAT7_7))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT7_8))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Planning' in data_text:
        keyboard = [
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(IOMS_CAT8_1))],
            [InlineKeyboardButton("Document Workflow (Alur Kerja Dokumen)", callback_data=str(IOMS_CAT8_2))],
            [InlineKeyboardButton("Request Delete eMOM (Permintaan Hapus eMOM)", callback_data=str(IOMS_CAT8_3))],
            [InlineKeyboardButton("Request Delete Site List (Permintaan Hapus Daftar Situs)", callback_data=str(IOMS_CAT8_4))],
            [InlineKeyboardButton("Request Take Out eKKST (Permintaan Hapus eKKST)", callback_data=str(IOMS_CAT8_5))],
            [InlineKeyboardButton("Update Data (Perbaharui Data)", callback_data=str(IOMS_CAT8_6))],
            [InlineKeyboardButton("Update Menu (Perbaharui Manu)", callback_data=str(IOMS_CAT8_7))],
            [InlineKeyboardButton("Update NE ID (Perbaharui NE ID)", callback_data=str(IOMS_CAT8_8))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT8_9))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Knowledge' in data_text:
        keyboard = [
            [InlineKeyboardButton("Update Menu (Perbaharui Menu)", callback_data=str(IOMS_CAT9_1))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT9_2))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Eligibility Check' in data_text:
        keyboard = [
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(IOMS_CAT10_1))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT10_2))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Budget' in data_text:
        keyboard = [
            [InlineKeyboardButton("Capex Balance (Saldo Belanja Modal)", callback_data=str(IOMS_CAT13_1))],
            [InlineKeyboardButton("Justification (Pembenaran)", callback_data=str(IOMS_CAT13_2))],
            [InlineKeyboardButton("FBP (KBR/KPAA) (FBP (KBR/KPAA))", callback_data=str(IOMS_CAT13_3))],
            [InlineKeyboardButton("Corsec (Corsec)", callback_data=str(IOMS_CAT13_4))],
            [InlineKeyboardButton("Reporting (Laporan)", callback_data=str(IOMS_CAT13_5))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT13_6))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Other Problems' in data_text:
        chatid_telegram = update.callback_query.from_user.id

        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
        data_select = client.command(query)
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select}' where chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None' WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_IOMS
    elif 'TANYA PROSES ?' in data_text:
        keyboard = [
            [InlineKeyboardButton("Acceptance", callback_data=str(IOMS_CAT14_1))],
            [InlineKeyboardButton("Budget", callback_data=str(IOMS_CAT14_2))],
            [InlineKeyboardButton("Deployment", callback_data=str(IOMS_CAT14_3))],
            [InlineKeyboardButton("Issue Partial Baut", callback_data=str(IOMS_CAT14_4))],
            [InlineKeyboardButton("Process", callback_data=str(IOMS_CAT14_5))],
            [InlineKeyboardButton("Login", callback_data=str(IOMS_CAT14_6))],
            [InlineKeyboardButton("Dashboard", callback_data=str(IOMS_CAT14_7))],
            [InlineKeyboardButton("Tasklist", callback_data=str(IOMS_CAT14_8))],
            [InlineKeyboardButton("Planning", callback_data=str(IOMS_CAT14_9))],
            [InlineKeyboardButton("Knowledge", callback_data=str(IOMS_CAT14_10))],
            [InlineKeyboardButton("Eligibility Check", callback_data=str(IOMS_CAT14_11))],
            [InlineKeyboardButton("Kembali", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def ioms_reqticket_case_a(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]

    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    
    message_id = query.message.message_id-1
    chat_id = update.callback_query.from_user.id
    bot_log.delete_message(chat_id,message_id)
    query = update.callback_query
    query.answer()
    if 'Add Case' in data_text:
        keyboard = [
            [InlineKeyboardButton("Add Menu (Tambah Menu)", callback_data=str(IOMS_CAT1_CASE_A1_1))],
            [InlineKeyboardButton("Add User (Tambah User)", callback_data=str(IOMS_CAT1_CASE_A1_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_CASE_A1_3))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Cancel Case' in data_text:
        keyboard = [
            [InlineKeyboardButton("Cancel ATP (Batal ATP)", callback_data=str(IOMS_CAT1_CASE_A2_1))],
            [InlineKeyboardButton("Cancel BOQ (Batal BOQ)", callback_data=str(IOMS_CAT1_CASE_A2_2))],
            [InlineKeyboardButton("Cancel eATP (Batal eATP)", callback_data=str(IOMS_CAT1_CASE_A2_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_CASE_A2_4))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Change Case' in data_text:
        keyboard = [
            [InlineKeyboardButton("Change Approval QC (Perubahan Persetujuan QC)", callback_data=str(IOMS_CAT1_CASE_A3_1))],
            [InlineKeyboardButton("Change BOQ (Perubahan BOQ)", callback_data=str(IOMS_CAT1_CASE_A3_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_CASE_A3_3))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Document Case' in data_text:
        keyboard = [
            [InlineKeyboardButton("Document Not Appearing (Dokumen Tidak Muncul)", callback_data=str(IOMS_CAT1_CASE_A4_1))],
            [InlineKeyboardButton("Document Not Synchrone (Dokumen Tidak Sinkron)", callback_data=str(IOMS_CAT1_CASE_A4_2))],
            [InlineKeyboardButton("Document Workflow (Alur Kerja Dokumen)", callback_data=str(IOMS_CAT1_CASE_A4_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_CASE_A4_4))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Error Case' in data_text:
        keyboard = [
            [InlineKeyboardButton("Error Data (Kesalahan Data)", callback_data=str(IOMS_CAT1_CASE_A5_1))],
            [InlineKeyboardButton("Error Database (Kesalahan Database)", callback_data=str(IOMS_CAT1_CASE_A5_2))],
            [InlineKeyboardButton("Error Document (Kesalahan Dokumen)", callback_data=str(IOMS_CAT1_CASE_A5_3))],
            [InlineKeyboardButton("Error Download Data (Kesalahan Unduh Data)", callback_data=str(IOMS_CAT1_CASE_A5_4))],
            [InlineKeyboardButton("Error Export Data (Kesalahan Expor Data)", callback_data=str(IOMS_CAT1_CASE_A5_5))],
            [InlineKeyboardButton("Error Generate ATP (Kesalahan Hasilkan ATP)", callback_data=str(IOMS_CAT1_CASE_A5_6))],
            [InlineKeyboardButton("Error Generate QC (Kesalahan Hasilkan QC)", callback_data=str(IOMS_CAT1_CASE_A5_7))],
            [InlineKeyboardButton("Error Generate SQAC (Kesalahan Hasilkan SQAC)", callback_data=str(IOMS_CAT1_CASE_A5_8))],
            [InlineKeyboardButton("Error Input Data (Kesalahan Memasukan Data)", callback_data=str(IOMS_CAT1_CASE_A5_9))],
            [InlineKeyboardButton("Error Menu (Kesalahan Menu)", callback_data=str(IOMS_CAT1_CASE_A5_10))],
            [InlineKeyboardButton("Error Submit ATP (Kesalahan Kirim ATP)", callback_data=str(IOMS_CAT1_CASE_A5_11))],
            [InlineKeyboardButton("Error Submit ELV (Kesalahan Kirim ELV)", callback_data=str(IOMS_CAT1_CASE_A5_12))],
            [InlineKeyboardButton("Error Upload BOQ (Kesalahan Unggah BOQ)", callback_data=str(IOMS_CAT1_CASE_A5_13))],
            [InlineKeyboardButton("Error User (Kesalahan Pengguna)", callback_data=str(IOMS_CAT1_CASE_A5_14))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_CASE_A5_15))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Generate Case' in data_text:
        keyboard = [
            [InlineKeyboardButton("Cant Generate QC (Tidak Dapat Menghasilkan QC)", callback_data=str(IOMS_CAT1_CASE_A6_1))],
            [InlineKeyboardButton("Cant Generate ATP (Tidak Dapat Menghasilkan ATP)", callback_data=str(IOMS_CAT1_CASE_A6_2))],
            [InlineKeyboardButton("Cant Generata eOA (Tidak Dapat Menghasilkan eOA)", callback_data=str(IOMS_CAT1_CASE_A6_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_CASE_A6_4))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Requests Case' in data_text:
        keyboard = [
            [InlineKeyboardButton("Request BOQ (Permintaan BOQ)", callback_data=str(IOMS_CAT1_CASE_A7_1))],
            [InlineKeyboardButton("Request Cancel (Permintaan Pembatalan)", callback_data=str(IOMS_CAT1_CASE_A7_2))],
            [InlineKeyboardButton("Request Delete eMOM (Permintaan Hapus eNOM)", callback_data=str(IOMS_CAT1_CASE_A7_3))],
            [InlineKeyboardButton("Request Delete LV (Permintaan Hapus LV)", callback_data=str(IOMS_CAT1_CASE_A7_4))],
            [InlineKeyboardButton("Request Delete MOS (Permintaan Hapus MOS)", callback_data=str(IOMS_CAT1_CASE_A7_5))],
            [InlineKeyboardButton("Request Mapping SOWID (Permintaan Pemetaan SOWID)", callback_data=str(IOMS_CAT1_CASE_A7_6))],
            [InlineKeyboardButton("Request New Menu (Permintaan Menu Baru)", callback_data=str(IOMS_CAT1_CASE_A7_7))],
            [InlineKeyboardButton("Request Reupload ATP (Permintaan Unggah Ulang ATP)", callback_data=str(IOMS_CAT1_CASE_A7_8))],
            [InlineKeyboardButton("Request User (Permintaan Pengguna)", callback_data=str(IOMS_CAT1_CASE_A7_9))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_CASE_A7_10))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Submit & Resubmit Case' in data_text:
        keyboard = [
            [InlineKeyboardButton("Cant Submit eLV (Tidak Dapat Mengirimkan eLV)", callback_data=str(IOMS_CAT1_CASE_A8_1))],
            [InlineKeyboardButton("Cant Resubmit OA (Tidak Dapat Mengirimkan Ulang OA)", callback_data=str(IOMS_CAT1_CASE_A8_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_CASE_A8_3))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Update Case' in data_text:
        keyboard = [

            [InlineKeyboardButton("Update ATP (Perbarui ATP)", callback_data=str(IOMS_CAT1_CASE_A9_1))],
            [InlineKeyboardButton("Update Data (Perbarui DAta)", callback_data=str(IOMS_CAT1_CASE_A9_2))],
            [InlineKeyboardButton("Update Database (Perbarui Database)", callback_data=str(IOMS_CAT1_CASE_A9_3))],
            [InlineKeyboardButton("Update Menu (Perbarui Menu)", callback_data=str(IOMS_CAT1_CASE_A9_4))],
            [InlineKeyboardButton("Update NE ID (Perbarui NE ID)", callback_data=str(IOMS_CAT1_CASE_A9_5))],
            [InlineKeyboardButton("Update PO (Perbarui PO)", callback_data=str(IOMS_CAT1_CASE_A9_6))],
            [InlineKeyboardButton("Update SOW (Perbarui SOW)", callback_data=str(IOMS_CAT1_CASE_A9_7))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IOMS_CAT1_CASE_A9_8))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IOMS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def ioms_reqticket_add1(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    try:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_IOMS
    except:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_IOMS

def end_ioms(update: Update, _: CallbackContext) -> None:
    username = update.message.from_user.username
    chatid_telegram  = update.message.from_user.id 
    now = datetime.now() # current date and time
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    keterangan = update.message.text.replace(',',' ').replace(', ',' ').replace("'","").replace('"',"")
    ##Create Ticket
    characters = list(string.digits)
    length = 10
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    ticket = "IOM"+"".join(password)
    status = []
    query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data = client.command(query)
    val_check_ticket = data[3] == ticket
    status.append(val_check_ticket)
    if status[0] is False:
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001966245452', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IOMS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)

        time.sleep(2)
        query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data_select = client.command(query)
        query = f"INSERT INTO production.helpdesk_report_swfm select '{data_select[0]}','{data_select[1]}','{data_select[2]}','{data_select[3]}','{data_select[4]}','{data_select[5]}','{data_select[6]}','{data_select[7]}','{data_select[8]}','{data_select[9]}','{data_select[10]}','{data_select[11]}','{data_select[12]}','{data_select[13]}','{data_select[14]}','{data_select[15]}','{data_select[16]}','{data_select[17]}','{data_select[18]}','{data_select[19]}','{data_select[20]}','{data_select[21]}','{data_select[22]}','{data_select[23]}','{data_select[24]}','{data_select[25]}'"
        client.command(query)
        time.sleep(2)

        query = f"select ticket from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data = client.command(query)
        ticket_status = data
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS'"
        check_count = client.command(query)
        check_count = check_count == 0
        if check_count is True:
            username_expert = 'https://t.me/puang_ocha'
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        else: 
            expert = []
            query = f"select expert from production.helpdesk_expert where application_name = 'IOMS'"
            data = client.command(query)
            expert.append(data)          
            expert = str(expert).replace('[','').replace(']','').replace("'",'').split('\\n')
            expert = expert[0]
            username_expert = 'https://t.me/{}'.format(expert)
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        log_bot(update, 'IOMS')
        log_bot_success_ioms_scarlett(update, '*Tiket* ➞ Telah Membuat Tiket 🎟')
    elif status[0] is True:
        characters = list(string.digits)
        length = 10
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        ticket = "IOM"+"".join(password)

        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001966245452', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IOMS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)

        time.sleep(2)
        query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data_select = client.command(query)
        query = f"INSERT INTO production.helpdesk_report_swfm select '{data_select[0]}','{data_select[1]}','{data_select[2]}','{data_select[3]}','{data_select[4]}','{data_select[5]}','{data_select[6]}','{data_select[7]}','{data_select[8]}','{data_select[9]}','{data_select[10]}','{data_select[11]}','{data_select[12]}','{data_select[13]}','{data_select[14]}','{data_select[15]}','{data_select[16]}','{data_select[17]}','{data_select[18]}','{data_select[19]}','{data_select[20]}','{data_select[21]}','{data_select[22]}','{data_select[23]}','{data_select[24]}','{data_select[25]}'"
        client.command(query)
        time.sleep(2)

        query = f"select ticket from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data = client.command(query)
        ticket_status = data
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS'"
        check_count = client.command(query)
        check_count = check_count == 0
        if check_count is True:
            username_expert = 'https://t.me/puang_ocha'
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        else:
            expert = []
            query = f"select expert from production.helpdesk_expert where application_name = 'IOMS'"
            data = client.command(query)
            expert.append(data)          
            expert = str(expert).replace('[','').replace(']','').replace("'",'').split('\\n')
            expert = expert[0]
            username_expert = 'https://t.me/{}'.format(expert)
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        log_bot(update, 'IOMS')
        log_bot_success_ioms_scarlett(update, '*Tiket* ➞ Telah Membuat Tiket 🎟')
    return ConversationHandler.END

def ioms_expert(update: Update, _: CallbackContext) -> None: 
    try:
        keyboard = [
            [InlineKeyboardButton("Registrasi >>", callback_data=str(REG_EXPERT_IOMS))],
            [InlineKeyboardButton("Hapus >>", callback_data=str(DEL_EXPERT_IOMS))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text="Anda memilih : *Tim Ahli*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    except:
        keyboard = [
            [InlineKeyboardButton("Registrasi", callback_data=str(REG_EXPERT_IOMS))],
            [InlineKeyboardButton("Hapus", callback_data=str(DEL_EXPERT_IOMS))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Anda memilih : *Tim Ahli*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def reg_expert_ioms(update: Update, _: CallbackContext) -> None:
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS'"
    count_data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda memilih: *Registrasi*",parse_mode=telegram.ParseMode.MARKDOWN)
    if count_data == 0 or count_data == 1 or count_data == 2 or count_data == 3 or count_data == 4 or count_data == 5 or count_data == 6 or count_data == 7 or count_data == 8 or count_data == 9:
        query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 3\nKlik /cancel untuk membatalkan")
        return END_REG_EXPERT_IOMS
    elif count_data == 10:
        query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 2\nKlik /cancel untuk membatalkan")
        return END_REG_EXPERT_IOMS
    elif count_data == 11:
        query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 1\nKlik /cancel untuk membatalkan")
        return END_REG_EXPERT_IOMS
    elif count_data == 12 or count_data == 13:
        query.message.reply_text("Registrasi Tim Ahli telah mencapai maksimum\nKlik /menu")
        log_bot_success_inline_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Registrasi telah mencapai maksimum')
        return ConversationHandler.END
def end_reg_expert_ioms(update: Update, _: CallbackContext) -> None:
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS'"
    count_data = client.command(query)
    parameter_user =  update.message.text.split()
    count_user =  len(update.message.text.split())
    if count_data == 0 or count_data == 1 or count_data == 2 or count_data == 3 or count_data == 4 or count_data == 5 or count_data == 6 or count_data == 7:
        if count_user == 1:
            query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[0]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
        elif count_user == 2:
            query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[0]}'"
            client.command(query)
            query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[1]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
        elif count_user == 3:
            query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[0]}'"
            client.command(query)
            query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[1]}'"
            client.command(query)
            query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[2]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
        else:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 3\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 3')
    elif count_data == 10:
        try:
            if count_user == 1:
                query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[0]}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
                log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            elif count_user == 2:
                query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[0]}'"
                client.command(query)
                query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[1]}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
                log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            else:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 2\nKlik /menu")
                log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 2')
        except:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 2\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 2')
    elif count_data == 11:
        try:
            if count_user == 1:
                query = f"INSERT INTO production.helpdesk_expert select 'IOMS', '{parameter_user[0]}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
                log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            else:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 1\nKlik /menu")
                log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 1')
        except:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 1\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 1')
    elif count_data == 12 or count_data == 13:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("Registrasi gagal, Username ID telah mencapai maksimum 10\nKlik /menu")
        log_bot_success_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 10')
    return ConversationHandler.END

def del_expert_ioms(update: Update, _: CallbackContext) -> None:
    return_text = get_del_fm_ioms()
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda memilih: *Hapus*",parse_mode=telegram.ParseMode.MARKDOWN)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS'"
    check_status = client.command(query)
    check_status = check_status == 0
    query = update.callback_query
    query.answer()
    if check_status is True:
        query.message.reply_text("Username ID telegram tidak ditemukan\nKlik /menu", parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_ioms_scarlett(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        return ConversationHandler.END
    elif check_status is False:
        for cmdOUT in splitting(return_text):
            query.message.reply_text(cmdOUT, disable_web_page_preview=True)
        query.message.reply_text("Hapus username ID telegram dan gunakan spasi setiap user jika lebih dari satu, maksimum 3 user\nKlik /cancel untuk membatalkan")
        return END_DEL_EXPERT_IOMS
def get_del_fm_ioms():
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    text = ''
    text += 'Expert Aktif :'
    text += '\n'
    query = f"select expert from production.helpdesk_expert where application_name = 'IOMS'"
    data = client.command(query)
    data_list = str(data).split('\\n')
    data_list = str(data_list).replace("['","").replace("']","").split('\\n')
    for data in data_list:
        check_username = f"├ {data}"
        text += check_username
        text += '\n'
    text += '\n'
    return text
def end_del_expert_ioms(update: Update, _: CallbackContext) -> None:
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    parameter_user =  update.message.text.split()
    count_user =  len(update.message.text.split())
    if count_user == 1:
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS' AND expert = '{parameter_user[0]}'"
        check_status = client.command(query)
        check_status_1 = check_status == 0
        if check_status_1 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        else:
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IOMS' AND expert = '{parameter_user[0]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil dihapus\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Hapus)* ➞ Berhasil Hapus')
    elif count_user == 2:
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS' AND expert = '{parameter_user[0]}'"
        check_status = client.command(query)
        check_status_1 = check_status == 0
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS' AND expert = '{parameter_user[1]}'"
        check_status = client.command(query)
        check_status_2 = check_status == 0
        if check_status_1 is True and check_status_2 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        else:
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IOMS' AND expert = '{parameter_user[0]}'"
            client.command(query)
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IOMS' AND expert = '{parameter_user[1]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil dihapus\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Hapus)* ➞ Berhasil Hapus')
    elif count_user == 3:
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS' AND expert = '{parameter_user[0]}'"
        check_status = client.command(query)
        check_status_1 = check_status == 0
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS' AND expert = '{parameter_user[1]}'"
        check_status = client.command(query)
        check_status_2 = check_status == 0
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IOMS' AND expert = '{parameter_user[2]}'"
        check_status = client.command(query)
        check_status_3 = check_status == 0
        if check_status_1 is True and check_status_2 is True and check_status_3 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        else:
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IOMS' AND expert = '{parameter_user[0]}'"
            client.command(query)
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IOMS' AND expert = '{parameter_user[1]}'"
            client.command(query)
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IOMS' AND expert = '{parameter_user[2]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil dihapus\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Tim Ahli (Hapus)* ➞ Berhasil Hapus')
    else:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan")
        log_bot_success_ioms_scarlett(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
    return ConversationHandler.END

def ioms_myticket(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)

    query = update.callback_query
    query.answer()
    position = data == 'admin'
    if position is True: ##ADMIN
        query.edit_message_text(f"Anda memilih : *Status Laporan (Admin)*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text(text="Silahkan masukkan Nomor Tiket\nContoh : IOMXXXXXXXXXXX\nKlik /cancel untuk membatalkan",parse_mode=telegram.ParseMode.MARKDOWN)
    elif position is False: ##USER
        query.edit_message_text(f"Anda memilih : *Status Laporan*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text(text="Silahkan masukkan Nomor Tiket\nContoh : IOMXXXXXXXXXXX\nKlik /cancel untuk membatalkan",parse_mode=telegram.ParseMode.MARKDOWN)
    return IOMS_MYTICKET_PROCESS

def ioms_myticket_process(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(f"Harap menunggu dalam beberapa detik...")
    ticket_check = update.message.text
    chatid_telegram = update.message.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    print(f"INI QUERY NYA {data}")
    position = data == 'admin'
    if position is True: ##ADMIN
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
            check_status = client.command(query)
            check_status = check_status == 0
            if check_status is True:
                update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
                log_bot_success_ioms_scarlett(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
                return ConversationHandler.END
            elif check_status is False:
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select status from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                data_check = client.command(query)
                if data_check == 'closed':
                    update.message.reply_text(f"Maaf Ticket sudah closed\nKlik /menu")
                    log_bot_success_ioms_scarlett(update, '*Status Laporan* ➞ Ticket sudah di closed')
                    return ConversationHandler.END
                elif data_check == 'open':
                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
                    client.command(query)
                    query = f"INSERT INTO production.action_swfm select '{chatid_telegram}','{ticket_check}','None','None','None'"
                    client.command(query)
                    query = f"select * from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                    data = client.command(query)
                    full_name = str(data[0]).title()
                    requests = 'https://t.me/{}'.format(data[1])
                    no_hp = data[3]
                    ticket = data[11]
                    regional = str(data[13])
                    problem_note = str(data[14])
                    problem__ = str(data[15]).replace('\\n',' ')
                    app = data[17]
                    date = str(data[18]).replace('-',' ')
                    update.message.reply_text(f'Creation Date : {date}\nApplication : #{app}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                    
                    keyboard = [
                        [InlineKeyboardButton("Iya", callback_data=str(IOMS_MYTICKET_PROCESS_END))],
                        [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Pilih Iya jika benar :", reply_markup=reply_markup)
                    return IOMS_MYTICKET_CLOSED
        except:
            update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
            return ConversationHandler.END
    elif position is False: ##USER
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select count(*) as `count` from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and ticket = '{ticket_check}'"
            check_status = client.command(query)
            check_status = check_status == 0
            if check_status is True:
                update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
                log_bot_success_ioms_scarlett(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
                return ConversationHandler.END
            elif check_status is False:
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select status from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                data_check = client.command(query)
                if data_check == 'closed':
                    update.message.reply_text(f"Maaf Ticket sudah closed\nKlik /menu")
                    log_bot_success_ioms_scarlett(update, '*Status Laporan* ➞ Ticket sudah di closed')
                    return ConversationHandler.END
                elif data_check == 'open':
                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
                    client.command(query)
                    query = f"INSERT INTO production.action_swfm select '{chatid_telegram}','{ticket_check}','None','None','None'"
                    client.command(query)
                    query = f"select * from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                    data = client.command(query)
                    full_name = str(data[0]).title()
                    requests = 'https://t.me/{}'.format(data[1])
                    no_hp = data[3]
                    ticket = data[11]
                    regional = str(data[13])
                    problem_note = str(data[14])
                    problem__ = str(data[15]).replace('\\n',' ')
                    app = data[17]
                    date = str(data[18]).replace('-',' ')
                    update.message.reply_text(f'Creation Date : {date}\nApplication : #{app}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                    
                    keyboard = [
                        [InlineKeyboardButton("Iya", callback_data=str(IOMS_MYTICKET_PROCESS_END))],
                        [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Pilih Iya jika benar :", reply_markup=reply_markup)
                    return IOMS_MYTICKET_CLOSED
        except:
            update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
            log_bot_success_ioms_scarlett(update, '*Status Laporan* ➞ Tidak memiliki laporan')
            return ConversationHandler.END
def ioms_myticket_closed(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Masukkan resolution action :",parse_mode=telegram.ParseMode.MARKDOWN)
    return IOMS_MYTICKET_CLOSED_END

def ioms_myticket_closed_end(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id
    full_name_closed = update.message.from_user.full_name
    handle_by = update.message.from_user.username
    now = datetime.now()
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    parameter = update.message.text.replace(',','.')
    update.message.reply_text("Proses closed tiket ...")
    time.sleep(3)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select * from production.action_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    data_list = str(data_select).replace("[","").replace("]","").replace("'","").replace('±','').replace('+','').replace("\\\\n",' ').split('\\n')
    for data in data_list:
        data = str(data).split(', ')
        ticket_log = data[1]

    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_report_swfm update  action_handle_by = '{handle_by}', action_resolution = '{parameter}', close_ticket_date = '{date_time}', status = 'closed' WHERE ticket = '{ticket_log}'"
    client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select username_telegram,fullname_telegram from production.helpdesk_report_swfm where ticket = '{ticket_log}'"
    data = client.command(query)
    requests = 'https://t.me/{}'.format(data[0])
    full_name = str(data[1]).title()
    update.message.reply_text(f"✅ Tiket [{full_name}]({requests}) telah closed\nKlik /menu", parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select username_telegram, fullname_telegram, channel_chatid, open_ticket_date, close_ticket_date, chatid_telegram from production.helpdesk_report_swfm where ticket = '{ticket_log}'"
    check_ticket = client.command(query)
    data_list = str(check_ticket).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    x = []
    for data in data_list:
        data = str(data).split(', ')

        open_str = f'{data[3]}, {data[4]}'
        closed_str = f'{data[5]}, {data[6]}'
        full_name = data[1]
        # Parsing string menjadi objek datetime
        open_date = datetime.strptime(open_str, "%d-%B-%Y, %H:%M:%S WIB")
        closed_date = datetime.strptime(closed_str, "%d-%B-%Y, %H:%M:%S WIB")
        # Menghitung selisih waktu
        selisih_waktu = closed_date - open_date
        # Mengambil selisih dalam bentuk hari
        day_difference = selisih_waktu
        
        #grup
        bot_log.send_message(chat_id=data[2],text=f'✅ Tiket *{ticket_log}* dari [{data[1]}]({data[0]}) telah *Terclosed* oleh {full_name_closed} dengan durasi → *{day_difference}*',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        ##user
        bot_log.send_message(chat_id=data[7],text=f'✅ Tiket anda *{ticket_log}* telah *Terclosed* oleh Admin HD {full_name_closed} dengan durasi → *{day_difference}*',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        log_bot_success_ioms_scarlett(update, '*Tiket* ➞ Closed Tiket ✅')
    #HAPUS
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    return ConversationHandler.END

def ioms_broadcast(update: Update, _: CallbackContext) -> None:  
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *Broadcast Pesan*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Silahkan masukkan pesan anda",parse_mode=telegram.ParseMode.MARKDOWN)
    return IOMS_BROADCAST_END

def ioms_broadcast_end(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id
    data_text = update.message.text
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_swfm, registered_ioms, registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    check_data = client.command(query)
    check_swfm = check_data[0]
    check_ioms = check_data[1]
    check_ipas = check_data[2]
    if check_ioms == 'True':
        if os.path.exists("/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_ioms.txt"):
            os.remove("/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_ioms.txt")
            time.sleep(1)
            data_text = update.message.text.replace('_','').replace('*','')
            log_bot = open('/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_ioms.txt','a')
            log_bot.write("{}".format(data_text))
            log_bot.close()
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Terima Kasih anda telah membuat pesan siaran, sedang dalam proses pengiriman dan membutuhkan waktu sekitar 1,5 Jam, dikarenakan banyaknya user yang telah terdaftar di BOT. Terima kasih.',parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            print("The file does not exist")
            time.sleep(1)
            data_text = update.message.text.replace('_','').replace('*','')
            log_bot = open('/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_ioms.txt','a')
            log_bot.write("{}".format(data_text))
            log_bot.close()
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Terima Kasih anda telah membuat pesan siaran, sedang dalam proses pengiriman dan membutuhkan waktu sekitar 1,5 Jam, dikarenakan banyaknya user yang telah terdaftar di BOT. Terima kasih.',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_ioms_scarlett(update, '*Broadcast Pesan* ➞ Pesan Siaran')
        return ConversationHandler.END

def ioms_makeadmin(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *Jadikan Admin*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Silahkan masukkan Username Telegram",parse_mode=telegram.ParseMode.MARKDOWN)
    return IOMS_MAKEADMIN_END

def ioms_makeadmin_end(update: Update, _: CallbackContext) -> None:
    username_telegram = update.message.text
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_bot_swfm where username_telegram = '{username_telegram}' and position = 'admin'"
    check_data = client.command(query)
    check_status = check_data == 0
    if check_status is True:
        query = f"ALTER TABLE production.helpdesk_bot_swfm update position = 'admin' where username_telegram = '{username_telegram}'"
        client.command(query)
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f'Username Telegram *{username_telegram}* sukses dijadikan Admin',parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f'Username tersebut sudah menjadi Admin',parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_ioms_scarlett(update, '*Jadikan Admin* ➞ Username Telegram')
    return ConversationHandler.END

def ioms_postlink(update: Update, _: CallbackContext) -> None: 
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Anda memilih : *My Ticket List*',parse_mode=telegram.ParseMode.MARKDOWN)
    try:
        query = f"select fullname_telegram, username_telegram, ticket, problem_title, post_link from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' and category = 'IOMS' and status = 'open'"
        data = client.command(query)
        query = f"select count(*) as `count` from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and category = 'IOMS' and status = 'open'"
        count_query = client.command(query)
        query = update.callback_query
        query.answer()
        check_status = count_query == 0
        if check_status is True:
            query.message.reply_text(f'Maaf anda tidak mempunyai My Ticket List',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_ioms_scarlett(update, '*My Ticket List* ➞ My Ticket List Tidak Ditemukan')
        elif check_status is False:
            query = f"select fullname_telegram, username_telegram, ticket, problem_title, post_link from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and category = 'IOMS' and status = 'open'"
            data1 = client.command(query)
            query = update.callback_query
            query.answer()
            data_list = str(data1).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
            output_text = ''
            output_text += '*Berikut adalah My Ticket List anda*\n\n'
            output_text += '*Category - Ticket - Post Link*\n'
            for data in data_list:
                data = str(data).split(', ')
                ticket = data[2]
                problem_title = str(data[3]).split(' ➞ ')[0]
                post_link = data[4]
                output_text += f"{problem_title} - {ticket} - {post_link}\n"
            output_text += '\n'
            output_text += 'Regards\nOCHABOT & Team'
            query.message.reply_text(f'{output_text}',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_ioms_scarlett(update, '*My Ticket List* ➞ My Ticket List Ditemukan')
        return ConversationHandler.END
    except:
        query = update.callback_query
        query.answer()
        query.message.reply_text(f'Maaf anda tidak mempunyai My Ticket List',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_ioms_scarlett(update, '*My Ticket List* ➞ My Ticket List Tidak Ditemukan')
        return ConversationHandler.END

def ioms_download_excel(update: Update, _: CallbackContext) -> None: 
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Mohon menunggu dalam beberapa detik...",parse_mode=telegram.ParseMode.MARKDOWN)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select * from production.helpdesk_report_swfm hrs  where status = 'open' and category = 'IOMS'"
    data = client.command(query)
    try:
        data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
        array_data = []
        for data in data_list:
            data = str(data).split(', ')
            dub_data = {'Nama': f'{data[0]}', 'Username Telegram': f'{data[1]}', 'Chatid Telegram': f'{data[2]}', 'No HP': f'{data[3]}', 'Email': f'{data[4]}', 'Remark': f'{data[5]}', 'Position' : f'{data[9]}', 'Channel Chatid': f'{data[10]}', 'Ticket': f'{data[11]}', 'Divison': f'{data[12]}', 'Regional': f'{data[13]}', 'Problem Title': f'{data[14]}', 'Problem Summary': f'{data[15]}', 'Status': f'{data[16]}', 'Category': f'{data[17]}', 'Open Ticket Date': f'{data[18]}, {data[19]}', 'Closed Ticket Date': f'{data[20]}', 'FCAPS': f'{data[21]}', 'Action Menu': f'{data[22]}', 'Action Category': f'{data[23]}', 'Action Handle By': f'{data[24]}', 'Action Resolution': f'{data[25]}', 'Post Link': f'{data[26]}'}
            array_data.append(dub_data)
    except:
        array_data = [{'Nama': '-', 'Username Telegram': '-', 'Chatid Telegram': '-', 'No HP': '-', 'Email': '-', 'Remark': '-', 'Position' : '-', 'Channel Chatid': '-', 'Ticket': '-', 'Divison': '-', 'Regional': '-', 'Problem Title': '-', 'Problem Summary': '-', 'Status': '-', 'Category': '-', 'Open Ticket Date': '- -', 'Closed Ticket Date': '-', 'FCAPS': '-', 'Action Menu': '-', 'Action Category': '-', 'Action Handle By': '-', 'Action Resolution': '-', 'Post Link': '-'}]
    query = f"select * from production.helpdesk_report_swfm hrs  where status = 'closed' and category = 'IOMS'"
    data = client.command(query)
    data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    array_data1 = []
    for data in data_list:
        data = str(data).split(', ')
        dub_data = {'Nama': f'{data[0]}', 'Username Telegram': f'{data[1]}', 'Chatid Telegram': f'{data[2]}', 'No HP': f'{data[3]}', 'Email': f'{data[4]}', 'Remark': f'{data[5]}', 'Position' : f'{data[9]}', 'Channel Chatid': f'{data[10]}', 'Ticket': f'{data[11]}', 'Divison': f'{data[12]}', 'Regional': f'{data[13]}', 'Problem Title': f'{data[14]}', 'Problem Summary': f'{data[15]}', 'Status': f'{data[16]}', 'Category': f'{data[17]}', 'Open Ticket Date': f'{data[18]}, {data[19]}', 'Closed Ticket Date': f'{data[20]},{data[21]}', 'FCAPS': f'{data[22]}', 'Action Menu': f'{data[23]}', 'Action Category': f'{data[24]}', 'Action Handle By': f'{data[25]}', 'Action Resolution': f'{data[26]}', 'Post Link': f'{data[27]}'}
        array_data1.append(dub_data)

    df1 = pd.DataFrame(array_data)
    df2 = pd.DataFrame(array_data1)
    writer = pd.ExcelWriter('/home/dimas/baru/helpdeskbot_v2/data/data_report_open_ticket_ioms.xlsx', engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Open Ticket', index=False)
    df2.to_excel(writer, sheet_name='Closed Ticket', index=False)
    writer.save()
    print('Sukses')
    syanticbot = telegram.Bot(token_bot) #SYANTICBOT
    syanticbot.sendDocument(chat_id = chatid_telegram, document=open('/home/dimas/baru/helpdeskbot_v2/data/data_report_open_ticket_ioms.xlsx','rb'), filename="Report Ticket IOMS.xlsx",caption='Ready to download Report Ticket IOMS')
    query = update.callback_query
    query.answer()
    query.message.reply_text(text="Berikut adalah link Download Aplikasi IOMS, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_inline_ioms_scarlett(update, '*Download* ➞ Laporan Tiket Excel')
    return ConversationHandler.END

def ioms_complaint(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Anda memilih : *Eskalasi Case*',parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(f'Ketik nomor ticket anda IOMXXXXXX',parse_mode=telegram.ParseMode.MARKDOWN)
    return IOMS_COMPLAINT_END

def ioms_complaint_end(update: Update, _: CallbackContext) -> None: 
    parameter_ticket = update.message.text
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{parameter_ticket}' and category = 'IOMS'"
    check_status = client.command(query)
    check_status = check_status == 0
    if check_status is True:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f"Nomor tiket tidak sesuai kategori atau salah", parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_ioms_scarlett(update, '*Eskalasi Case* ➞ Nomor Tiket Tidak Ditemukan')
    elif check_status is False:
        query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{parameter_ticket}' and category = 'IOMS' and status = 'closed'"
        check_status = client.command(query)
        check_status = check_status == 0
        if check_status is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f"Nomor tiket telah closed", parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_ioms_scarlett(update, '*Eskalasi Case* ➞ Nomor Tiket Telah Closed')
        elif check_status is False:
            chatid_1 = '1464528446'
            chatid_2 = '1745401090'
            query = f"select ticket, post_link from production.helpdesk_report_swfm where ticket = '{parameter_ticket}'"
            data_redirect = client.command(query)
            post_link = data_redirect[1]
            bot_log.send_message(chat_id=chatid_1,text=f'Semangat Pagi Rekan...\n\nNomor Tiket  {parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_2,text=f'Semangat Pagi Rekan...\n\nNomor Tiket  {parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            log_bot_success_ioms_com(update, '*Eskalasi Case* ➞ Eskalasi Case Berhasil dengan Nomor Tiket '+parameter_ticket)
            update.message.reply_text(f"Anda berhasil membuat Eskalasi Case, Mohon ditunggu sampai Team HD merespon di room diskusi. Terima Kasih", parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END
################################################END IOMS#######################################
    
################################################MENU IPAS#######################################
def menu_ipas(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    ##access
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *IPAS*",parse_mode=telegram.ParseMode.MARKDOWN)
    if data == 'True':
        query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
        data = client.command(query)
        query = update.callback_query
        query.answer()
        position = data == 'admin'
        if position is True: ##ADMIN
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IPAS_REQTICKET))],
                [InlineKeyboardButton("Tim Ahli >>", callback_data=str(IPAS_EXPERT))],
                [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(IPAS_MYTICKET))],
                [InlineKeyboardButton("Broadcast Pesan", callback_data=str(IPAS_BROADCAST))],
                [InlineKeyboardButton("Jadikan Admin", callback_data=str(IPAS_MAKEADMIN))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(IPAS_POSTLINK))],
                [InlineKeyboardButton("Download Laporan Tiket", callback_data=str(IPAS_DOWNLOAD_EXCEL))],
                [InlineKeyboardButton("Hapus UserBot", callback_data=str(DEL_USERBOT))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(IPAS_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        elif position is False: ##USER
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IPAS_REQTICKET))],
                [InlineKeyboardButton("Status Laporan", callback_data=str(IPAS_MYTICKET))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(IPAS_POSTLINK))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(IPAS_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        return MENU
    elif data == 'False':
        query = update.callback_query
        query.answer()
        query.message.reply_text(f"Mohon registrasi Menu IPAS terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_fail_inline_ipas(update, '*Menu* ➞ Akun Belum registrasi Menu IPAS')
    return ConversationHandler.END

def menu_ipas_(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    ##access
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *IPAS*",parse_mode=telegram.ParseMode.MARKDOWN)
    if data == 'True':
        query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
        data = client.command(query)
        query = update.callback_query
        query.answer()
        position = data == 'admin'
        if position is True: ##ADMIN
            try:
                message_id = query.message.message_id-1
                chat_id = update.callback_query.from_user.id
                bot_log.delete_message(chat_id,message_id)
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IPAS_REQTICKET))],
                    [InlineKeyboardButton("Tim Ahli >>", callback_data=str(IPAS_EXPERT))],
                    [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(IPAS_MYTICKET))],
                    [InlineKeyboardButton("Broadcast Pesan", callback_data=str(IPAS_BROADCAST))],
                    [InlineKeyboardButton("Jadikan Admin", callback_data=str(IPAS_MAKEADMIN))],
                    [InlineKeyboardButton("My Ticket List", callback_data=str(IPAS_POSTLINK))],
                    [InlineKeyboardButton("Download Laporan Tiket", callback_data=str(IPAS_DOWNLOAD_EXCEL))],
                    [InlineKeyboardButton("Hapus UserBot", callback_data=str(DEL_USERBOT))],
                    [InlineKeyboardButton("Eskalasi Case", callback_data=str(IPAS_COMPLAINT))],
                    [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text("Pilih :", reply_markup=reply_markup)
            except:
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IPAS_REQTICKET))],
                    [InlineKeyboardButton("Tim Ahli >>", callback_data=str(IPAS_EXPERT))],
                    [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(IPAS_MYTICKET))],
                    [InlineKeyboardButton("Broadcast Pesan", callback_data=str(IPAS_BROADCAST))],
                    [InlineKeyboardButton("Jadikan Admin", callback_data=str(IPAS_MAKEADMIN))],
                    [InlineKeyboardButton("My Ticket List", callback_data=str(IPAS_POSTLINK))],
                    [InlineKeyboardButton("Download Laporan Tiket", callback_data=str(IPAS_DOWNLOAD_EXCEL))],
                    [InlineKeyboardButton("Hapus UserBot", callback_data=str(DEL_USERBOT))],
                    [InlineKeyboardButton("Eskalasi Case", callback_data=str(IPAS_COMPLAINT))],
                    [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text("Pilih :", reply_markup=reply_markup)
        elif position is False: ##USER
            try:
                message_id = query.message.message_id-1
                chat_id = update.callback_query.from_user.id
                bot_log.delete_message(chat_id,message_id)
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IPAS_REQTICKET))],
                    [InlineKeyboardButton("Status Laporan", callback_data=str(IPAS_MYTICKET))],
                    [InlineKeyboardButton("My Ticket List", callback_data=str(IPAS_POSTLINK))],
                    [InlineKeyboardButton("Eskalasi Case", callback_data=str(IPAS_COMPLAINT))],
                    [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text("Pilih :", reply_markup=reply_markup)
            except:
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(IPAS_REQTICKET))],
                    [InlineKeyboardButton("Status Laporan", callback_data=str(IPAS_MYTICKET))],
                    [InlineKeyboardButton("My Ticket List", callback_data=str(IPAS_POSTLINK))],
                    [InlineKeyboardButton("Eskalasi Case", callback_data=str(IPAS_COMPLAINT))],
                    [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text("Pilih :", reply_markup=reply_markup)
        return MENU
    elif data == 'False':
        query = update.callback_query
        query.answer()
        query.message.reply_text(f"Mohon registrasi Menu IPAS terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_fail_inline_ipas(update, '*Menu* ➞ Akun Belum registrasi Menu IPAS')
    return ConversationHandler.END

def ipas_reqticket(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    try:
        keyboard = [
            [InlineKeyboardButton("Aplication Error >>", callback_data=str(IPAS_CAT7))],
            [InlineKeyboardButton("Transport >>", callback_data=str(IPAS_CAT1))],
            [InlineKeyboardButton("Power >>", callback_data=str(IPAS_CAT2))],
            [InlineKeyboardButton("ISR >>", callback_data=str(IPAS_CAT3))],
            [InlineKeyboardButton("Tower Milik >>", callback_data=str(IPAS_CAT4))],
            [InlineKeyboardButton("Tower Sewa >>", callback_data=str(IPAS_CAT5))],
            [InlineKeyboardButton("TANYA PROSES ?", callback_data=str(IPAS_CAT6))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_IPAS_))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id-1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Penjelasan Kategori: \n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*Transport :* Dashboard, Manage Data, Order Telkom, Ordering, QC/BA\n*Power :* Dashboard, Power Management\n*ISR :* FPJP, ISR Ordering\n*Tower Milik  :* Dashboard Milik, List Submission Legalitas, Site List Pengajuan\n*Tower Sewa :* Contract Tower Sewa, Denda, Recurring\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    except:
        keyboard = [
            [InlineKeyboardButton("Aplication Error >>", callback_data=str(IPAS_CAT7))],
            [InlineKeyboardButton("Transport >>", callback_data=str(IPAS_CAT1))],
            [InlineKeyboardButton("Power >>", callback_data=str(IPAS_CAT2))],
            [InlineKeyboardButton("ISR >>", callback_data=str(IPAS_CAT3))],
            [InlineKeyboardButton("Tower Milik >>", callback_data=str(IPAS_CAT4))],
            [InlineKeyboardButton("Tower Sewa >>", callback_data=str(IPAS_CAT5))],
            [InlineKeyboardButton("TANYA PROSES ?", callback_data=str(IPAS_CAT6))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_IPAS_))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        
        query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Penjelasan Kategori: \n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*Transport :* Dashboard, Manage Data, Order Telkom, Ordering, QC/BA\n*Power :* Dashboard, Power Management\n*ISR :* FPJP, ISR Ordering\n*Tower Milik  :* Dashboard Milik, List Submission Legalitas, Site List Pengajuan\n*Tower Sewa :* Contract Tower Sewa, Denda, Recurring\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def ipas_reqticket_add(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    message_id = query.message.message_id-1
    chat_id = update.callback_query.from_user.id
    bot_log.delete_message(chat_id,message_id)
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'Transport' in data_text:
        keyboard = [
            [InlineKeyboardButton("Dashboard (Dasbor)", callback_data=str(IPAS_CAT1_1))],
            [InlineKeyboardButton("Manage Data (Kelola Data)", callback_data=str(IPAS_CAT1_2))],
            [InlineKeyboardButton("Order Telkom (Pesan Telkom)", callback_data=str(IPAS_CAT1_3))],
            [InlineKeyboardButton("Ordering (Ordering)", callback_data=str(IPAS_CAT1_4))],
            [InlineKeyboardButton("QC/BA (QC/BA)", callback_data=str(IPAS_CAT1_5))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_CAT1_6))],
            [InlineKeyboardButton("Kembali", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Penjelasan Kategori: \n*Dashoard :* All, Dashboard, Login\n*Manage Data :* Manage Program, Manage Site ID, Manage Site ID Whitelist\n*Order Telkom :* Approval Surat, List Surat Telkom, New Surat Telkom, Surat Return\n*Ordering :* Approve Order, List Request, New Request, Order Draft, Order on Going, Request Reject\n*QC/BA :* BAUT, BAUT Approval, BAUT Approved, QC Approval\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Aplication Error' in data_text:
        keyboard = [
            [InlineKeyboardButton("Loading after Login (Loading Setelah Login)", callback_data=str(IPAS_CAT7_1))],
            [InlineKeyboardButton("Log out Yourself (Logout Sendiri)", callback_data=str(IPAS_CAT7_2))],
            [InlineKeyboardButton("Hang (Gantung)", callback_data=str(IPAS_CAT7_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_CAT7_4))],
            [InlineKeyboardButton("Kembali ke Menu", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Power' in data_text:
        keyboard = [
            [InlineKeyboardButton("Dashboard (Dasbor)", callback_data=str(IPAS_CAT2_1))],
            [InlineKeyboardButton("Power Management (Manajemen daya)", callback_data=str(IPAS_CAT2_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_CAT2_3))],
            [InlineKeyboardButton("Kembali", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Penjelasan Kategori: \n*Dashboard :* Order Request, Payment & Inquiry Difference\n*Power Management :* ID Pelanggan PLN, Inquiry Request, PLN Ordering, Site list, Tagihan PLN\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'ISR' in data_text:
        keyboard = [
            [InlineKeyboardButton("FPJP (FPJP)", callback_data=str(IPAS_CAT3_1))],
            [InlineKeyboardButton("ISR Ordering (ISR Ordering)", callback_data=str(IPAS_CAT3_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_CAT3_3))],
            [InlineKeyboardButton("Kembali", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Penjelasan Kategori: \n*FPJP :* Create FPJP\n*ISR Ordering :* ISR Data List, List Order, List Order Failed To Kominfo, List Order Need Approval, List Order On Process, New Request Order, Summary Links\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Tower Milik' in data_text:
        keyboard = [
            [InlineKeyboardButton("Dashboard Milik (Dasbor Milik)", callback_data=str(IPAS_CAT4_1))],
            [InlineKeyboardButton("List of Legality of Submission (Daftar Legalitas Pengajuan)", callback_data=str(IPAS_CAT4_2))],
            [InlineKeyboardButton("List of Submission Sites (Daftar Situs Pengiriman)", callback_data=str(IPAS_CAT4_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_CAT4_4))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Penjelasan Kategori: \n*Dashboard Milik :* -\n*List of Legality of Submission :* -\n*List of Submission Sites :* -\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Tower Sewa' in data_text:
        keyboard = [
            [InlineKeyboardButton("Tower Rental Contract (Kontrak Sewa Menara)", callback_data=str(IPAS_CAT5_1))],
            [InlineKeyboardButton("Denda (Denda)", callback_data=str(IPAS_CAT5_2))],
            [InlineKeyboardButton("Recurring (Berulang)", callback_data=str(IPAS_CAT5_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_CAT5_4))],
            [InlineKeyboardButton("Kembali", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Penjelasan Kategori: \n*Tower Rental Contract :* Bill Confirmation, Contract Library, Billing Data, First Contract, Main Account Management, Recontract, Site Baseline, Sub Account Management, Submit BAPS (BCL)\n*Denda :* Billing Data, Submit BAPS (BCL)\n*Recurring :* Approve BAPS, Billing Data, First Contract, Recontract, Submit BAPS (BCL), Update PO\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'TANYA PROSES ?' in data_text:
        keyboard = [
            [InlineKeyboardButton("Transport", callback_data=str(IPAS_CAT6_1))],
            [InlineKeyboardButton("Power", callback_data=str(IPAS_CAT6_2))],
            [InlineKeyboardButton("ISR", callback_data=str(IPAS_CAT6_3))],
            [InlineKeyboardButton("Tower Milik", callback_data=str(IPAS_CAT6_4))],
            [InlineKeyboardButton("Tower Sewa", callback_data=str(IPAS_CAT6_5))],
            [InlineKeyboardButton("Kembali", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def ipas_reqticket_cat1(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    chat_id = update.callback_query.message.chat_id
    message_id_1 = update.callback_query.message.message_id-1
    bot_log.delete_message(chat_id,message_id_1)
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'Dashboard' in data_text:
        keyboard = [
            [InlineKeyboardButton("All (Semua)", callback_data=str(IPAS_TICKET_CAT1_1))],
            [InlineKeyboardButton("Dasboard (Dasbor)", callback_data=str(IPAS_TICKET_CAT1_2))],
            [InlineKeyboardButton("Login (Gabung)", callback_data=str(IPAS_TICKET_CAT1_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT1_4))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Manage Data' in data_text:
        keyboard = [
            [InlineKeyboardButton("Manage Program (Kelola Program)", callback_data=str(IPAS_TICKET_CAT1_5))],
            [InlineKeyboardButton("Manage Site ID (Kelola Site ID)", callback_data=str(IPAS_TICKET_CAT1_6))],
            [InlineKeyboardButton("Manage Site ID Whitelist (Kelola Daftar Putih ID Situs)", callback_data=str(IOMS_CAT1_1))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT1_7))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Order Telkom' in data_text:
        keyboard = [
            [InlineKeyboardButton("Approval Letter (Surat persetujuan)", callback_data=str(IPAS_TICKET_CAT1_8))],
            [InlineKeyboardButton("Telkom Mail List (Daftar Surat Telkom)", callback_data=str(IPAS_TICKET_CAT1_9))],
            [InlineKeyboardButton("Approval Letter (Surat persetujuan", callback_data=str(IPAS_TICKET_CAT1_10))],
            [InlineKeyboardButton("New Telkom Letter (Surat Telkom Baru)", callback_data=str(IPAS_TICKET_CAT1_11))],
            [InlineKeyboardButton("Return Letter (Surat Pengembalian)", callback_data=str(IPAS_TICKET_CAT1_12))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT1_13))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Ordering' in data_text:
        keyboard = [
            [InlineKeyboardButton("Approve Order (Setujui Pesanan)", callback_data=str(IPAS_TICKET_CAT1_14))],
            [InlineKeyboardButton("List Request (Daftar Permintaan)", callback_data=str(IPAS_TICKET_CAT1_15))],
            [InlineKeyboardButton("New Request (Permintaan Baru)", callback_data=str(IPAS_TICKET_CAT1_16))],
            [InlineKeyboardButton("Order Draft (Draf Pesanan)", callback_data=str(IPAS_TICKET_CAT1_17))],
            [InlineKeyboardButton("Order on Going (Pesan Sedang Berlangsung)", callback_data=str(IPAS_TICKET_CAT1_18))],
            [InlineKeyboardButton("Request Reject(Permintaan ditolak)", callback_data=str(IPAS_TICKET_CAT1_19))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT1_20))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'QC/BA' in data_text:
        keyboard = [
            [InlineKeyboardButton("BAUT (BAUT)", callback_data=str(IPAS_TICKET_CAT1_21))],
            [InlineKeyboardButton("BAUT Approval (Persetujuan BAUT)", callback_data=str(IPAS_TICKET_CAT1_22))],
            [InlineKeyboardButton("BAUT Approved (BAUT Disetujui)", callback_data=str(IPAS_TICKET_CAT1_23))],
            [InlineKeyboardButton("QC Approval (Persetujuan QC)", callback_data=str(IPAS_TICKET_CAT1_24))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT1_25))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Other Problems' in data_text:
        keyboard = [
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT1_26))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
def ipas_reqticket_cat2(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    chat_id = update.callback_query.message.chat_id
    message_id_1 = update.callback_query.message.message_id-1
    bot_log.delete_message(chat_id,message_id_1)
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'Dashboard' in data_text:
        keyboard = [
            [InlineKeyboardButton("Order Request (Permintaan pesanan)", callback_data=str(IPAS_TICKET_CAT2_1))],
            [InlineKeyboardButton("Payment & Inquiry Difference (Perbedaan Pembayaran & Permintaan)", callback_data=str(IPAS_TICKET_CAT2_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT2_3))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Power Management' in data_text:
        keyboard = [
            [InlineKeyboardButton("PLN Customer ID (ID Pelanggan PLN)", callback_data=str(IPAS_TICKET_CAT2_4))],
            [InlineKeyboardButton("Inquiry Request (Permintaan)", callback_data=str(IPAS_TICKET_CAT2_5))],
            [InlineKeyboardButton("PLN Ordering (Pemesanan PLN)", callback_data=str(IPAS_TICKET_CAT2_6))],
            [InlineKeyboardButton("Site List (Daftar Situs)", callback_data=str(IPAS_TICKET_CAT2_7))],
            [InlineKeyboardButton("PPLN Bill (Tagihan PLN)", callback_data=str(IPAS_TICKET_CAT2_8))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT2_9))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Other Problems' in data_text:
        keyboard = [
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT2_10))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
def ipas_reqticket_cat3(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    chat_id = update.callback_query.message.chat_id
    message_id_1 = update.callback_query.message.message_id-1
    bot_log.delete_message(chat_id,message_id_1)
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'FPJP' in data_text:
        keyboard = [
            [InlineKeyboardButton("Create FPJP (Buat FPJP", callback_data=str(IPAS_TICKET_CAT3_1))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT3_2))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'ISR Ordering' in data_text:
        keyboard = [
            [InlineKeyboardButton("ISR Data List (Daftar Data ISR)", callback_data=str(IPAS_TICKET_CAT3_3))],
            [InlineKeyboardButton("Order List (Daftar Pesanan)", callback_data=str(IPAS_TICKET_CAT3_4))],
            [InlineKeyboardButton("List of Failed Orders to Kominfo (Daftar Pesanan Gagal ke Kominfo)", callback_data=str(IPAS_TICKET_CAT3_5))],
            [InlineKeyboardButton("Order List Requires Approval (Daftar Pesanan Membutuhkan Persetujuan)", callback_data=str(IPAS_TICKET_CAT3_6))],
            [InlineKeyboardButton("List of Orders in Process (Daftar Pesanan Sedang Diproses)", callback_data=str(IPAS_TICKET_CAT3_7))],
            [InlineKeyboardButton("New Request Order (Pesanan Permintaan Baru)", callback_data=str(IPAS_TICKET_CAT3_8))],
            [InlineKeyboardButton("Summary Links (Tautan Ringkasan)", callback_data=str(IPAS_TICKET_CAT3_9))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT3_10))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Other Problems' in data_text:
        keyboard = [
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT3_11))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def ipas_reqticket_cat4(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    message_id = query.message.message_id-1
    chat_id = update.callback_query.from_user.id
    bot_log.delete_message(chat_id,message_id)
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'Dashboard Milik' in data_text:
        keyboard = [
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT4_1))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'List of Legality of Submission' in data_text:
        keyboard = [
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT4_2))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'List of Submission Sites' in data_text:
        keyboard = [
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT4_3))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)    
    elif 'Other Problems' in data_text:
        keyboard = [
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT4_4))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def ipas_reqticket_cat5(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    message_id = query.message.message_id-1
    chat_id = update.callback_query.from_user.id
    bot_log.delete_message(chat_id,message_id)
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)

    if 'Tower Rental Contract' in data_text:
        keyboard = [
            [InlineKeyboardButton("Bill Confirmation (Konfirmasi Tagihan)", callback_data=str(IPAS_TICKET_CAT5_1))],
            [InlineKeyboardButton("Contract Library (Perpustakaan Kontrak)", callback_data=str(IPAS_TICKET_CAT5_2))],
            [InlineKeyboardButton("Billing Data (Data Penagihan)", callback_data=str(IPAS_TICKET_CAT5_3))],
            [InlineKeyboardButton("First Contract (Kontrak Pertama)", callback_data=str(IPAS_TICKET_CAT5_4))],
            [InlineKeyboardButton("Main Account Management (Manajemen Akun Utama)", callback_data=str(IPAS_TICKET_CAT5_5))],
            [InlineKeyboardButton("Recontract (Kontrak ulang)", callback_data=str(IPAS_TICKET_CAT5_6))],
            [InlineKeyboardButton("Site Baseline (Dasar Situs)", callback_data=str(IPAS_TICKET_CAT5_7))],
            [InlineKeyboardButton("Sub Account Management (Manajemen Sub Akun)", callback_data=str(IPAS_TICKET_CAT5_8))],
            [InlineKeyboardButton("Submit BAPS BCL (Menyerahkan BAPS BCL)", callback_data=str(IPAS_TICKET_CAT5_9))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT5_10))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Denda' in data_text:
        keyboard = [
            [InlineKeyboardButton("Billing Data (Data Penagihan)", callback_data=str(IPAS_TICKET_CAT5_11))],
            [InlineKeyboardButton("Submit BAPS BCL (Menyerahkan BAPS BCL)", callback_data=str(IPAS_TICKET_CAT5_12))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT5_13))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Recurring' in data_text:
        keyboard = [
            [InlineKeyboardButton("Approve BAPS (Menyetujui BAPS)", callback_data=str(IPAS_TICKET_CAT5_14))],
            [InlineKeyboardButton("Billing Data (Data Penagihan)", callback_data=str(IPAS_TICKET_CAT5_15))],
            [InlineKeyboardButton("First Contract (Kontrak Pertama)", callback_data=str(IPAS_TICKET_CAT5_16))],
            [InlineKeyboardButton("Submit BAPS BCL (Menyerahkan BAPS BCL)", callback_data=str(IPAS_TICKET_CAT5_17))],
            [InlineKeyboardButton("Update PO (Perbarui PO)", callback_data=str(IPAS_TICKET_CAT5_18))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT5_19))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)    
    elif 'Other Problems' in data_text:
        keyboard = [
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(IPAS_TICKET_CAT5_20))],
            [InlineKeyboardButton("Kembali ke Menu Kendala", callback_data=str(IPAS_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def ioms_reqticket_all(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    try:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_IPAS
    except:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_IPAS

def end_ipas(update: Update, _: CallbackContext) -> None:
    username = update.message.from_user.username
    chatid_telegram  = update.message.from_user.id 
    now = datetime.now() # current date and time
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    keterangan = update.message.text.replace(',',' ').replace(', ',' ').replace("'","").replace('"',"")
    ##Create Ticket
    characters = list(string.digits)
    length = 10
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    ticket = "IPS"+"".join(password)
    status = []
    query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data = client.command(query)
    val_check_ticket = data[3] == ticket
    problem_title = str(data[14]).split(' ➞ ')[0]
    status.append(val_check_ticket)
    if status[0] is False:
        data_select = problem_title
        if data_select == 'Transport':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002018867641', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Power':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002097556919', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'ISR':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002037557926', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Tower Milik':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002089555423', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Tower Sewa':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002111205004', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'TANYA PROSES ?':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002112107552', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Aplication Error':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002177304143', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)

        time.sleep(2)
        query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data_select = client.command(query)
        query = f"INSERT INTO production.helpdesk_report_swfm select '{data_select[0]}','{data_select[1]}','{data_select[2]}','{data_select[3]}','{data_select[4]}','{data_select[5]}','{data_select[6]}','{data_select[7]}','{data_select[8]}','{data_select[9]}','{data_select[10]}','{data_select[11]}','{data_select[12]}','{data_select[13]}','{data_select[14]}','{data_select[15]}','{data_select[16]}','{data_select[17]}','{data_select[18]}','{data_select[19]}','{data_select[20]}','{data_select[21]}','{data_select[22]}','{data_select[23]}','{data_select[24]}','{data_select[25]}'"
        client.command(query)
        time.sleep(2)

        query = f"select ticket from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data = client.command(query)
        ticket_status = data
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS'"
        check_count = client.command(query)
        check_count = check_count == 0
        if check_count is True:
            username_expert = 'https://t.me/puang_ocha'
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
            data_select = client.command(query)
            data_select = str(data_select).split(' ➞ ')[0]
            if data_select == 'Transport':
                telegram_channel = "https://t.me/+sQG0LJKafCYyZDI1"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Power':
                telegram_channel = "https://t.me/+Jh6ZiNaVhNUxZTBl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'ISR':
                telegram_channel = "https://t.me/+rXx0w1EvlMtmOWVl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Tower Milik':
                telegram_channel = "https://t.me/+tE9z9rmJ12IzMTM9"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Tower Sewa':
                telegram_channel = "https://t.me/+7sKZou361pE1MDBl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'TANYA PROSES ?':
                telegram_channel = "https://t.me/+ezJTmDsfnGZiN2E9"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Aplication Error':
                telegram_channel = "https://t.me/+Gr7loeS7JWZkYjI1"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        else:
            expert = []
            query = f"select expert from production.helpdesk_expert where application_name = 'IPAS'"
            data = client.command(query)
            expert.append(data)          
            expert = str(expert).replace('[','').replace(']','').replace("'",'').split('\\n')
            expert = expert[0]
            username_expert = 'https://t.me/{}'.format(expert)
            query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
            data_select = client.command(query)
            data_select = str(data_select).split(' ➞ ')[0]
            if data_select == 'Transport':
                telegram_channel = "https://t.me/+sQG0LJKafCYyZDI1"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Power':
                telegram_channel = "https://t.me/+Jh6ZiNaVhNUxZTBl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'ISR':
                telegram_channel = "https://t.me/+rXx0w1EvlMtmOWVl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Tower Milik':
                telegram_channel = "https://t.me/+tE9z9rmJ12IzMTM9"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Tower Sewa':
                telegram_channel = "https://t.me/+7sKZou361pE1MDBl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'TANYA PROSES ?':
                telegram_channel = "https://t.me/+ezJTmDsfnGZiN2E9"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Aplication Error':
                telegram_channel = "https://t.me/+Gr7loeS7JWZkYjI1"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        log_bot(update, 'IPAS')
        log_bot_success_ipas(update, '*Tiket* ➞ Telah Membuat Tiket 🎟')
    elif status[0] is True:
        characters = list(string.digits)
        length = 10
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        ticket = "IPS"+"".join(password)

        data_select = problem_title
        if data_select == 'Transport':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002018867641', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Power':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002097556919', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'ISR':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002037557926', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Tower Milik':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002089555423', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Tower Sewa':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002111205004', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'TANYA PROSES ?':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002112107552', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Aplication Error':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002177304143', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'IPAS', status = 'open', fcaps = 'ADMINSTRATION' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)

        time.sleep(2)
        query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data_select = client.command(query)
        query = f"INSERT INTO production.helpdesk_report_swfm select '{data_select[0]}','{data_select[1]}','{data_select[2]}','{data_select[3]}','{data_select[4]}','{data_select[5]}','{data_select[6]}','{data_select[7]}','{data_select[8]}','{data_select[9]}','{data_select[10]}','{data_select[11]}','{data_select[12]}','{data_select[13]}','{data_select[14]}','{data_select[15]}','{data_select[16]}','{data_select[17]}','{data_select[18]}','{data_select[19]}','{data_select[20]}','{data_select[21]}','{data_select[22]}','{data_select[23]}','{data_select[24]}','{data_select[25]}'"
        client.command(query)
        time.sleep(2)

        query = f"select ticket from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data = client.command(query)
        ticket_status = data
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS'"
        check_count = client.command(query)
        check_count = check_count == 0
        if check_count is True:
            username_expert = 'https://t.me/puang_ocha'
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
            data_select = client.command(query)
            data_select = str(data_select).split(' ➞ ')[0]
            if data_select == 'Transport':
                telegram_channel = "https://t.me/+sQG0LJKafCYyZDI1"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Power':
                telegram_channel = "https://t.me/+Jh6ZiNaVhNUxZTBl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'ISR':
                telegram_channel = "https://t.me/+rXx0w1EvlMtmOWVl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Tower Milik':
                telegram_channel = "https://t.me/+tE9z9rmJ12IzMTM9"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Tower Sewa':
                telegram_channel = "https://t.me/+7sKZou361pE1MDBl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'TANYA PROSES ?':
                telegram_channel = "https://t.me/+ezJTmDsfnGZiN2E9"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Aplication Error':
                telegram_channel = "https://t.me/+Gr7loeS7JWZkYjI1"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        else:
            expert = []
            query = f"select expert from production.helpdesk_expert where application_name = 'IPAS'"
            data = client.command(query)
            expert.append(data)          
            expert = str(expert).replace('[','').replace(']','').replace("'",'').split('\\n')
            expert = expert[0]
            username_expert = 'https://t.me/{}'.format(expert)
            query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
            data_select = client.command(query)
            data_select = str(data_select).split(' ➞ ')[0]
            if data_select == 'Transport':
                telegram_channel = "https://t.me/+sQG0LJKafCYyZDI1"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Power':
                telegram_channel = "https://t.me/+Jh6ZiNaVhNUxZTBl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'ISR':
                telegram_channel = "https://t.me/+rXx0w1EvlMtmOWVl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Tower Milik':
                telegram_channel = "https://t.me/+tE9z9rmJ12IzMTM9"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Tower Sewa':
                telegram_channel = "https://t.me/+7sKZou361pE1MDBl"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'TANYA PROSES ?':
                telegram_channel = "https://t.me/+ezJTmDsfnGZiN2E9"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : {}".format(expert) , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            elif data_select == 'Aplication Error':
                telegram_channel = "https://t.me/+Gr7loeS7JWZkYjI1"
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
                buttons = [[button1]]
                keyboard = InlineKeyboardMarkup(buttons)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        log_bot(update, 'IPAS')
        log_bot_success_ipas(update, '*Tiket* ➞ Telah Membuat Tiket 🎟')
    return ConversationHandler.END

def ipas_expert(update: Update, _: CallbackContext) -> None:
    try:
        keyboard = [
            [InlineKeyboardButton("Registrasi >>", callback_data=str(REG_EXPERT_IPAS))],
            [InlineKeyboardButton("Hapus >>", callback_data=str(DEL_EXPERT_IPAS))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text="Anda memilih : *Tim Ahli*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    except:
        keyboard = [
            [InlineKeyboardButton("Registrasi", callback_data=str(REG_EXPERT_IPAS))],
            [InlineKeyboardButton("Hapus", callback_data=str(DEL_EXPERT_IPAS))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Anda memilih : *Tim Ahli*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)


def reg_expert_ipas(update: Update, _: CallbackContext) -> None:
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS'"
    count_data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda memilih: *Registrasi*",parse_mode=telegram.ParseMode.MARKDOWN)
    if count_data == 0 or count_data == 1 or count_data == 2 or count_data == 3 or count_data == 4 or count_data == 5 or count_data == 6 or count_data == 7 or count_data == 8 or count_data == 9:
        query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 3\nKlik /cancel untuk membatalkan")
        return END_REG_EXPERT_IPAS
    elif count_data == 10:
        query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 2\nKlik /cancel untuk membatalkan")
        return END_REG_EXPERT_IPAS
    elif count_data == 11:
        query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 1\nKlik /cancel untuk membatalkan")
        return END_REG_EXPERT_IPAS
    elif count_data == 12 or count_data == 13:
        query.message.reply_text("Registrasi Tim Ahli telah mencapai maksimum\nKlik /menu")
        log_bot_success_inline_ioms_scarlett(update, '*Tim Ahli (Registrasi)* ➞ Registrasi telah mencapai maksimum')
        return ConversationHandler.END
def end_reg_expert_ipas(update: Update, _: CallbackContext) -> None:
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS'"
    count_data = client.command(query)
    parameter_user =  update.message.text.split()
    count_user =  len(update.message.text.split())
    if count_data == 0 or count_data == 1 or count_data == 2 or count_data == 3 or count_data == 4 or count_data == 5 or count_data == 6 or count_data == 7:
        if count_user == 1:
            query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[0]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
        elif count_user == 2:
            query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[0]}'"
            client.command(query)
            query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[1]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
        elif count_user == 3:
            query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[0]}'"
            client.command(query)
            query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[1]}'"
            client.command(query)
            query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[2]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
        else:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 3\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 3')
    elif count_data == 10:
        try:
            if count_user == 1:
                query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[0]}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
                log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            elif count_user == 2:
                query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[0]}'"
                client.command(query)
                query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[1]}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
                log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            else:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 2\nKlik /menu")
                log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 2')
        except:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 2\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 2')
    elif count_data == 11:
        try:
            if count_user == 1:
                query = f"INSERT INTO production.helpdesk_expert select 'IPAS', '{parameter_user[0]}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
                log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            else:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 1\nKlik /menu")
                log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 1')
        except:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 1\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 1')
    elif count_data == 12 or count_data == 13:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("Registrasi gagal, Username ID telah mencapai maksimum 10\nKlik /menu")
        log_bot_success_ipas(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 10')
    return ConversationHandler.END

def del_expert_ipas(update: Update, _: CallbackContext) -> None:
    return_text = get_del_fm_ipas()
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda memilih: *Hapus*",parse_mode=telegram.ParseMode.MARKDOWN)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS'"
    check_status = client.command(query)
    check_status = check_status == 0
    query = update.callback_query
    query.answer()
    if check_status is True:
        query.message.reply_text("Username ID telegram tidak ditemukan\nKlik /menu", parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_ipas(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        return ConversationHandler.END
    elif check_status is False:
        for cmdOUT in splitting(return_text):
            query.message.reply_text(cmdOUT, disable_web_page_preview=True)
        query.message.reply_text("Hapus username ID telegram dan gunakan spasi setiap user jika lebih dari satu, maksimum 3 user\nKlik /cancel untuk membatalkan")
        return END_DEL_EXPERT_IPAS
def get_del_fm_ipas():
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    text = ''
    text += 'Expert Aktif :'
    text += '\n'
    query = f"select expert from production.helpdesk_expert where application_name = 'IPAS'"
    data = client.command(query)
    data_list = str(data).split('\\n')
    data_list = str(data_list).replace("['","").replace("']","").split('\\n')
    for data in data_list:
        check_username = f"├ {data}"
        text += check_username
        text += '\n'
    text += '\n'
    return text
def end_del_expert_ipas(update: Update, _: CallbackContext) -> None:
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    parameter_user =  update.message.text.split()
    count_user =  len(update.message.text.split())
    if count_user == 1:
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS' AND expert = '{parameter_user[0]}'"
        check_status = client.command(query)
        check_status_1 = check_status == 0
        if check_status_1 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        else:
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IPAS' AND expert = '{parameter_user[0]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil dihapus\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Hapus)* ➞ Berhasil Hapus')
    elif count_user == 2:
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS' AND expert = '{parameter_user[0]}'"
        check_status = client.command(query)
        check_status_1 = check_status == 0
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS' AND expert = '{parameter_user[1]}'"
        check_status = client.command(query)
        check_status_2 = check_status == 0
        if check_status_1 is True and check_status_2 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        else:
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IPAS' AND expert = '{parameter_user[0]}'"
            client.command(query)
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IPAS' AND expert = '{parameter_user[1]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil dihapus\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Hapus)* ➞ Berhasil Hapus')
    elif count_user == 3:
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS' AND expert = '{parameter_user[0]}'"
        check_status = client.command(query)
        check_status_1 = check_status == 0
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS' AND expert = '{parameter_user[1]}'"
        check_status = client.command(query)
        check_status_2 = check_status == 0
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'IPAS' AND expert = '{parameter_user[2]}'"
        check_status = client.command(query)
        check_status_3 = check_status == 0
        if check_status_1 is True and check_status_2 is True and check_status_3 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        else:
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IPAS' AND expert = '{parameter_user[0]}'"
            client.command(query)
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IPAS' AND expert = '{parameter_user[1]}'"
            client.command(query)
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'IPAS' AND expert = '{parameter_user[2]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil dihapus\nKlik /menu")
            log_bot_success_ipas(update, '*Tim Ahli (Hapus)* ➞ Berhasil Hapus')
    else:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan")
        log_bot_success_ipas(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
    return ConversationHandler.END

def ipas_myticket(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)

    query = update.callback_query
    query.answer()
    position = data == 'admin'
    if position is True: ##ADMIN
        query.edit_message_text(f"Anda memilih : *Status Laporan (Admin)*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text(text="Silahkan masukkan Nomor Tiket\nContoh : IPSXXXXXXXXXXX\nKlik /cancel untuk membatalkan",parse_mode=telegram.ParseMode.MARKDOWN)
    elif position is False: ##USER
        query.edit_message_text(f"Anda memilih : *Status Laporan*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text(text="Silahkan masukkan Nomor Tiket\nContoh : IPSXXXXXXXXXXX\nKlik /cancel untuk membatalkan",parse_mode=telegram.ParseMode.MARKDOWN)
    return IPAS_MYTICKET_PROCESS

def ipas_myticket_process(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(f"Harap menunggu dalam beberapa detik...")
    ticket_check = update.message.text
    chatid_telegram = update.message.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    position = data == 'admin'
    if position is True: ##ADMIN
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
            check_status = client.command(query)
            check_status = check_status == 0
            if check_status is True:
                update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
                log_bot_success_ipas(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
                return ConversationHandler.END
            elif check_status is False:
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select status from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                data_check = client.command(query)
                if data_check == 'closed':
                    update.message.reply_text(f"Maaf Ticket sudah closed\nKlik /menu")
                    log_bot_success_ipas(update, '*Status Laporan* ➞ Ticket sudah di closed')
                    return ConversationHandler.END
                elif data_check == 'open':
                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
                    client.command(query)
                    query = f"INSERT INTO production.action_swfm select '{chatid_telegram}','{ticket_check}','None','None','None'"
                    client.command(query)
                    query = f"select * from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                    data = client.command(query)
                    full_name = str(data[0]).title()
                    requests = 'https://t.me/{}'.format(data[1])
                    no_hp = data[3]
                    ticket = data[11]
                    regional = str(data[13])
                    problem_note = str(data[14])
                    problem__ = str(data[15]).replace('\\n',' ')
                    app = data[17]
                    date = str(data[18]).replace('-',' ')
                    update.message.reply_text(f'Creation Date : {date}\nApplication : #{app}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                    
                    keyboard = [
                        [InlineKeyboardButton("Iya", callback_data=str(IPAS_MYTICKET_PROCESS_END))],
                        [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Pilih Iya jika benar :", reply_markup=reply_markup)
                    return IPAS_MYTICKET_CLOSED
        except:
            update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
            log_bot_success_ipas(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
            return ConversationHandler.END
    elif position is False: ##USER
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select count(*) as `count` from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and ticket = '{ticket_check}'"
            check_status = client.command(query)
            check_status = check_status == 0
            if check_status is True:
                update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
                log_bot_success_ipas(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
                return ConversationHandler.END
            elif check_status is False:
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select status from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                data_check = client.command(query)
                if data_check == 'closed':
                    update.message.reply_text(f"Maaf Ticket sudah closed\nKlik /menu")
                    log_bot_success_ipas(update, '*Status Laporan* ➞ Ticket sudah di closed')
                    return ConversationHandler.END
                elif data_check == 'open':
                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
                    client.command(query)
                    query = f"INSERT INTO production.action_swfm select '{chatid_telegram}','{ticket_check}','None','None','None'"
                    client.command(query)
                    query = f"select * from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                    data = client.command(query)
                    full_name = str(data[0]).title()
                    requests = 'https://t.me/{}'.format(data[1])
                    no_hp = data[3]
                    ticket = data[11]
                    regional = str(data[13])
                    problem_note = str(data[14])
                    problem__ = str(data[15]).replace('\\n',' ')
                    app = data[17]
                    date = str(data[18]).replace('-',' ')
                    update.message.reply_text(f'Creation Date : {date}\nApplication : #{app}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                    
                    keyboard = [
                        [InlineKeyboardButton("Iya", callback_data=str(IPAS_MYTICKET_PROCESS_END))],
                        [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Pilih Iya jika benar :", reply_markup=reply_markup)
                    return IPAS_MYTICKET_CLOSED
        except:
            update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
            log_bot_success_ipas(update, '*Status Laporan* ➞ Tidak memiliki laporan')
            return ConversationHandler.END
def ipas_myticket_closed(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Masukkan resolution action :",parse_mode=telegram.ParseMode.MARKDOWN)
    return IPAS_MYTICKET_CLOSED_END

def ipas_myticket_closed_end(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id
    full_name_closed = update.message.from_user.full_name
    handle_by = update.message.from_user.username
    now = datetime.now()
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    parameter = update.message.text.replace(',','.')
    update.message.reply_text("Proses closed tiket ...")
    time.sleep(3)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select * from production.action_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    data_list = str(data_select).replace("[","").replace("]","").replace("'","").replace('±','').replace('+','').replace("\\\\n",' ').split('\\n')
    for data in data_list:
        data = str(data).split(', ')
        ticket_log = data[1]

    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_report_swfm update  action_handle_by = '{handle_by}', action_resolution = '{parameter}', close_ticket_date = '{date_time}', status = 'closed' WHERE ticket = '{ticket_log}'"
    client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select username_telegram,fullname_telegram from production.helpdesk_report_swfm where ticket = '{ticket_log}'"
    data = client.command(query)
    requests = 'https://t.me/{}'.format(data[0])
    full_name = str(data[1]).title()
    update.message.reply_text(f"✅ Tiket [{full_name}]({requests}) telah closed\nKlik /menu", parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select username_telegram, fullname_telegram, channel_chatid, open_ticket_date, close_ticket_date, chatid_telegram from production.helpdesk_report_swfm where ticket = '{ticket_log}'"
    check_ticket = client.command(query)
    data_list = str(check_ticket).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    x = []
    for data in data_list:
        data = str(data).split(', ')

        open_str = f'{data[3]}, {data[4]}'
        closed_str = f'{data[5]}, {data[6]}'
        full_name = data[1]
        # Parsing string menjadi objek datetime
        open_date = datetime.strptime(open_str, "%d-%B-%Y, %H:%M:%S WIB")
        closed_date = datetime.strptime(closed_str, "%d-%B-%Y, %H:%M:%S WIB")
        # Menghitung selisih waktu
        selisih_waktu = closed_date - open_date
        # Mengambil selisih dalam bentuk hari
        day_difference = selisih_waktu

        #grup
        bot_log.send_message(chat_id=data[2],text=f'✅ Tiket *{ticket_log}* dari [{data[1]}]({data[0]}) telah *Terclosed* oleh {full_name_closed} dengan durasi → *{day_difference}*',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        ##user
        bot_log.send_message(chat_id=data[7],text=f'✅ Tiket anda *{ticket_log}* telah *Terclosed* oleh Admin HD {full_name_closed} dengan durasi → *{day_difference}*',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        log_bot_success_ipas(update, '*Tiket* ➞ Closed Tiket ✅')
    #HAPUS
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    return ConversationHandler.END

def ipas_broadcast(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *Broadcast Pesan*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Silahkan masukkan pesan anda",parse_mode=telegram.ParseMode.MARKDOWN)
    return IPAS_BROADCAST_END

def ipas_broadcast_end(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_swfm, registered_ioms, registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    check_data = client.command(query)
    check_swfm = check_data[0]
    check_ioms = check_data[1]
    check_ipas = check_data[2]
    if check_ipas == 'True':
        if os.path.exists("/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_ipas.txt"):
            os.remove("/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_ipas.txt")
            time.sleep(1)
            data_text = update.message.text.replace('_','').replace('*','')
            log_bot = open('/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_ipas.txt','a')
            log_bot.write("{}".format(data_text))
            log_bot.close()
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Terima Kasih anda telah membuat pesan siaran, sedang dalam proses pengiriman dan membutuhkan waktu sekitar 1,5 Jam, dikarenakan banyaknya user yang telah terdaftar di BOT. Terima kasih.',parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            print("The file does not exist")
            time.sleep(1)
            data_text = update.message.text.replace('_','').replace('*','')
            log_bot = open('/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_ipas.txt','a')
            log_bot.write("{}".format(data_text))
            log_bot.close()
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Terima Kasih anda telah membuat pesan siaran, sedang dalam proses pengiriman dan membutuhkan waktu sekitar 1,5 Jam, dikarenakan banyaknya user yang telah terdaftar di BOT. Terima kasih.',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_ipas(update, '*Broadcast Pesan* ➞ Pesan Siaran')
        return ConversationHandler.END

def ipas_makeadmin(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *Jadikan Admin*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Silahkan masukkan Username Telegram",parse_mode=telegram.ParseMode.MARKDOWN)
    return IPAS_MAKEADMIN_END

def ipas_makeadmin_end(update: Update, _: CallbackContext) -> None:
    username_telegram = update.message.text
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_bot_swfm where username_telegram = '{username_telegram}' and position = 'admin'"
    check_data = client.command(query)
    check_status = check_data == 0
    if check_status is True:
        query = f"ALTER TABLE production.helpdesk_bot_swfm update position = 'admin' where username_telegram = '{username_telegram}'"
        client.command(query)
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f'Username Telegram *{username_telegram}* sukses dijadikan Admin',parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f'Username tersebut sudah menjadi Admin',parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_ipas(update, '*Jadikan Admin* ➞ Username Telegram')
    return ConversationHandler.END

def ipas_postlink(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Anda memilih : *My Ticket List*',parse_mode=telegram.ParseMode.MARKDOWN)
    try:
        query = f"select fullname_telegram, username_telegram, ticket, problem_title, post_link from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' and category = 'IPAS' and status = 'open'"
        data = client.command(query)
        query = f"select count(*) as `count` from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and category = 'IPAS' and status = 'open'"
        count_query = client.command(query)
        query = update.callback_query
        query.answer()
        check_status = count_query == 0
        if check_status is True:
            query.message.reply_text(f'Maaf anda tidak mempunyai My Ticket List',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_ipas(update, '*My Ticket List* ➞ My Ticket List Tidak Ditemukan')
        elif check_status is False:
            query = f"select fullname_telegram, username_telegram, ticket, problem_title, post_link from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and category = 'IPAS' and status = 'open'"
            data1 = client.command(query)
            query = update.callback_query
            query.answer()
            data_list = str(data1).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
            output_text = ''
            output_text += '*Berikut adalah My Ticket List anda*\n\n'
            output_text += '*Category - Ticket - Post Link*\n'
            for data in data_list:
                data = str(data).split(', ')
                ticket = data[2]
                problem_title = str(data[3]).split(' ➞ ')[0]
                post_link = data[4]
                output_text += f"{problem_title} - {ticket} - {post_link}\n"
            output_text += '\n'
            output_text += 'Regards\nOCHABOT & Team'
            query.message.reply_text(f'{output_text}',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_ipas(update, '*My Ticket List* ➞ My Ticket List Ditemukan')
        return ConversationHandler.END
    except:
        query = update.callback_query
        query.answer()
        query.message.reply_text(f'Maaf anda tidak mempunyai My Ticket List',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_ipas(update, '*My Ticket List* ➞ My Ticket List Tidak Ditemukan')
        return ConversationHandler.END

def ipas_download_excel(update: Update, _: CallbackContext) -> None: 
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Mohon menunggu dalam beberapa detik...",parse_mode=telegram.ParseMode.MARKDOWN)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select * from production.helpdesk_report_swfm hrs  where status = 'open' and category = 'IPAS'"
    data = client.command(query)
    try:
        data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
        array_data = []
        for data in data_list:
            data = str(data).split(', ')
            dub_data = {'Nama': f'{data[0]}', 'Username Telegram': f'{data[1]}', 'Chatid Telegram': f'{data[2]}', 'No HP': f'{data[3]}', 'Email': f'{data[4]}', 'Remark': f'{data[5]}', 'Position' : f'{data[9]}', 'Channel Chatid': f'{data[10]}', 'Ticket': f'{data[11]}', 'Divison': f'{data[12]}', 'Regional': f'{data[13]}', 'Problem Title': f'{data[14]}', 'Problem Summary': f'{data[15]}', 'Status': f'{data[16]}', 'Category': f'{data[17]}', 'Open Ticket Date': f'{data[18]}, {data[19]}', 'Closed Ticket Date': f'{data[20]}', 'FCAPS': f'{data[21]}', 'Action Menu': f'{data[22]}', 'Action Category': f'{data[23]}', 'Action Handle By': f'{data[24]}', 'Action Resolution': f'{data[25]}', 'Post Link': f'{data[26]}'}
            array_data.append(dub_data)
    except:
        array_data = [{'Nama': '-', 'Username Telegram': '-', 'Chatid Telegram': '-', 'No HP': '-', 'Email': '-', 'Remark': '-', 'Position' : '-', 'Channel Chatid': '-', 'Ticket': '-', 'Divison': '-', 'Regional': '-', 'Problem Title': '-', 'Problem Summary': '-', 'Status': '-', 'Category': '-', 'Open Ticket Date': '- -', 'Closed Ticket Date': '-', 'FCAPS': '-', 'Action Menu': '-', 'Action Category': '-', 'Action Handle By': '-', 'Action Resolution': '-', 'Post Link': '-'}]
    query = f"select * from production.helpdesk_report_swfm hrs  where status = 'closed' and category = 'IPAS'"
    data = client.command(query)
    data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    array_data1 = []
    for data in data_list:
        data = str(data).split(', ')
        dub_data = {'Nama': f'{data[0]}', 'Username Telegram': f'{data[1]}', 'Chatid Telegram': f'{data[2]}', 'No HP': f'{data[3]}', 'Email': f'{data[4]}', 'Remark': f'{data[5]}', 'Position' : f'{data[9]}', 'Channel Chatid': f'{data[10]}', 'Ticket': f'{data[11]}', 'Divison': f'{data[12]}', 'Regional': f'{data[13]}', 'Problem Title': f'{data[14]}', 'Problem Summary': f'{data[15]}', 'Status': f'{data[16]}', 'Category': f'{data[17]}', 'Open Ticket Date': f'{data[18]}, {data[19]}', 'Closed Ticket Date': f'{data[20]},{data[21]}', 'FCAPS': f'{data[22]}', 'Action Menu': f'{data[23]}', 'Action Category': f'{data[24]}', 'Action Handle By': f'{data[25]}', 'Action Resolution': f'{data[26]}', 'Post Link': f'{data[27]}'}
        array_data1.append(dub_data)

    df1 = pd.DataFrame(array_data)
    df2 = pd.DataFrame(array_data1)
    writer = pd.ExcelWriter('/home/dimas/baru/helpdeskbot_v2/data/data_report_open_ticket_ioms.xlsx', engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Open Ticket', index=False)
    df2.to_excel(writer, sheet_name='Closed Ticket', index=False)
    writer.save()
    print('Sukses')
    syanticbot = telegram.Bot(token_bot) #SYANTICBOT
    syanticbot.sendDocument(chat_id = chatid_telegram, document=open('/home/dimas/baru/helpdeskbot_v2/data/data_report_open_ticket_ipas.xlsx','rb'), filename="Report Ticket IPAS.xlsx",caption='Ready to download Report Ticket IPAS')
    query = update.callback_query
    query.answer()
    query.message.reply_text(text="Berikut adalah link Download Aplikasi IPAS, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_inline_ipas(update, '*Download* ➞ Laporan Tiket Excel')
    return ConversationHandler.END

def ipas_complaint(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Anda memilih : *Eskalasi Case*',parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(f'Ketik nomor ticket anda IPSXXXXXXXX',parse_mode=telegram.ParseMode.MARKDOWN)
    return IPAS_COMPLAINT_END

def ipas_complaint_end(update: Update, _: CallbackContext) -> None: 
    parameter_ticket = update.message.text
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{parameter_ticket}' and category = 'IPAS'"
    check_status = client.command(query)
    check_status = check_status == 0
    if check_status is True:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f"Nomor tiket tidak sesuai kategori atau salah", parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_ipas(update, '*Eskalasi Case* ➞ Nomor Tiket Tidak Ditemukan')
    elif check_status is False:
        query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{parameter_ticket}' and category = 'IPAS' and status = 'closed'"
        check_status = client.command(query)
        check_status = check_status == 0
        if check_status is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f"Nomor tiket telah closed", parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_ipas(update, '*Eskalasi Case* ➞ Nomor Tiket Telah Closed')
        elif check_status is False:
            chatid_1 = '1207064180'
            chatid_2 = '1304677333'
            query = f"select ticket, post_link from production.helpdesk_report_swfm where ticket = '{parameter_ticket}'"
            data_redirect = client.command(query)
            post_link = data_redirect[1]
            bot_log.send_message(chat_id=chatid_1,text=f'Semangat Pagi Rekan...\n\nNomor Tiket  {parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_2,text=f'Semangat Pagi Rekan...\n\nNomor Tiket  {parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            log_bot_success_ipas_com(update, '*Eskalasi Case* ➞ Eskalasi Case Berhasil dengan Nomor Tiket '+parameter_ticket)
            update.message.reply_text(f"Anda berhasil membuat Eskalasi Case, Mohon ditunggu sampai Team HD merespon di room diskusi. Terima Kasih", parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END
################################################END IPAS#######################################

################################################MENU SWFM#######################################
def menu_swfm(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    ##access
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_swfm from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *SWFM*",parse_mode=telegram.ParseMode.MARKDOWN)
    if data == 'True':
        query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
        data = client.command(query)
        query = update.callback_query
        query.answer()
        position = data == 'admin'
        print(data)
        if position is True: ##ADMIN
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(SWFM_REQTICKET))],
                [InlineKeyboardButton("Tim Ahli >>", callback_data=str(SWFM_EXPERT))],
                [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(SWFM_MYTICKET))],
                [InlineKeyboardButton("Pusat Bantuan", callback_data=str(SWFM_BANTUAN))],
                [InlineKeyboardButton("Broadcast Pesan", callback_data=str(SWFM_BROADCAST))],
                [InlineKeyboardButton("Jadikan Admin", callback_data=str(SWFM_MAKEADMIN))],
                [InlineKeyboardButton("Hapus UserBot", callback_data=str(DEL_USERBOT))],
                # [InlineKeyboardButton("Download Aplikasi", callback_data=str(SWFM_DOWNLOAD))],
                [InlineKeyboardButton("Download Laporan Tiket", callback_data=str(SWFM_DOWNLOAD_EXCEL))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(SWFM_POSTLINK))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(SWFM_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        elif position is False: ##USER
            keyboard = [
                [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(SWFM_REQTICKET))],
                [InlineKeyboardButton("Status Laporan", callback_data=str(SWFM_MYTICKET))],
                [InlineKeyboardButton("Pusat Bantuan", callback_data=str(SWFM_BANTUAN))],
                # [InlineKeyboardButton("Download Aplikasi", callback_data=str(SWFM_DOWNLOAD))],
                [InlineKeyboardButton("My Ticket List", callback_data=str(SWFM_POSTLINK))],
                [InlineKeyboardButton("Eskalasi Case", callback_data=str(SWFM_COMPLAINT))],
                [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :", reply_markup=reply_markup)
        return MENU
    elif data == 'False':
        query = update.callback_query
        query.answer()
        query.message.reply_text(f"Mohon registrasi Menu SWFM terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_fail_inline_swfm(update, '*Menu* ➞ Akun Belum registrasi Menu SWFM')
        return ConversationHandler.END


    
def swfm_reqticket(update: Update, _: CallbackContext) -> None:
    try:
        keyboard = [
            [InlineKeyboardButton("R1 SUMBAGUT >>", callback_data=str(SWFM_REQTICKET1))],
            [InlineKeyboardButton("R2 SUMBAGSEL >>", callback_data=str(SWFM_REQTICKET2))],
            [InlineKeyboardButton("R3 JABOTABEK-INNER >>", callback_data=str(SWFM_REQTICKET3))],
            [InlineKeyboardButton("R4 WEST JAVA >>", callback_data=str(SWFM_REQTICKET4))],
            [InlineKeyboardButton("R5 CENTRAL JAVA >>", callback_data=str(SWFM_REQTICKET5))],
            [InlineKeyboardButton("R6 EAST JAVA >>", callback_data=str(SWFM_REQTICKET6))],
            [InlineKeyboardButton("R7 BALI NUSRA >>", callback_data=str(SWFM_REQTICKET7))],
            [InlineKeyboardButton("R8 KALIMANTAN >>", callback_data=str(SWFM_REQTICKET8))],
            [InlineKeyboardButton("R9 SULAWESI >>", callback_data=str(SWFM_REQTICKET9))],
            [InlineKeyboardButton("R10 SUMBAGTENG >>", callback_data=str(SWFM_REQTICKET10))],
            [InlineKeyboardButton("R11 PUMA >>", callback_data=str(SWFM_REQTICKET11))],
            [InlineKeyboardButton("R12 JABOTABEK-OUTER >>", callback_data=str(SWFM_REQTICKET12))],
            [InlineKeyboardButton("HQ >>", callback_data=str(SWFM_REQTICKET13))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_SWFM))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id-1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text="Anda memilih : *Laporan Kendala*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    except:
        keyboard = [
            [InlineKeyboardButton("R1 SUMBAGUT >>", callback_data=str(SWFM_REQTICKET1))],
            [InlineKeyboardButton("R2 SUMBAGSEL >>", callback_data=str(SWFM_REQTICKET2))],
            [InlineKeyboardButton("R3 JABOTABEK-INNER >>", callback_data=str(SWFM_REQTICKET3))],
            [InlineKeyboardButton("R4 WEST JAVA >>", callback_data=str(SWFM_REQTICKET4))],
            [InlineKeyboardButton("R5 CENTRAL JAVA >>", callback_data=str(SWFM_REQTICKET5))],
            [InlineKeyboardButton("R6 EAST JAVA >>", callback_data=str(SWFM_REQTICKET6))],
            [InlineKeyboardButton("R7 BALI NUSRA >>", callback_data=str(SWFM_REQTICKET7))],
            [InlineKeyboardButton("R8 KALIMANTAN >>", callback_data=str(SWFM_REQTICKET8))],
            [InlineKeyboardButton("R9 SULAWESI >>", callback_data=str(SWFM_REQTICKET9))],
            [InlineKeyboardButton("R10 SUMBAGTENG >>", callback_data=str(SWFM_REQTICKET10))],
            [InlineKeyboardButton("R11 PUMA >>", callback_data=str(SWFM_REQTICKET11))],
            [InlineKeyboardButton("R12 JABOTABEK-OUTER >>", callback_data=str(SWFM_REQTICKET12))],
            [InlineKeyboardButton("HQ >>", callback_data=str(SWFM_REQTICKET13))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_SWFM))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Anda memilih : *Laporan Kendala*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
def swfm_reqticket_add(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")

    chatid_telegram = update.callback_query.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update regional = '{data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    try:
        keyboard = [
            [InlineKeyboardButton("ANT >>", callback_data=str(SWFM_CAT1))],
            [InlineKeyboardButton("Aplication Error >>", callback_data=str(SWFM_CAT2))],
            [InlineKeyboardButton("BPS Manual >>", callback_data=str(SWFM_CAT3))],
            [InlineKeyboardButton("CGL (IMBAS PETIR) >>", callback_data=str(SWFM_CAT4))],
            [InlineKeyboardButton("Cant Check In >>", callback_data=str(SWFM_CAT5))],
            [InlineKeyboardButton("KPI >>", callback_data=str(SWFM_CAT6))],
            [InlineKeyboardButton("Master Data Management >>", callback_data=str(SWFM_CAT7))],
            [InlineKeyboardButton("Mobile >>", callback_data=str(SWFM_CAT8))],
            [InlineKeyboardButton("Performance >>", callback_data=str(SWFM_CAT9))],
            [InlineKeyboardButton("Preventive Maintenance >>", callback_data=str(SWFM_CAT10))],
            [InlineKeyboardButton("RH Visit >>", callback_data=str(SWFM_CAT11))],
            [InlineKeyboardButton("Site Refference >>", callback_data=str(SWFM_CAT12))],
            [InlineKeyboardButton("Teritory Operation >>", callback_data=str(SWFM_CAT13))],
            [InlineKeyboardButton("Ticketing Handling >>", callback_data=str(SWFM_CAT14))],
            [InlineKeyboardButton("TPAS >>", callback_data=str(SWFM_CAT15))],
            [InlineKeyboardButton("TS Manual >>", callback_data=str(SWFM_CAT16))],
            [InlineKeyboardButton("User Management >>", callback_data=str(SWFM_CAT17))],
            # [InlineKeyboardButton("Other Problems", callback_data=str(SWFM_CAT18))],
            [InlineKeyboardButton("TANYA PROSES ?", callback_data=str(SWFM_CAT19))],
            [InlineKeyboardButton("Kembali", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Penjelasan Kategori: \n*ANT :* *TOTI ➞ Create Ticket, TOTI ➞ View File Evidence, RPM ➞ Approval Ticket, RPM ➞ View File Evidence*\n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*BPS Manual :* Cant Submit Ticket, Menu Error, Service Variable Activity, BPS Ticket Not Appearing\n*CGL (IMBAS PETIR) :* Data Not Synchrone, Menu Error, Interference Lightning Claim\n*Cant Check In :* Site Refference, Ticketing Handling, Teritory Operation, TS Manual\n*KPI :* Data Not Found, Data Not Synchrone, Menu Error, Requests Takeout Ticket\n*Master Data Management :* *Site List Management ➞ Area, Site List Management ➞ Cluster, Site List Management ➞ Longlat, Site List Management ➞ NOP, Site List Management ➞ Regional, Site List Management ➞ Site Class, Site List Management ➞ Site Name, Site List Management ➞ Site Owner, Site List Management ➞ Site Type*\n*Mobile :* Change Role, Connection, Data Not Found, Data Not Synchrone, Daya Listrik, GPS Error, Knowladge, Menu Error, Register with Another Device\n*Performance :* *eBAIP ➞ Export BAIP, eBAIP ➞ Fill Form BAIP, eBAPP ➞ Signature Configuration, eBAPP ➞ Submit BAPP, eBAPP ➞ Fill Form BAPP, eKPI ➞ Submit KPI*\n*Preventive Maintenance :* Data Not Synchrone, Menu Error, New Menu, Cant Approve, Cant Follow Up, Genset, Sampling, Site, *SPlanning ➞ Approval, SPlanning ➞ Menu Error, SPlanning ➞ Change Schedule, SPlanning ➞ Notification Error, SPlanning ➞ Login, SPlanning ➞ Add Site, SPlanning ➞ Take Out Site, SPlanning ➞ Switch Site, SPlanning ➞ Change Date, SPlanning ➞ Extend Permit, SPlanning ➞ Print Permit*\n*RH Visit :* Cant Follow Up Ticket, Data Not Synchrone, Cant Approve, Menu Error\n*Site Refference :* Change Area, Data Not Found\n*Teritory Operation :* Add Area, Data Not Synchrone, Data Site Wrong\n*Ticketing Handling : *Alarm Ticket, Cant Approve, Cant Close, Change Area, Clear Time Delay, Data Not Found, Data Not Synchrone, Menu MBP Error, Import Area, Menu Error, Menu TS Error, Wrong Mapping Ticket, *Personal Tracking ➞ Info Clock In or Clock Out TO, Personal Tracking ➞ Tickets Handled, Personal Tracking ➞ Export, Fault Center ➞ Export PDF, Fault Center ➞ Manual Dispatch, Fault Center ➞ Escalate to INSERA TELKOM, Fault Center ➞ Escalate to TP Site Owner, Fault Center ➞ Update RCA, Fault Center ➞ Resolved Ticket, SVA ➞ Create Ticket, SVA ➞ Export Ticket, SVA ➞ Update Draft Ticket*\n*TPAS :* *Permit Approval ➞ Approval Permit, Permit Approval ➞ View Detail Permit, Permit Approval ➞ Search Permit*\n*TS Manual : *Menu Error\n*User Management : *Change Area User, Change Role, Invalid Email, Invalid Password, Menu Error, New User, Registered with Another Device, Req Double Area, Reset Password, User Not Found, Delete User, *Manage User Mobile ➞ Change Data User Mobile, Manage User Mobile ➞ Add User Mobile*\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    except:
        keyboard = [
            [InlineKeyboardButton("ANT >>", callback_data=str(SWFM_CAT1))],
            [InlineKeyboardButton("Aplication Error >>", callback_data=str(SWFM_CAT2))],
            [InlineKeyboardButton("BPS Manual >>", callback_data=str(SWFM_CAT3))],
            [InlineKeyboardButton("CGL (IMBAS PETIR) >>", callback_data=str(SWFM_CAT4))],
            [InlineKeyboardButton("Cant Check In >>", callback_data=str(SWFM_CAT5))],
            [InlineKeyboardButton("KPI >>", callback_data=str(SWFM_CAT6))],
            [InlineKeyboardButton("Master Data Management >>", callback_data=str(SWFM_CAT7))],
            [InlineKeyboardButton("Mobile >>", callback_data=str(SWFM_CAT8))],
            [InlineKeyboardButton("Performance >>", callback_data=str(SWFM_CAT9))],
            [InlineKeyboardButton("Preventive Maintenance >>", callback_data=str(SWFM_CAT10))],
            [InlineKeyboardButton("RH Visit >>", callback_data=str(SWFM_CAT11))],
            [InlineKeyboardButton("Site Refference >>", callback_data=str(SWFM_CAT12))],
            [InlineKeyboardButton("Teritory Operation >>", callback_data=str(SWFM_CAT13))],
            [InlineKeyboardButton("Ticketing Handling >>", callback_data=str(SWFM_CAT14))],
            [InlineKeyboardButton("TPAS >>", callback_data=str(SWFM_CAT15))],
            [InlineKeyboardButton("TS Manual >>", callback_data=str(SWFM_CAT16))],
            [InlineKeyboardButton("User Management >>", callback_data=str(SWFM_CAT17))],
            # [InlineKeyboardButton("Other Problems", callback_data=str(SWFM_CAT18))],
            [InlineKeyboardButton("TANYA PROSES ?", callback_data=str(SWFM_CAT19))],
            [InlineKeyboardButton("Kembali", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Penjelasan Kategori: \n*ANT :* *TOTI ➞ Create Ticket, TOTI ➞ View File Evidence, RPM ➞ Approval Ticket, RPM ➞ View File Evidence*\n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*BPS Manual :* Cant Submit Ticket, Menu Error, Service Variable Activity, BPS Ticket Not Appearing\n*CGL (IMBAS PETIR) :* Data Not Synchrone, Menu Error, Interference Lightning Claim\n*Cant Check In :* Site Refference, Ticketing Handling, Teritory Operation, TS Manual\n*KPI :* Data Not Found, Data Not Synchrone, Menu Error, Requests Takeout Ticket\n*Master Data Management :* *Site List Management ➞ Area, Site List Management ➞ Cluster, Site List Management ➞ Longlat, Site List Management ➞ NOP, Site List Management ➞ Regional, Site List Management ➞ Site Class, Site List Management ➞ Site Name, Site List Management ➞ Site Owner, Site List Management ➞ Site Type*\n*Mobile :* Change Role, Connection, Data Not Found, Data Not Synchrone, Daya Listrik, GPS Error, Knowladge, Menu Error, Register with Another Device\n*Performance :* *eBAIP ➞ Export BAIP, eBAIP ➞ Fill Form BAIP, eBAPP ➞ Signature Configuration, eBAPP ➞ Submit BAPP, eBAPP ➞ Fill Form BAPP, eKPI ➞ Submit KPI*\n*Preventive Maintenance :* Data Not Synchrone, Menu Error, New Menu, Cant Approve, Cant Follow Up, Genset, Sampling, Site, *SPlanning ➞ Approval, SPlanning ➞ Menu Error, SPlanning ➞ Change Schedule, SPlanning ➞ Notification Error, SPlanning ➞ Login, SPlanning ➞ Add Site, SPlanning ➞ Take Out Site, SPlanning ➞ Switch Site, SPlanning ➞ Change Date, SPlanning ➞ Extend Permit, SPlanning ➞ Print Permit*\n*RH Visit :* Cant Follow Up Ticket, Data Not Synchrone, Cant Approve, Menu Error\n*Site Refference :* Change Area, Data Not Found\n*Teritory Operation :* Add Area, Data Not Synchrone, Data Site Wrong\n*Ticketing Handling : *Alarm Ticket, Cant Approve, Cant Close, Change Area, Clear Time Delay, Data Not Found, Data Not Synchrone, Menu MBP Error, Import Area, Menu Error, Menu TS Error, Wrong Mapping Ticket, *Personal Tracking ➞ Info Clock In or Clock Out TO, Personal Tracking ➞ Tickets Handled, Personal Tracking ➞ Export, Fault Center ➞ Export PDF, Fault Center ➞ Manual Dispatch, Fault Center ➞ Escalate to INSERA TELKOM, Fault Center ➞ Escalate to TP Site Owner, Fault Center ➞ Update RCA, Fault Center ➞ Resolved Ticket, SVA ➞ Create Ticket, SVA ➞ Export Ticket, SVA ➞ Update Draft Ticket*\n*TPAS :* *Permit Approval ➞ Approval Permit, Permit Approval ➞ View Detail Permit, Permit Approval ➞ Search Permit*\n*TS Manual : *Menu Error\n*User Management : *Change Area User, Change Role, Invalid Email, Invalid Password, Menu Error, New User, Registered with Another Device, Req Double Area, Reset Password, User Not Found, Delete User, *Manage User Mobile ➞ Change Data User Mobile, Manage User Mobile ➞ Add User Mobile*\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)

def swfm_reqticket_add1(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    # print(f"yang ini {data_text}")
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    message_id = query.message.message_id-1
    chat_id = update.callback_query.from_user.id
    bot_log.delete_message(chat_id,message_id)
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'BPS Manual' in data_text:
        keyboard = [
            [InlineKeyboardButton("Menu Error (Menu Eror)", callback_data=str(SWFM_CAT1_1))],
            [InlineKeyboardButton("BPS Ticket Not Appearing (Ticket BPS Tidak Muncul)", callback_data=str(SWFM_CAT1_2))],
            [InlineKeyboardButton("Cant Submit Ticket (Tidak Dapat submit Tiket)", callback_data=str(SWFM_CAT1_3))],
            [InlineKeyboardButton("SVA (Aktivitas Variabel Layanan)", callback_data=str(SWFM_CAT1_4))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT1_5))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'KPI' in data_text:
        keyboard = [
            [InlineKeyboardButton("Data Not Found (Data Tidak Ditemukan)", callback_data=str(SWFM_CAT2_1))],
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(SWFM_CAT2_2))],
            [InlineKeyboardButton("Requests Takeout Ticket (Permintaan Tiket Hapus)", callback_data=str(SWFM_CAT2_3))],
            [InlineKeyboardButton("Menu Error (Menu Eror)", callback_data=str(SWFM_CAT2_4))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT2_5))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Mobile' in data_text:
        keyboard = [
            [InlineKeyboardButton("Change Role (Ganti Role)", callback_data=str(SWFM_CAT3_1))],
            [InlineKeyboardButton("Connection (Koneksi)", callback_data=str(SWFM_CAT3_2))],
            [InlineKeyboardButton("Data Not Found (Data Tidak Ditemukan)", callback_data=str(SWFM_CAT3_3))],
            [InlineKeyboardButton("Electrical power (Daya Listrik)", callback_data=str(SWFM_CAT3_4))],
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(SWFM_CAT3_5))],
            [InlineKeyboardButton("GPS Error (GPS Eror)", callback_data=str(SWFM_CAT3_6))],
            [InlineKeyboardButton("Knowladge (Pengetahuan)", callback_data=str(SWFM_CAT3_7))],
            [InlineKeyboardButton("Menu Error (Menu Eror)", callback_data=str(SWFM_CAT3_8))],
            [InlineKeyboardButton("Registered with Another Device (Terdaftar dengan Perangkat Lain)", callback_data=str(SWFM_CAT3_9))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT3_10))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Preventive Maintenance' in data_text:
        keyboard = [
            [InlineKeyboardButton("Cant Approve (Tidak Dapat diApprove)", callback_data=str(SWFM_CAT9_1))],
            [InlineKeyboardButton("Cant Follow Up (Tiket Tidak Dapat Di Follow Up)", callback_data=str(SWFM_CAT9_2))],
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(SWFM_CAT9_3))],
            [InlineKeyboardButton("Cant Save Photos (Tidak Dapat Menyimpan Foto)", callback_data=str(SWFM_CAT9_18))],
            [InlineKeyboardButton("Cant take over (Tidak Bisa Mengambil Alih)", callback_data=str(SWFM_CAT9_19))],
            [InlineKeyboardButton("Unable to Upload (Tidak Dapat Mengunggah)", callback_data=str(SWFM_CAT9_20))],
            [InlineKeyboardButton("Buttons are not Clickable (Tombol Tidak Dapat Diklik)", callback_data=str(SWFM_CAT9_21))],
            [InlineKeyboardButton("Menu Error (Menu Eror)", callback_data=str(SWFM_CAT9_4))],
            [InlineKeyboardButton("New Menu (Menu Baru)", callback_data=str(SWFM_CAT9_5))],
            [InlineKeyboardButton("Genset (Genset) >>", callback_data=str(SWFM_CAT9_PMGENSET))],
            [InlineKeyboardButton("Site (Site) >>", callback_data=str(SWFM_CAT9_PMSITE))],
            [InlineKeyboardButton("Sampling (Sampling) >>", callback_data=str(SWFM_CAT9_PMSAMPLING))],
            [InlineKeyboardButton("SPlanning ➞ Approval (Perencanaan Jadwal ➞ Persetujuan)", callback_data=str(SWFM_CAT9_6))],
            [InlineKeyboardButton("SPlanning ➞ Menu Error (Perencanaan Jadwal ➞ Menu Eror)", callback_data=str(SWFM_CAT9_7))],
            [InlineKeyboardButton("SPlanning ➞ Change Schedule (Perencanaan Jadwal ➞ Ubah Jadwal)", callback_data=str(SWFM_CAT9_8))],
            [InlineKeyboardButton("SPlanning ➞ Notification Error (Perencanaan Jadwal ➞ Pemberitahuan Eror)", callback_data=str(SWFM_CAT9_9))],
            [InlineKeyboardButton("SPlanning ➞ Login (Perencanaan Jadwal ➞ Gabung)", callback_data=str(SWFM_CAT9_10))],
            [InlineKeyboardButton("SPlanning ➞ Add Site (Perencanaan Jadwal ➞ Tambah Site)", callback_data=str(SWFM_CAT9_11))],
            [InlineKeyboardButton("SPlanning ➞ Take Out Site (Perencanaan Jadwal ➞ Keluarkan Site)", callback_data=str(SWFM_CAT9_12))],
            [InlineKeyboardButton("SPlanning ➞ Switch Site (Perencanaan Jadwal ➞ Beralih Site)", callback_data=str(SWFM_CAT9_13))],
            [InlineKeyboardButton("SPlanning ➞ Change Date (Perencanaan Jadwal ➞ Ganti Tanggal)", callback_data=str(SWFM_CAT9_14))],
            [InlineKeyboardButton("SPlanning ➞ Extend Permit (Perencanaan Jadwal ➞ Perpanjang Izin)", callback_data=str(SWFM_CAT9_15))],
            [InlineKeyboardButton("SPlanning ➞ Print Permit (Perencanaan Jadwal ➞ Izin Cetak)", callback_data=str(SWFM_CAT9_16))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT9_17))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Site Refference' in data_text:
        keyboard = [
            [InlineKeyboardButton("Change Area (Ganti Area)", callback_data=str(SWFM_CAT4_1))],
            [InlineKeyboardButton("Data Not Found (Data Tidak Ditemukan)", callback_data=str(SWFM_CAT4_2))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT4_3))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Teritory Operation' in data_text:
        keyboard = [
            [InlineKeyboardButton("Add Area (Tambah Area)", callback_data=str(SWFM_CAT5_1))],
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(SWFM_CAT5_2))],
            [InlineKeyboardButton("Data Site Wrong (Data Site Salah)", callback_data=str(SWFM_CAT5_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT5_4))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Ticketing Handling' in data_text:
        keyboard = [
            [InlineKeyboardButton("Alarm Ticket (Alarm Tiket)", callback_data=str(SWFM_CAT6_1))],
            [InlineKeyboardButton("Cant Approve (Tidak Dapat diApprove)", callback_data=str(SWFM_CAT6_2))],
            [InlineKeyboardButton("Cant Close (Tidak Bisa Tutup)", callback_data=str(SWFM_CAT6_3))],
            [InlineKeyboardButton("Change Area (Ganti Area)", callback_data=str(SWFM_CAT6_4))],
            [InlineKeyboardButton("Clear Time Delay (Hapus Waktu Tunda)", callback_data=str(SWFM_CAT6_5))],
            [InlineKeyboardButton("Data Not Found (Data Tidak Ditemukan)", callback_data=str(SWFM_CAT6_6))],
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(SWFM_CAT6_7))],
            [InlineKeyboardButton("Menu MBP Error (Menu MBP Eror)", callback_data=str(SWFM_CAT6_8))],
            [InlineKeyboardButton("Menu TS Error (Menu TS Eror)", callback_data=str(SWFM_CAT6_9))],
            [InlineKeyboardButton("Import Area (Impor Area)", callback_data=str(SWFM_CAT6_10))],
            [InlineKeyboardButton("Menu Error (Menu Eror)", callback_data=str(SWFM_CAT6_11))],
            [InlineKeyboardButton("Wrong Mapping Ticket (Pemetaan Tiket Salah)", callback_data=str(SWFM_CAT6_12))],
            [InlineKeyboardButton("Personal Tracking ➞ Clock In or Clock Out TO (Pelacakan Pribadi ➞ Info Jam Masuk atau Keluar TO)", callback_data=str(SWFM_CAT6_13))],
            [InlineKeyboardButton("Personal Tracking ➞ Tickets Handled (Pelacakan Pribadi ➞ Tiket DItangani)", callback_data=str(SWFM_CAT6_14))],
            [InlineKeyboardButton("Personal Tracking ➞ Export (Pelacakan Pribadi ➞ Ekspor)", callback_data=str(SWFM_CAT6_15))],
            [InlineKeyboardButton("SVA ➞ Update Draft Ticket (SVA ➞ Perbarui Rancangan Tiket)", callback_data=str(SWFM_CAT6_16))],
            [InlineKeyboardButton("SVA ➞ Export Ticket (SVA ➞ Ekspor Tiket)", callback_data=str(SWFM_CAT6_17))],
            [InlineKeyboardButton("SVA ➞ Create Ticket (SVA ➞ Buat Tiket)", callback_data=str(SWFM_CAT6_18))],
            [InlineKeyboardButton("Fault Center ➞ Export PDF (Fault Center ➞ Ekspor PDF)", callback_data=str(SWFM_CAT6_19))],
            [InlineKeyboardButton("Fault Center ➞ Manual Dispatch (Fault Center ➞ Pengiriman Manual)", callback_data=str(SWFM_CAT6_20))],
            [InlineKeyboardButton("Fault Center ➞ Escalate to INSERRA TELKOM (Fault Center ➞ Eskalasi ke INSERRA TELKOM)", callback_data=str(SWFM_CAT6_21))],
            [InlineKeyboardButton("Fault Center ➞ Escalate to TP Site Owner (Fault Center ➞ Eskalasi ke TP Site Owner)", callback_data=str(SWFM_CAT6_22))],
            [InlineKeyboardButton("Fault Center ➞ Update RCA (Fault Center ➞ Perbarui RCA)", callback_data=str(SWFM_CAT6_23))],
            [InlineKeyboardButton("Fault Center ➞ Resolved Ticket  (Fault Center ➞ Menyelesaikan Tiket)", callback_data=str(SWFM_CAT6_24))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT6_25))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'TS Manual' in data_text:
        keyboard = [
            [InlineKeyboardButton("Menu Error (Menu Eror)", callback_data=str(SWFM_CAT7_1))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT7_2))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'User Management' in data_text:
        keyboard = [
            [InlineKeyboardButton("Change Area User (Ubah Area User)", callback_data=str(SWFM_CAT8_1))],
            [InlineKeyboardButton("Change Role (Ganti Role)", callback_data=str(SWFM_CAT8_2))],
            [InlineKeyboardButton("Delete User (Hapus User)", callback_data=str(SWFM_CAT8_3))],
            [InlineKeyboardButton("Invalid Email (Email tidak valid)", callback_data=str(SWFM_CAT8_4))],
            [InlineKeyboardButton("Invalid Password (Password tidak valid)", callback_data=str(SWFM_CAT8_5))],
            [InlineKeyboardButton("Menu Error (Menu Error)", callback_data=str(SWFM_CAT8_6))],
            [InlineKeyboardButton("New User (User Baru)", callback_data=str(SWFM_CAT8_7))],
            [InlineKeyboardButton("Registered with Another Device (Terdaftar dengan Perangkat Lain)", callback_data=str(SWFM_CAT8_8))],
            [InlineKeyboardButton("Req Double Area (Persyaratan Area Ganda)", callback_data=str(SWFM_CAT8_9))],
            [InlineKeyboardButton("Reset Password (Atur Ulang Kata Sandi)", callback_data=str(SWFM_CAT8_10))],
            [InlineKeyboardButton("User Not Found (User Tidak Ditemukan)", callback_data=str(SWFM_CAT8_11))],
            [InlineKeyboardButton("Manage User Mobile ➞ Change Date User Mobie (Manage User Mobile ➞ Ubah Tanggal Pengguna Ponsel)", callback_data=str(SWFM_CAT8_12))],
            [InlineKeyboardButton("Manage User Mobile ➞ Add User Mobile (Manage User Mobile ➞ Tambah Pengguna Ponsel)", callback_data=str(SWFM_CAT8_13))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT8_14))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'CGL (IMBAS PETIR)' in data_text:
        keyboard = [
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(SWFM_CAT11_1))],
            [InlineKeyboardButton("Menu Error (Menu Eror)", callback_data=str(SWFM_CAT11_2))],
            [InlineKeyboardButton("Interference Lightning Claim ➞ Create Ticket (Klaim Petir Gangguan ➞ Buat Tiket)", callback_data=str(SWFM_CAT11_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT11_4))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'RH Visit' in data_text:
        keyboard = [
            [InlineKeyboardButton("Cant Approve (Tidak Dapat diApprove)", callback_data=str(SWFM_CAT12_1))],
            [InlineKeyboardButton("Cant Follow Up Ticket (Tiket Tidak Dapat Di Follow Up)", callback_data=str(SWFM_CAT12_2))],
            [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(SWFM_CAT12_3))],
            [InlineKeyboardButton("Menu Error (Menu Eror)", callback_data=str(SWFM_CAT12_4))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT12_5))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Cant Check In' in data_text:
        keyboard = [
            [InlineKeyboardButton("Site Refference (Kategori)", callback_data=str(SWFM_CAT13_1))],
            [InlineKeyboardButton("Ticketing Handling (Kategori)", callback_data=str(SWFM_CAT13_2))],
            [InlineKeyboardButton("Teritory Operation (Kategori)", callback_data=str(SWFM_CAT13_3))],
            [InlineKeyboardButton("TS Manual (Kategori)", callback_data=str(SWFM_CAT13_4))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT13_5))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Aplication Error' in data_text:
        keyboard = [
            [InlineKeyboardButton("Loading after Login (Loading Setelah Login)", callback_data=str(SWFM_CAT14_1))],
            [InlineKeyboardButton("Log out Yourself (Logout Sendiri)", callback_data=str(SWFM_CAT14_2))],
            [InlineKeyboardButton("Hang (Gantung)", callback_data=str(SWFM_CAT14_3))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT14_4))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'ANT' in data_text:
        keyboard = [
            [InlineKeyboardButton("TOTI ➞ Create Ticket (TOTI ➞ Buat Tiket)", callback_data=str(SWFM_CAT15_1))],
            [InlineKeyboardButton("TOTI ➞ View File Evidence (TOTI ➞ Lihat Bukti File)", callback_data=str(SWFM_CAT15_2))],
            [InlineKeyboardButton("RPM ➞ View File Evidence (RPM ➞ Lihat Bukti File)", callback_data=str(SWFM_CAT15_3))],
            [InlineKeyboardButton("RPM ➞ Approval Ticket (RPM ➞ Persetujuan Tiket)", callback_data=str(SWFM_CAT15_4))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT15_5))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Master Data Management' in data_text:
        keyboard = [
            [InlineKeyboardButton("Site List Management ➞ Area (Site List Management ➞ Area)", callback_data=str(SWFM_CAT16_1))],
            [InlineKeyboardButton("Site List Management ➞ Cluster (Site List Management ➞ Cluster)", callback_data=str(SWFM_CAT16_2))],
            [InlineKeyboardButton("Site List Management ➞ Longlat (Site List Management ➞ Longlat)", callback_data=str(SWFM_CAT16_3))],
            [InlineKeyboardButton("Site List Management ➞ NOP (Site List Management ➞ NOP)", callback_data=str(SWFM_CAT16_4))],
            [InlineKeyboardButton("Site List Management ➞ Regional (Site List Management ➞ Regional)", callback_data=str(SWFM_CAT16_5))],
            [InlineKeyboardButton("Site List Management ➞ Site Class (Site List Management ➞ Site Class)", callback_data=str(SWFM_CAT16_6))],
            [InlineKeyboardButton("Site List Management ➞ Site Name (Site List Management ➞ Site Name)", callback_data=str(SWFM_CAT16_7))],
            [InlineKeyboardButton("Site List Management ➞ Site Owner (Site List Management ➞ Site Owner)", callback_data=str(SWFM_CAT16_8))],
            [InlineKeyboardButton("Site List Management ➞ Site Type (Site List Management ➞ Site Type)", callback_data=str(SWFM_CAT16_9))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT16_10))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Performance' in data_text:
        keyboard = [
            [InlineKeyboardButton("eBAIP ➞ Export BAIP (eKPI ➞ Ekspor BAIP)", callback_data=str(SWFM_CAT17_1))],
            [InlineKeyboardButton("eBAIP ➞ Fill Form BAIP (eKPI ➞ Isi Formulir BAIP)", callback_data=str(SWFM_CAT17_2))],
            [InlineKeyboardButton("eBAPP ➞ Signature Configuration (eKPI ➞ Konfigurasi Tanda Tangan)", callback_data=str(SWFM_CAT17_3))],
            [InlineKeyboardButton("eBAPP ➞ Submit BAPP (eKPI ➞ Menyerahkan BAPP)", callback_data=str(SWFM_CAT17_4))],
            [InlineKeyboardButton("eBAPP ➞ Fill Form BAPP (eKPI ➞ Isi Formulir BAPP)", callback_data=str(SWFM_CAT17_5))],
            [InlineKeyboardButton("eKPI ➞ Submit KPI (eKPI ➞ Menyerahkan KPI)", callback_data=str(SWFM_CAT17_6))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT17_7))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'TPAS' in data_text:
        keyboard = [
            [InlineKeyboardButton("Permit Approval ➞ Approval Permit (Persetujuan Izin ➞ Izin Persetujuan)", callback_data=str(SWFM_CAT18_1))],
            [InlineKeyboardButton("Permit Approval ➞ View Detail Permit (Persetujuan Izin ➞ Izin Melihat Detail)", callback_data=str(SWFM_CAT18_2))],
            [InlineKeyboardButton("Permit Approval ➞ Search Permit (Persetujuan Izin ➞ Izin Pencarian)", callback_data=str(SWFM_CAT18_3))],
            [InlineKeyboardButton("Cant Approve (Tidak Dapat diApprove)", callback_data=str(SWFM_CAT18_4))],
            [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT18_5))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'TANYA PROSES ?' in data_text:
        keyboard = [
            [InlineKeyboardButton("ANT", callback_data=str(SWFM_CAT19_1))],
            [InlineKeyboardButton("BPS Manual", callback_data=str(SWFM_CAT19_2))],
            [InlineKeyboardButton("CGL (IMBAS PETIR)", callback_data=str(SWFM_CAT19_3))],
            [InlineKeyboardButton("Cant Check In", callback_data=str(SWFM_CAT19_4))],
            [InlineKeyboardButton("KPI", callback_data=str(SWFM_CAT19_5))],
            [InlineKeyboardButton("Master Data Management", callback_data=str(SWFM_CAT19_6))],
            [InlineKeyboardButton("Mobile", callback_data=str(SWFM_CAT19_7))],
            [InlineKeyboardButton("Performance", callback_data=str(SWFM_CAT19_8))],
            [InlineKeyboardButton("Preventive Maintenance", callback_data=str(SWFM_CAT19_9))],
            [InlineKeyboardButton("RH Visit", callback_data=str(SWFM_CAT19_10))],
            [InlineKeyboardButton("Site Refference", callback_data=str(SWFM_CAT19_11))],
            [InlineKeyboardButton("Teritory Operation", callback_data=str(SWFM_CAT19_12))],
            [InlineKeyboardButton("Ticketing Handling", callback_data=str(SWFM_CAT19_13))],
            [InlineKeyboardButton("TPAS", callback_data=str(SWFM_CAT19_14))],
            [InlineKeyboardButton("TS Manual", callback_data=str(SWFM_CAT19_15))],
            [InlineKeyboardButton("User Management", callback_data=str(SWFM_CAT19_16))],
            [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    elif 'Other Problems' in data_text:
        chatid_telegram = update.callback_query.from_user.id

        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
        data_select = client.command(query)
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select}' where chatid_telegram = '{chatid_telegram}'"
        client.command(query)

        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None' WHERE chatid_telegram = '{chatid_telegram}'"
        client.command(query)
        query = update.callback_query
        query.answer()
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END_SWFM

def swfm_reqticket_pmsite(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    keyboard = [
        [InlineKeyboardButton("Failed Submission Ticket (Tiket Penyerahan)", callback_data=str(SWFM_CAT9_PMSITE_1))],
        [InlineKeyboardButton("Data Asset (Aset Data)", callback_data=str(SWFM_CAT9_PMSITE_2))],
        [InlineKeyboardButton("Follow-Up and Approval Process (Proses Tindak Lanjut dan Persetujuan)", callback_data=str(SWFM_CAT9_PMSITE_3))],
        [InlineKeyboardButton("Requests Permit (Permintaan Izin)", callback_data=str(SWFM_CAT9_PMSITE_4))],
        [InlineKeyboardButton("Care Process and Photos (Proses Perawatan dan Foto)", callback_data=str(SWFM_CAT9_PMSITE_5))],
        [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT9_PMSITE_6))],
        [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Pilih :",reply_markup=reply_markup)

def swfm_reqticket_pmgenset(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    keyboard = [
        [InlineKeyboardButton("Take Over Error (Ambil alih Kesalahan)", callback_data=str(SWFM_CAT9_PMGENSET_1))],
        [InlineKeyboardButton("Approval Issue (Masalah Persetujuan)", callback_data=str(SWFM_CAT9_PMGENSET_2))],
        [InlineKeyboardButton("Documentation Issue (Msalah Dokumentasi)", callback_data=str(SWFM_CAT9_PMGENSET_3))],
        [InlineKeyboardButton("Data Not Synchrone (Data Tidak sinkron)", callback_data=str(SWFM_CAT9_PMGENSET_4))],
        [InlineKeyboardButton("Data Asset (Aset Data)", callback_data=str(SWFM_CAT9_PMGENSET_5))],
        [InlineKeyboardButton("Application Error (Aplikasi Error)", callback_data=str(SWFM_CAT9_PMGENSET_6))],
        [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT9_PMGENSET_7))],
        [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Pilih :",reply_markup=reply_markup)

def swfm_reqticket_pmsampling(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    keyboard = [
        [InlineKeyboardButton("Cant Apporove (Tidak Bisa Menyutujui)", callback_data=str(SWFM_CAT9_PMSAMPLING_1))],
        [InlineKeyboardButton("Cant Synchrone (Tidak Dapat sinkron)", callback_data=str(SWFM_CAT9_PMSAMPLING_2))],
        [InlineKeyboardButton("Cancel Error (Kesalahan saat Pembatalan)", callback_data=str(SWFM_CAT9_PMSAMPLING_3))],
        [InlineKeyboardButton("Location Error Kesalahan Lokasi)", callback_data=str(SWFM_CAT9_PMSAMPLING_4))],
        [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(SWFM_CAT9_PMSAMPLING_5))],
        [InlineKeyboardButton("Kembali ke Menu Regional", callback_data=str(SWFM_REQTICKET))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Pilih :",reply_markup=reply_markup)


def swfm_reqticket_add2(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","").split(' (')[0]
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select} ➞ {data_text}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    time.sleep(2)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data_check = client.command(query)
    data_cat1 = str(data_check).split(' ➞ ')[0]
    data_cat2 = str(data_check).split(' ➞ ')[1]
    
    username = update.callback_query.from_user.username
    query = update.callback_query
    query.answer()
    # print(data_check)
    if 'Cant Check In' in data_check:
        channel_telegram = 'https://t.me/+uvk9c1Ry-VVjMjE1'
        query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', problem_title = 'User Management ➞ {data_cat1} ➞ {data_cat2}' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
            query = update.callback_query
            query.answer()
            message_id = query.message.message_id+1
            chat_id = update.callback_query.from_user.id
            bot_log.delete_message(chat_id,message_id)
            query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
            return END_SWFM
        except:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', problem_title = 'User Management ➞ {data_cat1} ➞ {data_cat2}' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
            query = update.callback_query
            query.answer()
            query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
            return END_SWFM
    else:
        channel_telegram = 'https://t.me/+uvk9c1Ry-VVjMjE1'
        query.edit_message_text(f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
            query = update.callback_query
            query.answer()
            # print(query)
            message_id = query.message.message_id+1
            chat_id = update.callback_query.from_user.id
            bot_log.delete_message(chat_id,message_id)
            query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
            return END_SWFM
        except:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None'  WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
            query = update.callback_query
            query.answer()
            query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
            return END_SWFM
        
# def clean_repeated_errors(s):
#     first_part = s.split('\n')[0]
#     print(f"first part = {first_part} s = {s}")
#     return first_part.strip()

def end_swfm(update: Update, _: CallbackContext) -> None:
    username = update.message.from_user.username
    chatid_telegram  = update.message.from_user.id 
    now = datetime.now() # current date and time
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    keterangan = update.message.text.replace(',',' ').replace(', ',' ').replace("'","").replace('"',"")
    ##Create Ticket
    characters = list(string.digits)
    length = 10
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    ticket = "SFM"+"".join(password)
    status = []
    query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data = client.command(query)
    val_check_ticket = data[3] == ticket
    problem_title = str(data[14]).split(' ➞ ')[0]
    status.append(val_check_ticket)
    if status[0] is False:
        data_select = problem_title
        data_select = data_select.split('\\n')[0]
        # print(data_select.split('\\n')[0])
        # data_select = 'Aplication Error'
        print(f"kalo muncul ga error ============================================================== {status[0]}  ====== STATUS {data_select}")
        if data_select == 'BPS Manual':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001940026674', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'KPI':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002076787818', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Mobile':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002042322394', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Preventive Maintenance':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002124230836', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Site Refference':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001616529958', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Teritory Operation':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002112027770', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Ticketing Handling':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002069743362', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'TS Manual':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002015471600', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'User Management':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001992461882', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Other Problems':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002107619822', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'CGL (IMBAS PETIR)':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002050195876', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'RH Visit':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002100716307', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Cant Check In':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002060389928', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Aplication Error':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002072488977', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'ANT':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002221992913', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Master Data Management':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002205131221', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Performance':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002229909079', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'TPAS':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002170544907', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'TANYA PROSES ?':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002153667955', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        

        time.sleep(2)
        query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data_select = client.command(query)
        query = f"INSERT INTO production.helpdesk_report_swfm select '{data_select[0]}','{data_select[1]}','{data_select[2]}','{data_select[3]}','{data_select[4]}','{data_select[5]}','{data_select[6]}','{data_select[7]}','{data_select[8]}','{data_select[9]}','{data_select[10]}','{data_select[11]}','{data_select[12]}','{data_select[13]}','{data_select[14]}','{data_select[15]}','{data_select[16]}','{data_select[17]}','{data_select[18]}','{data_select[19]}','{data_select[20]}','{data_select[21]}','{data_select[22]}','{data_select[23]}','{data_select[24]}','{data_select[25]}'"
        client.command(query)
        time.sleep(2)

        query = f"select ticket from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data = client.command(query)
        ticket_status = data
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM'"
        check_count = client.command(query)
        print(check_count)
        check_count = check_count == 0
        
        if check_count is True:
            username_expert = 'https://t.me/puang_ocha'
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
            data_select1 = client.command(query)
            data_select = str(data_select1).split(' ➞ ')[0]
            if data_select == 'BPS Manual':
                telegram_channel = "https://t.me/+JttjynPed2A1MDhl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_1}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
                
            elif data_select == 'KPI':
                print('ini')
                telegram_channel = "https://t.me/+MYbeWXAyR7pkNzNl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_2}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Mobile':
                telegram_channel = "https://t.me/+PWF9LCcQ8ZA2Njk1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_3}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Preventive Maintenance':
                telegram_channel = "https://t.me/+JKvY45t3n1wyNzll"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_4}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Site Refference':
                telegram_channel = "https://t.me/+xBnBSecb0xA4YjU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_5}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Teritory Operation':
                telegram_channel = "https://t.me/+NNM90kZNo604ZGI9"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_6}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Ticketing Handling':
                telegram_channel = "https://t.me/+277RJuKYOwkzMWM1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_7}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TS Manual':
                telegram_channel = "https://t.me/+b_QFKVjjY5EyYzll"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_8}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'User Management':
                telegram_channel = "https://t.me/+gCxokTxlwIU5YjA1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_9}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Other Problems':
                telegram_channel = "https://t.me/+uvk9c1Ry-VVjMjE1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_10}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'CGL (IMBAS PETIR)':
                telegram_channel = "https://t.me/+L6gs0AaeIu41N2U1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_11}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'RH Visit':
                telegram_channel = "https://t.me/+bXvaxWWE3tk5MGRl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_12}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Cant Check In':
                telegram_channel = "https://t.me/+ujAWzvI_cRxjNDg1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_13}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Aplication Error':
                telegram_channel = "https://t.me/+bFJfOpGpDd9jMzk9"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN) 
            elif data_select == 'ANT':
                telegram_channel = "https://t.me/+D5q3lNb5fTozYmU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Master Data Management':
                telegram_channel = "https://t.me/+RI4A3n6ElN9lODU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Performance':
                telegram_channel = "https://t.me/+KzT2jiWqdIliNzU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TPAS':
                telegram_channel = "https://t.me/+OSsJom_31ic3NzZl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TANYA PROSES ?':
                telegram_channel = "https://t.me/+mADjX8I8Ds42Y2Nl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            expert = []
            query = f"select expert from production.helpdesk_expert where application_name = 'SWFM'"
            data = client.command(query)
            expert.append(data)          
            expert = str(expert).replace('[','').replace(']','').replace("'",'').split('\\n')
            expert = expert[0]
            username_expert = 'https://t.me/{}'.format(expert)
            data_select = str(problem_title).split(' ➞ ')[0].split('/n')[0].split('\\n')[0]
            # data_select = 'Aplication Error'
            # print(data_select);
            # print(data_select)

            if data_select == 'BPS Manual':
                telegram_channel = "https://t.me/+JttjynPed2A1MDhl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_1}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    print('ada')
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    print('tidak ada')
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'KPI':
                telegram_channel = "https://t.me/+MYbeWXAyR7pkNzNl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_2}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Mobile':
                telegram_channel = "https://t.me/+PWF9LCcQ8ZA2Njk1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_3}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Preventive Maintenance':
                telegram_channel = "https://t.me/+JKvY45t3n1wyNzll"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_4}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Site Refference':
                telegram_channel = "https://t.me/+xBnBSecb0xA4YjU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_5}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Teritory Operation':
                telegram_channel = "https://t.me/+NNM90kZNo604ZGI9"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_6}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Ticketing Handling':
                telegram_channel = "https://t.me/+277RJuKYOwkzMWM1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_7}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TS Manual':
                telegram_channel = "https://t.me/+b_QFKVjjY5EyYzll"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_8}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'User Management':
                telegram_channel = "https://t.me/+gCxokTxlwIU5YjA1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_9}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Other Problems':
                telegram_channel = "https://t.me/+uvk9c1Ry-VVjMjE1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_10}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'CGL (IMBAS PETIR)':
                telegram_channel = "https://t.me/+L6gs0AaeIu41N2U1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_11}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'RH Visit':
                telegram_channel = "https://t.me/+bXvaxWWE3tk5MGRl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_12}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Cant Check In':
                telegram_channel = "https://t.me/+ujAWzvI_cRxjNDg1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_13}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Aplication Error':
                telegram_channel = "https://t.me/+bFJfOpGpDd9jMzk9"
                # proxies = {"https_proxy": "10.37.190.29:8080"}
                proxies = {"https_proxy": "10.59.105.206:8080"}
                first_part = data_select.split('\n')[0]
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                # print(f"ini DATA SELECT: {first_part}, \n https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}")
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                # print(telegram_channel)
                
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'ANT':
                telegram_channel = "https://t.me/+D5q3lNb5fTozYmU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Master Data Management':
                telegram_channel = "https://t.me/+RI4A3n6ElN9lODU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Performance':
                telegram_channel = "https://t.me/+KzT2jiWqdIliNzU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TPAS':
                telegram_channel = "https://t.me/+OSsJom_31ic3NzZl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TANYA PROSES ?':
                telegram_channel = "https://t.me/+mADjX8I8Ds42Y2Nl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            
            # INI LOG
            log_bot(update, 'SWFM')
            log_bot_success_swfm(update, '*Tiket* ➞ Telah Membuat Tiket 🎟')
    elif status[0] is True:
        characters = list(string.digits)
        length = 10
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        ticket = "SFM"+"".join(password)

        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
        data_select = client.command(query)
        data_select = str(data_select).split(' ➞ ')[0]
        if data_select == 'BPS Manual':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001940026674', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'KPI':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002076787818', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Mobile':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002042322394', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Preventive Maintenance':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002124230836', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Site Refference':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001616529958', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Teritory Operation':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002112027770', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Ticketing Handling':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002069743362', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'TS Manual':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002015471600', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'User Management':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1001992461882', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Other Problems':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002107619822', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'CGL (IMBAS PETIR)':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002050195876', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'RH Visit':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002100716307', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Cant Check In':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002060389928', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Aplication Error':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002072488977', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'ANT':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002221992913', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Master Data Management':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002205131221', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'Performance':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002229909079', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'TPAS':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002170544907', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        elif data_select == 'TANYA PROSES ?':
            query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = '-1002153667955', ticket = '{ticket}', problem_summary = '{keterangan}', open_ticket_date = '{date_time}', category = 'SWFM', status = 'open', fcaps = 'FAULT' WHERE chatid_telegram = '{chatid_telegram}'"
            client.command(query)
        

        time.sleep(2)
        query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data_select = client.command(query)
        query = f"INSERT INTO production.helpdesk_report_swfm select '{data_select[0]}','{data_select[1]}','{data_select[2]}','{data_select[3]}','{data_select[4]}','{data_select[5]}','{data_select[6]}','{data_select[7]}','{data_select[8]}','{data_select[9]}','{data_select[10]}','{data_select[11]}','{data_select[12]}','{data_select[13]}','{data_select[14]}','{data_select[15]}','{data_select[16]}','{data_select[17]}','{data_select[18]}','{data_select[19]}','{data_select[20]}','{data_select[21]}','{data_select[22]}','{data_select[23]}','{data_select[24]}','{data_select[25]}'"
        client.command(query)
        time.sleep(2)

        query = f"select ticket from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
        data = client.command(query)
        telegram_channel = "https://t.me/+uvk9c1Ry-VVjMjE1"
        ticket_status = data
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM'"
        check_count = client.command(query)
        check_count = check_count == 0
        if check_count is True:
            username_expert = 'https://t.me/puang_ocha'
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
            data_select = client.command(query)
            data_select = str(data_select).split(' ➞ ')[0]
            if data_select == 'BPS Manual':
                telegram_channel = "https://t.me/+JttjynPed2A1MDhl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_1}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
                
            elif data_select == 'KPI':
                telegram_channel = "https://t.me/+MYbeWXAyR7pkNzNl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_2}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Mobile':
                telegram_channel = "https://t.me/+PWF9LCcQ8ZA2Njk1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_3}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Preventive Maintenance':
                telegram_channel = "https://t.me/+JKvY45t3n1wyNzll"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_4}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Site Refference':
                telegram_channel = "https://t.me/+xBnBSecb0xA4YjU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_5}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Teritory Operation':
                telegram_channel = "https://t.me/+NNM90kZNo604ZGI9"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_6}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Ticketing Handling':
                telegram_channel = "https://t.me/+277RJuKYOwkzMWM1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_7}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TS Manual':
                telegram_channel = "https://t.me/+b_QFKVjjY5EyYzll"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_8}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'User Management':
                telegram_channel = "https://t.me/+gCxokTxlwIU5YjA1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_9}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Other Problems':
                telegram_channel = "https://t.me/+uvk9c1Ry-VVjMjE1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_10}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'CGL (IMBAS PETIR)':
                telegram_channel = "https://t.me/+L6gs0AaeIu41N2U1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_11}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'RH Visit':
                telegram_channel = "https://t.me/+bXvaxWWE3tk5MGRl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_12}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Cant Check In':
                telegram_channel = "https://t.me/+ujAWzvI_cRxjNDg1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_13}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Aplication Error':
                telegram_channel = "https://t.me/+bFJfOpGpDd9jMzk9"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'ANT':
                telegram_channel = "https://t.me/+D5q3lNb5fTozYmU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Master Data Management':
                telegram_channel = "https://t.me/+RI4A3n6ElN9lODU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Performance':
                telegram_channel = "https://t.me/+KzT2jiWqdIliNzU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TPAS':
                telegram_channel = "https://t.me/+OSsJom_31ic3NzZl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TANYA PROSES ?':
                telegram_channel = "https://t.me/+mADjX8I8Ds42Y2Nl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            expert = []
            query = f"select expert from production.helpdesk_expert where application_name = 'SWFM'"
            data = client.command(query)
            expert.append(data)          
            expert = str(expert).replace('[','').replace(']','').replace("'",'').split('\\n')
            expert = expert[0]
            username_expert = 'https://t.me/{}'.format(expert)

            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
            data_select = client.command(query)
            data_select = str(data_select).split(' ➞ ')[0]
            if data_select == 'BPS Manual':
                telegram_channel = "https://t.me/+JttjynPed2A1MDhl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_1}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
                
            elif data_select == 'KPI':
                print('testdkjfnksdjfnjsdfjsdfjsdfsdfksdfkjsnfafinskfjnskjfnsd==================')
                telegram_channel = "https://t.me/+z6RZqhUr-ws3OWRl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_2}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Mobile':
                telegram_channel = "https://t.me/+PWF9LCcQ8ZA2Njk1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_3}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Preventive Maintenance':
                telegram_channel = "https://t.me/+JKvY45t3n1wyNzll"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_4}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Site Refference':
                telegram_channel = "https://t.me/+xBnBSecb0xA4YjU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_5}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Teritory Operation':
                telegram_channel = "https://t.me/+NNM90kZNo604ZGI9"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_6}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Ticketing Handling':
                telegram_channel = "https://t.me/+277RJuKYOwkzMWM1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_7}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TS Manual':
                telegram_channel = "https://t.me/+b_QFKVjjY5EyYzll"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_8}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'User Management':
                telegram_channel = "https://t.me/+gCxokTxlwIU5YjA1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_9}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Other Problems':
                telegram_channel = "https://t.me/+uvk9c1Ry-VVjMjE1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_10}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'CGL (IMBAS PETIR)':
                telegram_channel = "https://t.me/+L6gs0AaeIu41N2U1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_11}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'RH Visit':
                telegram_channel = "https://t.me/+bXvaxWWE3tk5MGRl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_12}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Cant Check In':
                telegram_channel = "https://t.me/+ujAWzvI_cRxjNDg1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_13}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Aplication Error':
                telegram_channel = "https://t.me/+bFJfOpGpDd9jMzk9"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'ANT':
                telegram_channel = "https://t.me/+D5q3lNb5fTozYmU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Master Data Management':
                telegram_channel = "https://t.me/+RI4A3n6ElN9lODU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'Performance':
                telegram_channel = "https://t.me/+KzT2jiWqdIliNzU1"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TPAS':
                telegram_channel = "https://t.me/+OSsJom_31ic3NzZl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
            elif data_select == 'TANYA PROSES ?':
                telegram_channel = "https://t.me/+mADjX8I8Ds42Y2Nl"
                proxies = {"https_proxy": "10.37.190.29:8080"}
                url = f'https://api.telegram.org/bot{token_bot}/getChatMember?chat_id={chatid_14}&user_id={chatid_telegram}'
                res = requests.get(url=url, proxies=proxies)
                data = res.json()
                if data['ok']:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
                    buttons = [[button1]]
                    keyboard = InlineKeyboardMarkup(buttons)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
                else:
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*\n\n{telegram_channel}',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot(update, 'SWFM')
        log_bot_success_swfm(update, '*Tiket* ➞ Telah Membuat Tiket 🎟')
        
    return ConversationHandler.END

def swfm_expert(update: Update, _: CallbackContext) -> None:
    try:
        keyboard = [
            [InlineKeyboardButton("Registrasi >>", callback_data=str(REG_EXPERT_SWFM))],
            [InlineKeyboardButton("Hapus >>", callback_data=str(DEL_EXPERT_SWFM))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text="Anda memilih : *Tim Ahli*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
    except:
        keyboard = [
            [InlineKeyboardButton("Registrasi", callback_data=str(REG_EXPERT_SWFM))],
            [InlineKeyboardButton("Hapus", callback_data=str(DEL_EXPERT_SWFM))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Anda memilih : *Tim Ahli*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
def reg_expert_swfm(update: Update, _: CallbackContext) -> None:
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM'"
    count_data = client.command(query)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda memilih: *Registrasi*",parse_mode=telegram.ParseMode.MARKDOWN)
    if count_data == 0 or count_data == 1 or count_data == 2 or count_data == 3 or count_data == 4 or count_data == 5 or count_data == 6 or count_data == 7 or count_data == 8 or count_data == 9:
        query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 3\nKlik /cancel untuk membatalkan")
        return END_REG_EXPERT_SWFM
    elif count_data == 10:
        query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 2\nKlik /cancel untuk membatalkan")
        return END_REG_EXPERT_SWFM
    elif count_data == 11:
        query.message.reply_text("Ketik username ID telegram tanpa @ dan gunakan spasi setiap user jika lebih dari satu. Maksimum 1\nKlik /cancel untuk membatalkan")
        return END_REG_EXPERT_SWFM
    elif count_data == 12 or count_data == 13:
        query.message.reply_text("Registrasi Tim Ahli telah mencapai maksimum\nKlik /menu")
        log_bot_success_inline_swfm(update, '*Tim Ahli (Registrasi)* ➞ Registrasi telah mencapai maksimum')
        return ConversationHandler.END
def end_reg_expert_swfm(update: Update, _: CallbackContext) -> None:
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM'"
    count_data = client.command(query)
    parameter_user =  update.message.text.split()
    count_user =  len(update.message.text.split())
    if count_data == 0 or count_data == 1 or count_data == 2 or count_data == 3 or count_data == 4 or count_data == 5 or count_data == 6 or count_data == 7:
        if count_user == 1:
            query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[0]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
        elif count_user == 2:
            query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[0]}'"
            client.command(query)
            query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[1]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
        elif count_user == 3:
            query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[0]}'"
            client.command(query)
            query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[1]}'"
            client.command(query)
            query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[2]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
        else:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 3\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 3')
    elif count_data == 10:
        try:
            if count_user == 1:
                query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[0]}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
                log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            elif count_user == 2:
                query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[0]}'"
                client.command(query)
                query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[1]}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
                log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            else:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 2\nKlik /menu")
                log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 2')
        except:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 2\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 2')
    elif count_data == 11:
        try:
            if count_user == 1:
                query = f"INSERT INTO production.helpdesk_expert select 'SWFM', '{parameter_user[0]}'"
                client.command(query)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("✅ Berhasil Registrasi\nKlik /menu")
                log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Registrasi Sukses')
            else:
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 1\nKlik /menu")
                log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 1')
        except:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Registrasi gagal, ketik username ID Telegram Maksimum 1\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 1')
    elif count_data == 12 or count_data == 13:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("Registrasi gagal, Username ID telah mencapai maksimum 10\nKlik /menu")
        log_bot_success_swfm(update, '*Tim Ahli (Registrasi)* ➞ Maximum Registrasi Username ID Telegram 10')
    return ConversationHandler.END

def del_expert_swfm(update: Update, _: CallbackContext) -> None:
    return_text = get_del_fm_swfm()
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Anda memilih: *Hapus*",parse_mode=telegram.ParseMode.MARKDOWN)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM'"
    check_status = client.command(query)
    check_status = check_status == 0
    query = update.callback_query
    query.answer()
    if check_status is True:
        query.message.reply_text("Username ID telegram tidak ditemukan\nKlik /menu", parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_swfm(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        return ConversationHandler.END
    elif check_status is False:
        for cmdOUT in splitting(return_text):
            query.message.reply_text(cmdOUT, disable_web_page_preview=True)
        query.message.reply_text("Hapus username ID telegram dan gunakan spasi setiap user jika lebih dari satu, maksimum 3 user\nKlik /cancel untuk membatalkan")
        return END_DEL_EXPERT_SWFM
def get_del_fm_swfm():
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    text = ''
    text += 'Expert Aktif :'
    text += '\n'
    query = f"select expert from production.helpdesk_expert where application_name = 'SWFM'"
    data = client.command(query)
    data_list = str(data).split('\\n')
    data_list = str(data_list).replace("['","").replace("']","").split('\\n')
    for data in data_list:
        check_username = f"├ {data}"
        text += check_username
        text += '\n'
    text += '\n'
    return text
def end_del_expert_swfm(update: Update, _: CallbackContext) -> None:
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    parameter_user =  update.message.text.split()
    count_user =  len(update.message.text.split())
    if count_user == 1:
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM' AND expert = '{parameter_user[0]}'"
        check_status = client.command(query)
        check_status_1 = check_status == 0
        if check_status_1 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        else:
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'SWFM' AND expert = '{parameter_user[0]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil dihapus\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Hapus)* ➞ Berhasil Hapus')
    elif count_user == 2:
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM' AND expert = '{parameter_user[0]}'"
        check_status = client.command(query)
        check_status_1 = check_status == 0
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM' AND expert = '{parameter_user[1]}'"
        check_status = client.command(query)
        check_status_2 = check_status == 0
        if check_status_1 is True and check_status_2 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        else:
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'SWFM' AND expert = '{parameter_user[0]}'"
            client.command(query)
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'SWFM' AND expert = '{parameter_user[1]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil dihapus\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Hapus)* ➞ Berhasil Hapus')
    elif count_user == 3:
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM' AND expert = '{parameter_user[0]}'"
        check_status = client.command(query)
        check_status_1 = check_status == 0
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM' AND expert = '{parameter_user[1]}'"
        check_status = client.command(query)
        check_status_2 = check_status == 0
        query = f"select count(*) as `count` from production.helpdesk_expert where application_name = 'SWFM' AND expert = '{parameter_user[2]}'"
        check_status = client.command(query)
        check_status_3 = check_status == 0
        if check_status_1 is True and check_status_2 is True and check_status_3 is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
        else:
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'SWFM' AND expert = '{parameter_user[0]}'"
            client.command(query)
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'SWFM' AND expert = '{parameter_user[1]}'"
            client.command(query)
            query = f"ALTER TABLE production.helpdesk_expert delete where application_name = 'SWFM' AND expert = '{parameter_user[2]}'"
            client.command(query)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text("✅ Berhasil dihapus\nKlik /menu")
            log_bot_success_swfm(update, '*Tim Ahli (Hapus)* ➞ Berhasil Hapus')
    else:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("Username ID telegram yang dihapus tidak ditemukan")
        log_bot_success_swfm(update, '*Tim Ahli (Hapus)* ➞ Username ID Telegram tidak ditemukan')
    return ConversationHandler.END

def swfm_myticket(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id 
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)

    query = update.callback_query
    query.answer()
    position = data == 'admin'
    if position is True: ##ADMIN
        query.edit_message_text(f"Anda memilih : *Status Laporan (Admin)*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text(text="Silahkan masukkan Nomor Tiket\nContoh : SFMXXXXXXXXXXX\nKlik /cancel untuk membatalkan",parse_mode=telegram.ParseMode.MARKDOWN)
    elif position is False: ##USER
        query.edit_message_text(f"Anda memilih : *Status Laporan*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text(text="Silahkan masukkan Nomor Tiket\nContoh : SFMXXXXXXXXXXX\nKlik /cancel untuk membatalkan",parse_mode=telegram.ParseMode.MARKDOWN)
    return SWFM_MYTICKET_ERROR

def swfm_myticket_error(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(f"Harap menunggu dalam beberapa detik...")
    ticket_check = update.message.text
    chatid_telegram = update.message.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select position from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' LIMIT 1"
    data = client.command(query)
    position = data == 'admin'
    if position is True: ##ADMIN
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
            check_status = client.command(query)
            check_status = check_status == 0
            if check_status is True:
                update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
                log_bot_success_swfm(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
                return ConversationHandler.END
            elif check_status is False:
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select status from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                data_check = client.command(query)
                if data_check == 'closed':
                    update.message.reply_text(f"Maaf Ticket sudah closed\nKlik /menu")
                    log_bot_success_swfm(update, '*Status Laporan* ➞ Ticket sudah di closed')
                    return ConversationHandler.END
                elif data_check == 'open':
                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
                    client.command(query)
                    query = f"INSERT INTO production.action_swfm select '{chatid_telegram}','{ticket_check}','None','None','None'"
                    client.command(query)
                    query = f"select * from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                    data = client.command(query)
                    full_name = str(data[0]).title()
                    requests = 'https://t.me/{}'.format(data[1])
                    no_hp = data[3]
                    ticket = data[11]
                    regional = str(data[13])
                    problem_note = str(data[14])
                    problem__ = str(data[15]).replace('\\n',' ')
                    app = data[17]
                    date = str(data[18]).replace('-',' ')
                    update.message.reply_text(f'Creation Date : {date}\nApplication : #{app}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                    
                    keyboard = [
                        [InlineKeyboardButton("Iya", callback_data=str(SWFM_MYTICKET_PROCESS_END))],
                        [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Pilih Iya jika benar :", reply_markup=reply_markup)
                    return SWFM_MYTICKET_PROCESS
        except:
            update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
            log_bot_success_swfm(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
            return ConversationHandler.END
    elif position is False: ##USER
        try:
            client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            query = f"select count(*) as `count` from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and ticket = '{ticket_check}'"
            check_status = client.command(query)
            check_status = check_status == 0
            if check_status is True:
                update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
                log_bot_success_swfm(update, '*Status Laporan (Admin)* ➞ Tidak memiliki laporan')
                return ConversationHandler.END
            elif check_status is False:
                client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                query = f"select status from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                data_check = client.command(query)
                if data_check == 'closed':
                    update.message.reply_text(f"Maaf Ticket sudah closed\nKlik /menu")
                    log_bot_success_swfm(update, '*Status Laporan* ➞ Ticket sudah di closed')
                    return ConversationHandler.END
                elif data_check == 'open':
                    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
                    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
                    client.command(query)
                    query = f"INSERT INTO production.action_swfm select '{chatid_telegram}','{ticket_check}','None','None','None'"
                    client.command(query)
                    query = f"select * from production.helpdesk_report_swfm where ticket = '{ticket_check}'"
                    data = client.command(query)
                    full_name = str(data[0]).title()
                    requests = 'https://t.me/{}'.format(data[1])
                    no_hp = data[3]
                    ticket = data[11]
                    regional = str(data[13])
                    problem_note = str(data[14])
                    problem__ = str(data[15]).replace('\\n',' ')
                    app = data[17]
                    date = str(data[18]).replace('-',' ')
                    update.message.reply_text(f'Creation Date : {date}\nApplication : #{app}\nTicket : #{ticket}\nSummary Case : *{problem_note} ↔️ ({problem__})*\nRequestor : [{full_name}]({requests})\nNo HP : {no_hp}\nRegional : {regional}',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                    
                    keyboard = [
                        [InlineKeyboardButton("Iya", callback_data=str(SWFM_MYTICKET_PROCESS_END))],
                        [InlineKeyboardButton("Tidak", callback_data=str(CANCEL_HOME))],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                    update.message.reply_text("Pilih Iya jika benar :", reply_markup=reply_markup)
                    return SWFM_MYTICKET_PROCESS
        except:
            update.message.reply_text(f"Maaf tiket anda salah\nKlik /menu")
            log_bot_success_swfm(update, '*Status Laporan* ➞ Tidak memiliki laporan')
            return ConversationHandler.END

def swfm_myticket_process_end(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text('Anda memilih : *Iya*',parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text("Penjelasan Resolution : \n*By System :* Tindakan diselesaikan otomatis oleh sistem\n*By SPV :* Tindakan ditindaklanjutin oleh SPV, mempertimbangkan masalah dan memberikan solusi kepada TIM\n*By Helpdesk :* Tindakan ditangani oleh TIM dukungan yang bertugas menangani masalah\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
    keyboard = [
        [InlineKeyboardButton("By System", callback_data=str(SWFM_MYTICKET_ACTION_MENU1))],
        [InlineKeyboardButton("By SPV", callback_data=str(SWFM_MYTICKET_ACTION_MENU2))],
        [InlineKeyboardButton("By Helpdesk", callback_data=str(SWFM_MYTICKET_ACTION_MENU3))],
        [InlineKeyboardButton("Other Problems", callback_data=str(SWFM_MYTICKET_ACTION_MENU4))],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Klik menu dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)

def swfm_myticket_action_menu(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            error_from = str(data['text']).split(" - ")[0]
    query.edit_message_text(text=f"Anda memilih : *{error_from}*",parse_mode=telegram.ParseMode.MARKDOWN)
    chatid_telegram = update.callback_query.from_user.id 
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.action_swfm update error_from = '{error_from}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    
    query = f"select problem_title, problem_summary from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    data = client.command(query)
    data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    query = update.callback_query
    query.answer()
    message_id = query.message.message_id-1
    chat_id = update.callback_query.from_user.id
    bot_log.delete_message(chat_id,message_id)
    for data in data_list:
        data = str(data).split(', ')
        data_problem = data[0].split(' ➞ ')[0]
        if data_problem == 'BPS Manual':
            keyboard = [
                [InlineKeyboardButton("Bugs", callback_data=str(SWFM_MYTICKET_ACTION_CAT1))],
                [InlineKeyboardButton("Data", callback_data=str(SWFM_MYTICKET_ACTION_CAT2))],
                [InlineKeyboardButton("UI/UX", callback_data=str(SWFM_MYTICKET_ACTION_CAT3))],
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT4))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        elif data_problem == 'KPI':
            keyboard = [
                [InlineKeyboardButton("Data", callback_data=str(SWFM_MYTICKET_ACTION_CAT5))],
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT6))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        elif data_problem == 'Mobile':
            keyboard = [
                [InlineKeyboardButton("Bugs", callback_data=str(SWFM_MYTICKET_ACTION_CAT7))],
                [InlineKeyboardButton("Data", callback_data=str(SWFM_MYTICKET_ACTION_CAT8))],
                [InlineKeyboardButton("New Requiement", callback_data=str(SWFM_MYTICKET_ACTION_CAT9))],
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT10))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        elif data_problem == 'Preventive Maintenance':
            keyboard = [
                [InlineKeyboardButton("Bugs", callback_data=str(SWFM_MYTICKET_ACTION_CAT11))],
                [InlineKeyboardButton("Data", callback_data=str(SWFM_MYTICKET_ACTION_CAT12))],
                [InlineKeyboardButton("New Requiement", callback_data=str(SWFM_MYTICKET_ACTION_CAT13))],
                [InlineKeyboardButton("Workflow", callback_data=str(SWFM_MYTICKET_ACTION_CAT14))],
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT15))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        elif data_problem == 'Site Refference':
            keyboard = [
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT16))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        elif data_problem == 'Teritory Operation':
            keyboard = [
                [InlineKeyboardButton("Data", callback_data=str(SWFM_MYTICKET_ACTION_CAT17))],
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT18))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        elif data_problem == 'Ticketing Handling':
            keyboard = [
                [InlineKeyboardButton("Bugs", callback_data=str(SWFM_MYTICKET_ACTION_CAT19))],
                [InlineKeyboardButton("Data", callback_data=str(SWFM_MYTICKET_ACTION_CAT20))],
                [InlineKeyboardButton("UI/UX", callback_data=str(SWFM_MYTICKET_ACTION_CAT21))],
                [InlineKeyboardButton("New Requiement", callback_data=str(SWFM_MYTICKET_ACTION_CAT22))],
                [InlineKeyboardButton("Technical Issue", callback_data=str(SWFM_MYTICKET_ACTION_CAT23))],
                [InlineKeyboardButton("Workflow", callback_data=str(SWFM_MYTICKET_ACTION_CAT24))],
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT25))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        elif data_problem == 'TS Manual':
            keyboard = [
                [InlineKeyboardButton("Bugs", callback_data=str(SWFM_MYTICKET_ACTION_CAT26))],
                [InlineKeyboardButton("New Requiement", callback_data=str(SWFM_MYTICKET_ACTION_CAT27))],
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT28))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        elif data_problem == 'User Management':
            keyboard = [
                [InlineKeyboardButton("New Requiement", callback_data=str(SWFM_MYTICKET_ACTION_CAT29))],
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT30))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)
        else:
            keyboard = [
                [InlineKeyboardButton("Others", callback_data=str(SWFM_MYTICKET_ACTION_CAT31))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Klik tombol dibawah ini :\n\nketik /cancel untuk membatalkan", reply_markup=reply_markup)

def swfm_myticket_action_cat(update: Update, _: CallbackContext) -> None:   
    chatid_telegram = update.callback_query.from_user.id 
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            error_cat = str(data['text']).replace(" -","")
    query.edit_message_text(text=f"Anda memilih : *{error_cat}*",parse_mode=telegram.ParseMode.MARKDOWN)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.action_swfm update category = '{error_cat}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    query = f"select * from production.helpdesk_expert he where application_name ='SWFM'"
    data = client.command(query)
    data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    query = update.callback_query
    query.answer()
    try:
        datas = []
        for data in data_list:
            data = str(data).split(', ')
            data = f"{data[1]}"
            datas.append([data])
        datas.append(['-'])
        if datas == []:
            reply_keyboard = [
                ['-']
                ]
            query.message.reply_text('Tidak ada Tim Ahli, Pilih tombol dibawah ini "-" :\nketik /cancel untuk membatalkan.',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,selective=True,resize_keyboard=True),parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            reply_keyboard = datas
            query.message.reply_text('Pilih  tombol dibawah ini\nketik /cancel untuk membatalkan',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard= True, selective=True,resize_keyboard=True))
            
    except IndexError:
        reply_keyboard = [
            ['-']
            ]
        query.message.reply_text('Tidak ada Tim Ahli, Pilih tombol dibawah ini "-" :\nketik /cancel untuk membatalkan.',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,selective=True,resize_keyboard=True),parse_mode=telegram.ParseMode.MARKDOWN)
    return SWFM_MYTICKET_CLOSED


def swfm_myticket_closed(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id
    handle_by = update.message.text
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.action_swfm update handle_by = '{handle_by}' where chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text(text="Masukkan resolution action :",parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    return SWFM_MYTICKET_CLOSED_END
def swfm_myticket_closed_end(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id
    full_name_closed = update.message.from_user.full_name
    now = datetime.now()
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    parameter = update.message.text.replace(',','.')
    update.message.reply_text("Proses closed tiket ...")
    time.sleep(3)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select * from production.action_swfm where chatid_telegram = '{chatid_telegram}'"
    data_select = client.command(query)
    data_list = str(data_select).replace("[","").replace("]","").replace("'","").replace('±','').replace('+','').replace("\\\\n",' ').split('\\n')
    for data in data_list:
        data = str(data).split(', ')
        ticket_log_swfm = data[1]
        error_from_swfm = data[2]
        action_cat_swfm = data[4]
        handle_by_swfm = data[3]

    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.helpdesk_report_swfm update action_menu = '{error_from_swfm}', action_category = '{action_cat_swfm}', action_handle_by = '{handle_by_swfm}', action_resolution = '{parameter}', close_ticket_date = '{date_time}', status = 'closed' WHERE ticket = '{ticket_log_swfm}'"
    client.command(query)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select username_telegram,fullname_telegram from production.helpdesk_report_swfm where ticket = '{ticket_log_swfm}'"
    data = client.command(query)
    requests = 'https://t.me/{}'.format(data[0])
    full_name = str(data[1]).title()
    update.message.reply_text(f"✅ Tiket [{full_name}]({requests}) telah closed\nKlik /menu", parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select username_telegram, fullname_telegram, channel_chatid, open_ticket_date, close_ticket_date, chatid_telegram from production.helpdesk_report_swfm where ticket = '{ticket_log_swfm}'"
    check_ticket = client.command(query)
    data_list = str(check_ticket).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    x = []
    for data in data_list:
        data = str(data).split(', ')
        open_str = f'{data[3]}, {data[4]}'
        closed_str = f'{data[5]}, {data[6]}'
        full_name = data[1]
        # Parsing string menjadi objek datetime
        open_date = datetime.strptime(open_str, "%d-%B-%Y, %H:%M:%S WIB")
        closed_date = datetime.strptime(closed_str, "%d-%B-%Y, %H:%M:%S WIB")
        # Menghitung selisih waktu
        selisih_waktu = closed_date - open_date
        # Mengambil selisih dalam bentuk hari
        day_difference = selisih_waktu

        ##grup
        bot_log.send_message(chat_id=data[2],text=f'✅ Tiket *{ticket_log_swfm}* dari [{data[1]}]({data[0]}) telah *Terclosed* oleh {full_name_closed} dengan durasi → *{day_difference}*',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        ##user
        bot_log.send_message(chat_id=data[7],text=f'✅ Tiket anda *{ticket_log_swfm}* telah *Terclosed* oleh Admin HD {full_name_closed} dengan durasi → *{day_difference}*',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        log_bot_success_swfm(update, '*Tiket* ➞ Closed Tiket ✅')
    #HAPUS
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"ALTER TABLE production.action_swfm  DELETE WHERE chatid_telegram = '{chatid_telegram}'"
    client.command(query)
    return ConversationHandler.END

def swfm_broadcast(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *Broadcast Pesan*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Silahkan masukkan pesan anda",parse_mode=telegram.ParseMode.MARKDOWN)
    return SWFM_BROADCAST_END

def swfm_broadcast_end(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.message.from_user.id
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select registered_swfm, registered_ioms, registered_ipas from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    check_data = client.command(query)
    check_swfm = check_data[0]
    check_ioms = check_data[1]
    check_ipas = check_data[2]
    if check_swfm == 'True':
        if os.path.exists("/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_swfm.txt"):
            os.remove("/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_swfm.txt")
            time.sleep(1)
            data_text = update.message.text.replace('_','').replace('*','')
            log_bot = open('/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_swfm.txt','a')
            log_bot.write("{}".format(data_text))
            log_bot.close()
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Terima Kasih anda telah membuat pesan siaran, sedang dalam proses pengiriman dan membutuhkan waktu sekitar 1,5 Jam, dikarenakan banyaknya user yang telah terdaftar di BOT. Terima kasih.',parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            print("The file does not exist")
            time.sleep(1)
            data_text = update.message.text.replace('_','').replace('*','')
            log_bot = open('/home/dimas/baru/helpdeskbot_v2/broadcast_syantic/log/bc_syantic_swfm.txt','a')
            log_bot.write("{}".format(data_text))
            log_bot.close()
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Terima Kasih anda telah membuat pesan siaran, sedang dalam proses pengiriman dan membutuhkan waktu sekitar 1,5 Jam, dikarenakan banyaknya user yang telah terdaftar di BOT. Terima kasih.',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_swfm(update, '*Broadcast Pesan* ➞ Pesan Siaran')
        return ConversationHandler.END

def swfm_makeadmin(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Anda memilih : *Jadikan Admin*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Silahkan masukkan Username Telegram",parse_mode=telegram.ParseMode.MARKDOWN)
    return SWFM_MAKEADMIN_END

def swfm_makeadmin_end(update: Update, _: CallbackContext) -> None:
    username_telegram = update.message.text
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_bot_swfm where username_telegram = '{username_telegram}' and position = 'admin'"
    check_data = client.command(query)
    check_status = check_data == 0
    if check_status is True:
        query = f"ALTER TABLE production.helpdesk_bot_swfm update position = 'admin' where username_telegram = '{username_telegram}'"
        client.command(query)
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f'Username Telegram *{username_telegram}* sukses dijadikan Admin',parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f'Username tersebut sudah menjadi Admin',parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_swfm(update, '*Jadikan Admin* ➞ Username Telegram')
    return ConversationHandler.END

def swfm_bantuan(update: Update, _: CallbackContext) -> None: 
    try:
        keyboard = [
            [InlineKeyboardButton("Kapan Backup Power System (BPS Manual) digunakan?", callback_data=str(SWFM_BANTUAN_1))],
            [InlineKeyboardButton("Apa yang terdapat dalam Menu (Preventive Maintenance?)", callback_data=str(SWFM_BANTUAN_2))],
            [InlineKeyboardButton("Bagaimana cara kerja (Ticketing Handling)?", callback_data=str(SWFM_BANTUAN_3))],
            [InlineKeyboardButton("Mengapa Technical Support (TS Manual) menjadi relevan jika tidak ada alarm yang muncul di INAP?", callback_data=str(SWFM_BANTUAN_4))],
            [InlineKeyboardButton("SWFM WEB (Url Link Web)", callback_data=str(SWFM_BANTUAN_5))],
            [InlineKeyboardButton("SWFM Mobile (Url Link Download Aplikasi)", callback_data=str(SWFM_BANTUAN_6))],
            [InlineKeyboardButton("Modul SPV TO", callback_data=str(SWFM_BANTUAN_7))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        message_id = query.message.message_id+1
        chat_id = update.callback_query.from_user.id
        bot_log.delete_message(chat_id,message_id)
        query.edit_message_text(text="Anda memilih : *Pusat Bantuan*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih rekomendasi artikel :",reply_markup=reply_markup)
    except:
        keyboard = [
            [InlineKeyboardButton("Kapan Backup Power System (BPS Manual) digunakan?", callback_data=str(SWFM_BANTUAN_1))],
            [InlineKeyboardButton("Apa yang terdapat dalam Menu (Preventive Maintenance?)", callback_data=str(SWFM_BANTUAN_2))],
            [InlineKeyboardButton("Bagaimana cara kerja (Ticketing Handling)?", callback_data=str(SWFM_BANTUAN_3))],
            [InlineKeyboardButton("Mengapa Technical Support (TS Manual) menjadi relevan jika tidak ada alarm yang muncul di INAP?", callback_data=str(SWFM_BANTUAN_4))],
            [InlineKeyboardButton("SWFM WEB (Url Link Web)", callback_data=str(SWFM_BANTUAN_5))],
            [InlineKeyboardButton("SWFM Mobile (Url Link Download Aplikasi)", callback_data=str(SWFM_BANTUAN_6))],
            [InlineKeyboardButton("Modul SPV TO", callback_data=str(SWFM_BANTUAN_7))],
            [InlineKeyboardButton("Kembali", callback_data=str(MENU_UTAMA))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Anda memilih : *Pusat Bantuan*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih rekomendasi artikel :",reply_markup=reply_markup)

def swfm_bantuan_end(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'Kapan Backup Power System (BPS Manual) digunakan?' in data_text:
        query.message.reply_text("https://nurdjatis-organization.gitbook.io/smart-work-force-management/ticketing-handling/bps-manual",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text="Berikut adalah Pusat Bantuan (BPS Manual), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_swfm(update, '*Pusat Bantuan* ➞ Bantuan')
        return ConversationHandler.END
    elif 'Apa yang terdapat dalam Menu (Preventive Maintenance)?' in data_text:
        query.message.reply_text("https://nurdjatis-organization.gitbook.io/smart-work-force-management/preventive-maintenance/pm-schedule-planning",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text="Berikut adalah Pusat Bantuan (Preventive Maintenance), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_swfm(update, '*Pusat Bantuan* ➞ Bantuan')
        return ConversationHandler.END
    elif 'Bagaimana cara kerja (Ticketing Handling)?' in data_text:
        query.message.reply_text("https://nurdjatis-organization.gitbook.io/smart-work-force-management/ticketing-handling/poc-perubahan-severity",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text="Berikut adalah Pusat Bantuan (Ticketing Handling), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_swfm(update, '*Pusat Bantuan* ➞ Bantuan')
        return ConversationHandler.END
    elif 'Mengapa Technical Support (TS Manual) menjadi relevan jika tidak ada alarm yang muncul di INAP?' in data_text:
        query.message.reply_text("https://nurdjatis-organization.gitbook.io/smart-work-force-management/ticketing-handling/ts-manual",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text="Berikut adalah Pusat Bantuan (TS Manual), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_swfm(update, '*Pusat Bantuan* ➞ Bantuan')
        return ConversationHandler.END
    elif 'SWFM WEB (Url Link Web)' in data_text:
        query.message.reply_text("https://smartwfm.network.telkomsel.co.id/Login",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text="Berikut adalah URL WEB SWFM, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_swfm(update, '*Pusat Bantuan* ➞ Bantuan')
        return ConversationHandler.END
    elif 'SWFM Mobile (Url Link Download Aplikasi)' in data_text:
        query.message.reply_text("https://tia.telkomsel.co.id/NativeAppBuilder/App?AppKey=fdb3ff36-032d-424a-97d5-3539184520b0",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text="Berikut adalah link Download Aplikasi SWFM, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_swfm(update, '*Pusat Bantuan* ➞ Bantuan')
        return ConversationHandler.END
    elif 'Modul SPV TO' in data_text:
        keyboard = [
            [InlineKeyboardButton("Site List Management", callback_data=str(SWFM_BANTUAN_SPV_1))],
            [InlineKeyboardButton("PM Schedule Planning", callback_data=str(SWFM_BANTUAN_SPV_2))],
            [InlineKeyboardButton("PM Site", callback_data=str(SWFM_BANTUAN_SPV_3))],
            [InlineKeyboardButton("PM Genset", callback_data=str(SWFM_BANTUAN_SPV_4))],
            [InlineKeyboardButton("Fault Center", callback_data=str(SWFM_BANTUAN_SPV_5))],
            [InlineKeyboardButton("Fault Center SWFM", callback_data=str(SWFM_BANTUAN_SPV_6))],
            [InlineKeyboardButton("Personel Tracking", callback_data=str(SWFM_BANTUAN_SPV_7))],
            [InlineKeyboardButton("SVA", callback_data=str(SWFM_BANTUAN_SPV_8))],
            [InlineKeyboardButton("Asset Safe Guard", callback_data=str(SWFM_BANTUAN_SPV_9))],
            [InlineKeyboardButton("TS Manual", callback_data=str(SWFM_BANTUAN_SPV_10))],
            [InlineKeyboardButton("Manage User Mobile", callback_data=str(SWFM_BANTUAN_SPV_11))],
            [InlineKeyboardButton("ANT TOTI", callback_data=str(SWFM_BANTUAN_SPV_12))],
            [InlineKeyboardButton("ANT RPM", callback_data=str(SWFM_BANTUAN_SPV_13))],
            [InlineKeyboardButton("BBM Fixed Genset Refill", callback_data=str(SWFM_BANTUAN_SPV_14))],
            [InlineKeyboardButton("TPAS", callback_data=str(SWFM_BANTUAN_SPV_15))],
            [InlineKeyboardButton("CGL", callback_data=str(SWFM_BANTUAN_SPV_16))],
            [InlineKeyboardButton("Batal", callback_data=str(CANCEL_HOME))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Penjelasan Kategori: \n*Site List Management :* Ubah data Lon-Lat Site\n*PM Schedule Planning :* Add Site, Take Out Site, Switch Site, Change Date, Verify, Extend Permit, Print Permit\n*PM Site :* Approval ticket\n*PM Genset :* Approval ticket\n*Fault Center :* Manual Dispatch, Escalate to INSERA, Escalate to TOTI, Update RCA, Resolved Ticket, Switch Ticket Type\n*Fault Center SWFM :* Exclude Ticket\n*Personel Tracking :* Info Clock-in/Clock-out TO, Tiket yang di handle, Export\n*SVA :* Create ticket, Add Doc/Photo/Receipt, Re-assign, Review ticket\n*Asset Safe Guard :* Approval ticket\n*TS Manual :* Create ticket, Approval ticket, Export ticket\n*Manage User Mobile :* Ubah Role, Ubah Device, Reset Password\n*ANT TOTI :* Create ticket, View file bukti\n*ANT RPM :* View file bukti, Approval ticket\n*BBM Fixed Genset Refill :* Create ticket\n*TPAS :* Search permit, View detail permit, Approval permit\n*CGL :* Create ticket\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :",reply_markup=reply_markup)
def swfm_bantuan_spv(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    query = update.callback_query
    query.answer()
    message_id = query.message.message_id-1
    chat_id = update.callback_query.from_user.id
    bot_log.delete_message(chat_id,message_id)
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    if 'Site List Management' in data_text:
        query.message.reply_text("https://bit.ly/swfm-site-list-management",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'PM Schedule Planning' in data_text:
        query.message.reply_text("https://bit.ly/swfm-pm-schedule-planning",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'PM Site' in data_text:
        query.message.reply_text("https://bit.ly/swfm-pm-site",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'PM Genset' in data_text:
        query.message.reply_text("https://bit.ly/swfm-pm-genset",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'Fault Center' in data_text:
        query.message.reply_text("https://bit.ly/swfm-fault-center",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'Fault Center SWFM' in data_text:
        query.message.reply_text("https://bit.ly/swfm-fault-center-swfm",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'Personel Tracking' in data_text:
        query.message.reply_text("https://bit.ly/swfm-personel-tracking",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'SVA' in data_text:
        query.message.reply_text("https://bit.ly/swfm-service-variable-activity",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'Asset Safe Guard' in data_text:
        query.message.reply_text("https://bit.ly/swfm-asset-guard",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'TS Manual' in data_text:
        query.message.reply_text("https://bit.ly/swfm-ts-manual",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'Manage User Mobile' in data_text:
        query.message.reply_text("https://bit.ly/swfm-manage-user-mobile",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'ANT TOTI' in data_text:
        query.message.reply_text("https://bit.ly/swfm-ticket-tp",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'ANT RPM' in data_text:
        query.message.reply_text("https://bit.ly/swfm-ticket-rpm",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'BBM Fixed Genset Refill' in data_text:
        query.message.reply_text("https://bit.ly/swfm-bbm-fixed-genset-refill",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'TPAS' in data_text:
        query.message.reply_text("https://bit.ly/swfm-permit-approval",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'CGL' in data_text:
        query.message.reply_text("https://bit.ly/swfm-interference-lightning-claim",parse_mode=telegram.ParseMode.HTML)
        query.message.reply_text(text=f"Berikut adalah Pusat Bantuan ({data_text}), terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_inline_swfm(update, '*Pusat Bantuan* ➞ Bantuan')
    return ConversationHandler.END

def del_userbot(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    
    query.message.reply_text(text="Masukkan No HP yang akan di hapus dari database BOT :",parse_mode=telegram.ParseMode.MARKDOWN)
    return SWFM_USERBOT_END

def swfm_userbot_end(update: Update, _: CallbackContext) -> None:
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Harap menunggu dalam beberapa detik....',parse_mode=telegram.ParseMode.MARKDOWN)
    data_text = update.message.text.replace('+','').replace(' ','').replace('-','')
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_bot_swfm where no_hp = '{data_text}'"
    check_status = client.command(query)
    check_status = check_status == 0
    if check_status is True:
        update.message.reply_text('Maaf No HP yang anda masukkan salah atau tidak sesuai. Silahkan cek kembali',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_swfm(update, '*Hapus UserBot* ➞ No HP yang dimasukkan salah atau tidak sesuai')
    elif check_status is False:
        client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
        query = f"ALTER TABLE production.helpdesk_bot_swfm DELETE WHERE no_hp = '{data_text}'"
        data = client.command(query)
        update.message.reply_text(f'✅ User dari No HP {data_text} berhasil dihapus',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_swfm(update, '*Hapus UserBot* ➞ Berhasil hapus UserBot dengan Nomor '+data_text)
    return ConversationHandler.END

def swfm_download(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text("https://tia.telkomsel.co.id/NativeAppBuilder/App?AppKey=fdb3ff36-032d-424a-97d5-3539184520b0",parse_mode=telegram.ParseMode.HTML)
    query.message.reply_text(text="Berikut adalah link Download Aplikasi SWFM, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_inline_swfm(update, '*Download* ➞ Aplikasi')
    return ConversationHandler.END
def swfm_download_excel(update: Update, _: CallbackContext) -> None: 
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(text="Mohon menunggu dalam beberapa detik...",parse_mode=telegram.ParseMode.MARKDOWN)
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select * from production.helpdesk_report_swfm hrs  where status = 'open' and category = 'SWFM'"
    data = client.command(query)
    try:
        data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
        array_data = []
        for data in data_list:
            data = str(data).split(', ')
            dub_data = {'Nama': f'{data[0]}', 'Username Telegram': f'{data[1]}', 'Chatid Telegram': f'{data[2]}', 'No HP': f'{data[3]}', 'Email': f'{data[4]}', 'Remark': f'{data[5]}', 'Position' : f'{data[9]}', 'Channel Chatid': f'{data[10]}', 'Ticket': f'{data[11]}', 'Divison': f'{data[12]}', 'Regional': f'{data[13]}', 'Problem Title': f'{data[14]}', 'Problem Summary': f'{data[15]}', 'Status': f'{data[16]}', 'Category': f'{data[17]}', 'Open Ticket Date': f'{data[18]}, {data[19]}', 'Closed Ticket Date': f'{data[20]}', 'FCAPS': f'{data[21]}', 'Action Menu': f'{data[22]}', 'Action Category': f'{data[23]}', 'Action Handle By': f'{data[24]}', 'Action Resolution': f'{data[25]}', 'Post Link': f'{data[26]}'}
            array_data.append(dub_data)
    except:
        array_data = [{'Nama': '-', 'Username Telegram': '-', 'Chatid Telegram': '-', 'No HP': '-', 'Email': '-', 'Remark': '-', 'Position' : '-', 'Channel Chatid': '-', 'Ticket': '-', 'Divison': '-', 'Regional': '-', 'Problem Title': '-', 'Problem Summary': '-', 'Status': '-', 'Category': '-', 'Open Ticket Date': '- -', 'Closed Ticket Date': '-', 'FCAPS': '-', 'Action Menu': '-', 'Action Category': '-', 'Action Handle By': '-', 'Action Resolution': '-', 'Post Link': '-'}]
    query = f"select * from production.helpdesk_report_swfm hrs  where status = 'closed' and category = 'SWFM'"
    data = client.command(query)
    data_list = str(data).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
    array_data1 = []
    for data in data_list:
        data = str(data).split(', ')
        dub_data = {'Nama': f'{data[0]}', 'Username Telegram': f'{data[1]}', 'Chatid Telegram': f'{data[2]}', 'No HP': f'{data[3]}', 'Email': f'{data[4]}', 'Remark': f'{data[5]}', 'Position' : f'{data[9]}', 'Channel Chatid': f'{data[10]}', 'Ticket': f'{data[11]}', 'Divison': f'{data[12]}', 'Regional': f'{data[13]}', 'Problem Title': f'{data[14]}', 'Problem Summary': f'{data[15]}', 'Status': f'{data[16]}', 'Category': f'{data[17]}', 'Open Ticket Date': f'{data[18]}, {data[19]}', 'Closed Ticket Date': f'{data[20]},{data[21]}', 'FCAPS': f'{data[22]}', 'Action Menu': f'{data[23]}', 'Action Category': f'{data[24]}', 'Action Handle By': f'{data[25]}', 'Action Resolution': f'{data[26]}', 'Post Link': f'{data[27]}'}
        array_data1.append(dub_data)

    df1 = pd.DataFrame(array_data)
    df2 = pd.DataFrame(array_data1)
    writer = pd.ExcelWriter('/home/dimas/baru/helpdeskbot_v2/data/data_report_open_ticket_swfm.xlsx', engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Open Ticket', index=False)
    df2.to_excel(writer, sheet_name='Closed Ticket', index=False)
    writer.save()
    print('Sukses')
    syanticbot = telegram.Bot(token_bot) #SYANTICBOT
    syanticbot.sendDocument(chat_id = chatid_telegram, document=open('/home/dimas/baru/helpdeskbot_v2/data/data_report_open_ticket_swfm.xlsx','rb'), filename="Report Ticket SWFM.xlsx",caption='Ready to download Report Ticket SWFM')
    query = update.callback_query
    query.answer()
    query.message.reply_text(text="Berikut adalah link Download Aplikasi SWFM, terima kasih",parse_mode=telegram.ParseMode.MARKDOWN)
    log_bot_success_inline_swfm(update, '*Download* ➞ Laporan Tiket Excel')
    return ConversationHandler.END
def swfm_postlink(update: Update, _: CallbackContext) -> None: 
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Anda memilih : *My Ticket List*',parse_mode=telegram.ParseMode.MARKDOWN)
    try:
        query = f"select fullname_telegram, username_telegram, ticket, problem_title, post_link from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}' and category = 'SWFM' and status = 'open'"
        data = client.command(query)
        query = f"select count(*) as `count` from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and category = 'SWFM' and status = 'open'"
        count_query = client.command(query)
        query = update.callback_query
        query.answer()
        check_status = count_query == 0
        if check_status is True:
            query.message.reply_text(f'Maaf anda tidak mempunyai My Ticket List',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_swfm(update, '*My Ticket List* ➞ My Ticket List Tidak Ditemukan')
        elif check_status is False:
            query = f"select fullname_telegram, username_telegram, ticket, problem_title, post_link from production.helpdesk_report_swfm where chatid_telegram = '{chatid_telegram}' and category = 'SWFM' and status = 'open'"
            data1 = client.command(query)
            query = update.callback_query
            query.answer()
            data_list = str(data1).replace("[","").replace("]","").replace("'","").replace("\\\\n",' ').split('\\n')
            output_text = ''
            output_text += '*Berikut adalah My Ticket List anda*\n\n'
            output_text += '*Category - Ticket - Post Link*\n'
            for data in data_list:
                data = str(data).split(', ')
                ticket = data[2]
                problem_title = str(data[3]).split(' ➞ ')[0]
                post_link = data[4]
                output_text += f"{problem_title} - {ticket} - {post_link}\n"
            output_text += '\n'
            output_text += 'Regards\nOCHABOT & Team'
            query.message.reply_text(f'{output_text}',parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_inline_swfm(update, '*My Ticket List* ➞ My Ticket List Ditemukan')
        return ConversationHandler.END
    except:
        query = update.callback_query
        query.answer()
        query.message.reply_text(f'Maaf anda tidak mempunyai My Ticket List',parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_inline_swfm(update, '*My Ticket List* ➞ My Ticket List Tidak Ditemukan')
        return ConversationHandler.END

def swfm_complaint(update: Update, _: CallbackContext) -> None: 
    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Anda memilih : *Eskalasi Case*',parse_mode=telegram.ParseMode.MARKDOWN)
    query.message.reply_text(f'Ketik nomor ticket anda SFMXXXXXXXXX',parse_mode=telegram.ParseMode.MARKDOWN)
    return SWFM_COMPLAINT_END

def swfm_complaint_end(update: Update, _: CallbackContext) -> None: 
    parameter_ticket = update.message.text
    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{parameter_ticket}' and category = 'SWFM'"
    check_status = client.command(query)
    check_status = check_status == 0
    if check_status is True:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text(f"Nomor tiket tidak sesuai kategori atau salah", parse_mode=telegram.ParseMode.MARKDOWN)
        log_bot_success_swfm(update, '*Eskalasi Case* ➞ Nomor Tiket Tidak Ditemukan')
    elif check_status is False:
        query = f"select count(*) as `count` from production.helpdesk_report_swfm where ticket = '{parameter_ticket}' and category = 'SWFM'"
        check_status = client.command(query)
        check_status = check_status == 0
        if check_status is True:
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f"Nomor tiket telah closed", parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_swfm(update, '*Eskalasi Case* ➞ Nomor Tiket Telah Closed')
        elif check_status is False:
            chatid_1 = '342102215'
            chatid_2 = '1176582959'
            chatid_3 = '1464528446'
            chatid_4 = '1829660243'
            chatid_5 = '5317456220'
            chatid_6 = '5428551305'
            chatid_7 = '6352879536'
            chatid_8 = '6494532312'
            chatid_9 = '6520696581'
            chatid_10 = '462124845'
            chatid_11 = '135159366'
            query = f"select ticket, post_link from production.helpdesk_report_swfm where ticket = '{parameter_ticket}'"
            data_redirect = client.command(query)
            post_link = data_redirect[1]

            # bot_log.send_message(chat_id=chatid_10,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  {parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

            bot_log.send_message(chat_id=chatid_1,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_2,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_3,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_4,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_5,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_6,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_7,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_8,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_9,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_10,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            bot_log.send_message(chat_id=chatid_11,text=f'📣 Eskalasi Case\n\nSemangat Pagi Rekan Admin HD...\n\nNomor Tiket  #{parameter_ticket} ➞ di room diskusi ({post_link})\n\nMohon bantuannya Admin HD, segera di respon kendalanya karena sampai saat ini masih belum ada updated\n\nTerima Kasih',parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            update.message.reply_text(f"Anda berhasil membuat Eskalasi Case, Mohon ditunggu sampai Team HD merespon di room diskusi. Terima Kasih", parse_mode=telegram.ParseMode.MARKDOWN)
            log_bot_success_swfm_com(update, '*Eskalasi Case* ➞ Eskalasi Case Berhasil dengan Nomor Tiket '+parameter_ticket)
    return ConversationHandler.END

################################################END SWFM#######################################

def main() -> None:
    updater = Updater(token_bot) 
    dispatcher = updater.dispatcher
    #Requests
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU_REGISTRATION: [
            CallbackQueryHandler(registration_tools_ioms, pattern='^' + str(REGISTRATION_TOOLS_IOMS) + '$'),
            CallbackQueryHandler(registration_check_ioms, pattern='^' + str(REGISTRATION_IOMS) + '$'),
            CallbackQueryHandler(registration_ioms_mitra, pattern='^' + str(REGISTRATION_IOMS_MITRA) + '$'),
            
            #
            CallbackQueryHandler(registration_tools_ipas, pattern='^' + str(REGISTRATION_TOOLS_IPAS) + '$'),
            CallbackQueryHandler(registration_check_ipas, pattern='^' + str(REGISTRATION_IPAS) + '$'),
            CallbackQueryHandler(registration_ipas_mitra, pattern='^' + str(REGISTRATION_IPAS_MITRA) + '$'),
            #
            CallbackQueryHandler(registration_tools_swfm, pattern='^' + str(REGISTRATION_TOOLS_SWFM) + '$'),
            CallbackQueryHandler(registration_check_swfm, pattern='^' + str(REGISTRATION_SWFM) + '$'),
            CallbackQueryHandler(registration_swfm_end, pattern='^' + str(REGISTRATION_SWFM_END) + '$'),
            CallbackQueryHandler(cancel_home, pattern='^' + str(CANCEL_HOME) + '$')],
            REGISTRATION_EMAILS_IOMS: [MessageHandler(Filters.text & ~Filters.command, registration_emails_ioms)],
            REGISTRATION_PWD_IOMS: [MessageHandler(Filters.text & ~Filters.command, registration_pwd_ioms)],
            LDAP_NO_IOMS: [MessageHandler(Filters.text & ~Filters.command, ldap_no_ioms)],

            REGISTRATION_EMAILS_IPAS: [MessageHandler(Filters.text & ~Filters.command, registration_emails_ipas)],
            REGISTRATION_PWD_IPAS: [MessageHandler(Filters.text & ~Filters.command, registration_pwd_ipas)],
            LDAP_NO_IPAS: [MessageHandler(Filters.text & ~Filters.command, ldap_no_ipas)],

            REGISTRATION_NOHP_SWFM: [MessageHandler(Filters.text & ~Filters.command, registration_nohp_swfm)],
            REGISTRATION_EMAIL_SWFM: [MessageHandler(Filters.text & ~Filters.command, registration_email_swfm)],
            REGISTRATION_IOMS_END: [MessageHandler(Filters.text & ~Filters.command, registration_ioms_end)],
            REGISTRATION_IPAS_END: [MessageHandler(Filters.text & ~Filters.command, registration_ipas_end)],
            # CallbackQueryHandler(registration_end_approval, pattern='^' + str(REGISTRATION_END_APPROVAL) + '$')
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)]},
    
        fallbacks=[CommandHandler('cancel', cancel_registration),CommandHandler('batal', cancel_registration)],conversation_timeout=90)
    dispatcher.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('panduan', panduan)],
        states={
            PANDUAN: [
            CallbackQueryHandler(panduan_swfm, pattern='^' + str(PANDUAN_SWFM) + '$'),
            CallbackQueryHandler(panduan_ioms, pattern='^' + str(PANDUAN_IOMS) + '$'),
            CallbackQueryHandler(panduan_ipas, pattern='^' + str(PANDUAN_IPAS) + '$'),
            CallbackQueryHandler(cancel_home, pattern='^' + str(CANCEL_HOME) + '$'),
            ],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)]},

        fallbacks=[CommandHandler('cancel', cancel_registration),CommandHandler('batal', cancel_registration)],conversation_timeout=90)
    dispatcher.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu', menu)],
        states={
            MENU_REGISTRATION: [
            CallbackQueryHandler(cancel_home, pattern='^' + str(CANCEL_HOME) + '$')],
            MENU: [
            CallbackQueryHandler(menu_utama, pattern='^' + str(MENU_UTAMA) + '$'),
            CallbackQueryHandler(menu_ioms, pattern='^' + str(MENU_IOMS) + '$'),
            CallbackQueryHandler(menu_ioms_, pattern='^' + str(MENU_IOMS_) + '$'),
            CallbackQueryHandler(ioms_reqticket, pattern='^' + str(IOMS_REQTICKET) + '$'),
            CallbackQueryHandler(ioms_reqticket_, pattern='^' + str(IOMS_REQTICKET_) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT7) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT8) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT9) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT10) + '$'),
            # CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT11) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT12) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT13) + '$'),
            CallbackQueryHandler(ioms_reqticket_add, pattern='^' + str(IOMS_CAT14) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_10) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_11) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_12) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_13) + '$'),
            # CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_14) + '$'),
            CallbackQueryHandler(ioms_reqticket_case_a, pattern='^' + str(IOMS_CAT1_CASE_A_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_case_a, pattern='^' + str(IOMS_CAT1_CASE_A_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_case_a, pattern='^' + str(IOMS_CAT1_CASE_A_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_case_a, pattern='^' + str(IOMS_CAT1_CASE_A_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_case_a, pattern='^' + str(IOMS_CAT1_CASE_A_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_case_a, pattern='^' + str(IOMS_CAT1_CASE_A_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_case_a, pattern='^' + str(IOMS_CAT1_CASE_A_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_case_a, pattern='^' + str(IOMS_CAT1_CASE_A_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_case_a, pattern='^' + str(IOMS_CAT1_CASE_A_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A1_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A1_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A1_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A2_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A2_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A2_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A2_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A3_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A3_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A3_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A4_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A4_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A4_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A4_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_10) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_11) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_12) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_13) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_14) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A5_15) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A6_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A6_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A6_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A6_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A7_10) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A8_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A8_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A8_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A9_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A9_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A9_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A9_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A9_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A9_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A9_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT1_CASE_A9_8) + '$'),

            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_10) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_11) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT2_12) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT3_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT3_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT3_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT4_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT4_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT5_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT5_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT5_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT6_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT6_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT6_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT6_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT6_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT7_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT7_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT7_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT7_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT7_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT7_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT7_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT7_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT8_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT8_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT8_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT8_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT8_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT8_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT8_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT8_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT8_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT9_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT9_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT10_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT10_2) + '$'),
            # INI
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT12_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT12_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT12_3) + '$'),
            # CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT12_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT13_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT13_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT13_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT13_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT13_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT13_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_10) + '$'),
            CallbackQueryHandler(ioms_reqticket_add1, pattern='^' + str(IOMS_CAT14_11) + '$'),
            CallbackQueryHandler(ioms_expert, pattern='^' + str(IOMS_EXPERT) + '$'),
            CallbackQueryHandler(reg_expert_ioms, pattern='^' + str(REG_EXPERT_IOMS) + '$'),
            CallbackQueryHandler(del_expert_ioms, pattern='^' + str(DEL_EXPERT_IOMS) + '$'),
            CallbackQueryHandler(ioms_myticket, pattern='^' + str(IOMS_MYTICKET) + '$'),
            CallbackQueryHandler(ioms_broadcast, pattern='^' + str(IOMS_BROADCAST) + '$'),
            CallbackQueryHandler(ioms_makeadmin, pattern='^' + str(IOMS_MAKEADMIN) + '$'),
            CallbackQueryHandler(ioms_postlink, pattern='^' + str(IOMS_POSTLINK) + '$'),
            CallbackQueryHandler(ioms_download_excel, pattern='^' + str(IOMS_DOWNLOAD_EXCEL) + '$'),
            CallbackQueryHandler(ioms_complaint, pattern='^' + str(IOMS_COMPLAINT) + '$'),
            #
            CallbackQueryHandler(menu_ipas, pattern='^' + str(MENU_IPAS) + '$'),
            CallbackQueryHandler(menu_ipas_, pattern='^' + str(MENU_IPAS_) + '$'),
            CallbackQueryHandler(ipas_reqticket, pattern='^' + str(IPAS_REQTICKET) + '$'),
            CallbackQueryHandler(ipas_reqticket_add, pattern='^' + str(IPAS_CAT1) + '$'),
            CallbackQueryHandler(ipas_reqticket_add, pattern='^' + str(IPAS_CAT2) + '$'),
            CallbackQueryHandler(ipas_reqticket_add, pattern='^' + str(IPAS_CAT3) + '$'),
            CallbackQueryHandler(ipas_reqticket_add, pattern='^' + str(IPAS_CAT4) + '$'),
            CallbackQueryHandler(ipas_reqticket_add, pattern='^' + str(IPAS_CAT5) + '$'),
            CallbackQueryHandler(ipas_reqticket_add, pattern='^' + str(IPAS_CAT6) + '$'),
            CallbackQueryHandler(ipas_reqticket_add, pattern='^' + str(IPAS_CAT7) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat1, pattern='^' + str(IPAS_CAT1_1) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat1, pattern='^' + str(IPAS_CAT1_2) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat1, pattern='^' + str(IPAS_CAT1_3) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat1, pattern='^' + str(IPAS_CAT1_4) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat1, pattern='^' + str(IPAS_CAT1_5) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat1, pattern='^' + str(IPAS_CAT1_6) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat2, pattern='^' + str(IPAS_CAT2_1) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat2, pattern='^' + str(IPAS_CAT2_2) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat2, pattern='^' + str(IPAS_CAT2_3) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat3, pattern='^' + str(IPAS_CAT3_1) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat3, pattern='^' + str(IPAS_CAT3_2) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat3, pattern='^' + str(IPAS_CAT3_3) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat4, pattern='^' + str(IPAS_CAT4_1) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat4, pattern='^' + str(IPAS_CAT4_2) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat4, pattern='^' + str(IPAS_CAT4_3) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat4, pattern='^' + str(IPAS_CAT4_4) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat5, pattern='^' + str(IPAS_CAT5_1) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat5, pattern='^' + str(IPAS_CAT5_2) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat5, pattern='^' + str(IPAS_CAT5_3) + '$'),
            CallbackQueryHandler(ipas_reqticket_cat5, pattern='^' + str(IPAS_CAT5_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_CAT6_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_CAT6_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_CAT6_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_CAT6_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_CAT6_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_CAT7_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_CAT7_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_CAT7_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_CAT7_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_10) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_11) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_12) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_13) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_14) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_15) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_16) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_17) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_18) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_19) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_20) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_21) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_22) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_23) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_24) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_25) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT1_26) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT2_10) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_10) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT3_11) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT4_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT4_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT4_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT4_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_1) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_2) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_3) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_4) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_5) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_6) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_7) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_8) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_9) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_10) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_11) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_12) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_13) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_14) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_15) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_16) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_17) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_18) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_19) + '$'),
            CallbackQueryHandler(ioms_reqticket_all, pattern='^' + str(IPAS_TICKET_CAT5_20) + '$'),

            CallbackQueryHandler(ipas_expert, pattern='^' + str(IPAS_EXPERT) + '$'),
            CallbackQueryHandler(reg_expert_ipas, pattern='^' + str(REG_EXPERT_IPAS) + '$'),
            CallbackQueryHandler(del_expert_ipas, pattern='^' + str(DEL_EXPERT_IPAS) + '$'),
            CallbackQueryHandler(ipas_myticket, pattern='^' + str(IPAS_MYTICKET) + '$'),
            CallbackQueryHandler(ipas_broadcast, pattern='^' + str(IPAS_BROADCAST) + '$'),
            CallbackQueryHandler(ipas_makeadmin, pattern='^' + str(IPAS_MAKEADMIN) + '$'),
            CallbackQueryHandler(ipas_postlink, pattern='^' + str(IPAS_POSTLINK) + '$'),
            CallbackQueryHandler(ipas_download_excel, pattern='^' + str(IPAS_DOWNLOAD_EXCEL) + '$'),
            CallbackQueryHandler(ipas_complaint, pattern='^' + str(IPAS_COMPLAINT) + '$'),
            #
            CallbackQueryHandler(menu_scarlett, pattern='^' + str(MENU_SCARLETT) + '$'),
            CallbackQueryHandler(menu_scarlett_, pattern='^' + str(MENU_SCARLETT_) + '$'),
            CallbackQueryHandler(scarlett_reqticket, pattern='^' + str(SCARLETT_REQTICKET) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add1, pattern='^' + str(SCARLETT_CAT1) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add2, pattern='^' + str(SCARLETT_CAT1_1) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add2, pattern='^' + str(SCARLETT_CAT1_2) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add2, pattern='^' + str(SCARLETT_CAT1_3) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add, pattern='^' + str(SCARLETT_CAT2) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add, pattern='^' + str(SCARLETT_CAT3) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add, pattern='^' + str(SCARLETT_CAT4) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add, pattern='^' + str(SCARLETT_CAT5) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add, pattern='^' + str(SCARLETT_CAT6) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add, pattern='^' + str(SCARLETT_CAT7) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add, pattern='^' + str(SCARLETT_CAT8) + '$'),
            # CallbackQueryHandler(scarlett_reqticket_add, pattern='^' + str(SCARLETT_CAT9) + '$'),
            CallbackQueryHandler(scarlett_reqticket_add, pattern='^' + str(SCARLETT_CAT10) + '$'),
            CallbackQueryHandler(scarlett_myticket, pattern='^' + str(SCARLETT_MYTICKET) + '$'),
            CallbackQueryHandler(scarlett_postlink, pattern='^' + str(SCARLETT_POSTLINK) + '$'),
            CallbackQueryHandler(scarlett_download_excel, pattern='^' + str(SCARLETT_DOWNLOAD_EXCEL) + '$'),
            CallbackQueryHandler(scarlett_complaint, pattern='^' + str(SCARLETT_COMPLAINT) + '$'),
            #
            CallbackQueryHandler(menu_swfm, pattern='^' + str(MENU_SWFM) + '$'),
            CallbackQueryHandler(swfm_reqticket, pattern='^' + str(SWFM_REQTICKET) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET7) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET8) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET9) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET10) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET11) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET12) + '$'),
            CallbackQueryHandler(swfm_reqticket_add, pattern='^' + str(SWFM_REQTICKET13) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT7) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT8) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT9) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT10) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT11) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT12) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT13) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT14) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT15) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT16) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT17) + '$'),
            # CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT18) + '$'),
            CallbackQueryHandler(swfm_reqticket_add1, pattern='^' + str(SWFM_CAT19) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT1_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT1_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT1_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT1_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT1_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT2_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT2_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT2_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT2_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT2_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_7) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_8) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_9) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT3_10) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT4_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT4_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT4_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT5_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT5_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT5_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT5_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_7) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_8) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_9) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_10) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_11) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_12) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_13) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_14) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_15) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_16) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_17) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_18) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_19) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_20) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_21) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_22) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_23) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_24) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT6_25) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT7_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT7_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_7) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_8) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_9) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_10) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_11) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_12) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_13) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT8_14) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_7) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_8) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_9) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_10) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_11) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_12) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_13) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_14) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_15) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_16) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_17) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_18) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_19) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_20) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_21) + '$'),

            CallbackQueryHandler(swfm_reqticket_pmsite, pattern='^' + str(SWFM_CAT9_PMSITE) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSITE_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSITE_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSITE_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSITE_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSITE_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSITE_6) + '$'),
            CallbackQueryHandler(swfm_reqticket_pmgenset, pattern='^' + str(SWFM_CAT9_PMGENSET) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMGENSET_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMGENSET_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMGENSET_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMGENSET_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMGENSET_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMGENSET_6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMGENSET_7) + '$'),
            CallbackQueryHandler(swfm_reqticket_pmsampling, pattern='^' + str(SWFM_CAT9_PMSAMPLING) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSAMPLING_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSAMPLING_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSAMPLING_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSAMPLING_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT9_PMSAMPLING_5) + '$'),

            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT11_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT11_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT11_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT11_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT12_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT12_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT12_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT12_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT12_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT13_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT13_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT13_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT13_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT13_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT14_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT14_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT14_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT14_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT15_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT15_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT15_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT15_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT15_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_7) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_8) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_9) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT16_10) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT17_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT17_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT17_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT17_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT17_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT17_6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT17_7) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT18_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT18_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT18_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT18_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT18_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_1) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_2) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_3) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_4) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_5) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_6) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_7) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_8) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_9) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_10) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_11) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_12) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_13) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_14) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_15) + '$'),
            CallbackQueryHandler(swfm_reqticket_add2, pattern='^' + str(SWFM_CAT19_16) + '$'),

            

            
            CallbackQueryHandler(swfm_expert, pattern='^' + str(SWFM_EXPERT) + '$'),
            CallbackQueryHandler(reg_expert_swfm, pattern='^' + str(REG_EXPERT_SWFM) + '$'),
            CallbackQueryHandler(del_expert_swfm, pattern='^' + str(DEL_EXPERT_SWFM) + '$'),
            CallbackQueryHandler(swfm_myticket, pattern='^' + str(SWFM_MYTICKET) + '$'),
            CallbackQueryHandler(swfm_broadcast, pattern='^' + str(SWFM_BROADCAST) + '$'),
            CallbackQueryHandler(swfm_makeadmin, pattern='^' + str(SWFM_MAKEADMIN) + '$'),
            CallbackQueryHandler(swfm_bantuan, pattern='^' + str(SWFM_BANTUAN) + '$'),
            CallbackQueryHandler(swfm_bantuan_end, pattern='^' + str(SWFM_BANTUAN_1) + '$'),
            CallbackQueryHandler(swfm_bantuan_end, pattern='^' + str(SWFM_BANTUAN_2) + '$'),
            CallbackQueryHandler(swfm_bantuan_end, pattern='^' + str(SWFM_BANTUAN_3) + '$'),
            CallbackQueryHandler(swfm_bantuan_end, pattern='^' + str(SWFM_BANTUAN_4) + '$'),
            CallbackQueryHandler(swfm_bantuan_end, pattern='^' + str(SWFM_BANTUAN_5) + '$'),
            CallbackQueryHandler(swfm_bantuan_end, pattern='^' + str(SWFM_BANTUAN_6) + '$'),
            CallbackQueryHandler(swfm_bantuan_end, pattern='^' + str(SWFM_BANTUAN_7) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_1) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_2) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_3) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_4) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_5) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_6) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_7) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_8) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_9) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_10) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_11) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_12) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_13) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_14) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_15) + '$'),
            CallbackQueryHandler(swfm_bantuan_spv, pattern='^' + str(SWFM_BANTUAN_SPV_16) + '$'),
            CallbackQueryHandler(del_userbot, pattern='^' + str(DEL_USERBOT) + '$'),
            # CallbackQueryHandler(swfm_download, pattern='^' + str(SWFM_DOWNLOAD) + '$'),
            CallbackQueryHandler(swfm_download_excel, pattern='^' + str(SWFM_DOWNLOAD_EXCEL) + '$'),
            CallbackQueryHandler(swfm_postlink, pattern='^' + str(SWFM_POSTLINK) + '$'),
            CallbackQueryHandler(swfm_complaint, pattern='^' + str(SWFM_COMPLAINT) + '$'),
            CallbackQueryHandler(cancel_home, pattern='^' + str(CANCEL_HOME) + '$'),
            ],
            #SCARLETT
            SCARLETT_MYTICKET_PROCESS: [MessageHandler(Filters.text & ~Filters.command, scarlett_myticket_process)],
            SCARLETT_MYTICKET_CLOSED: [CallbackQueryHandler(scarlett_myticket_closed, pattern='^' + str(SCARLETT_MYTICKET_PROCESS_END) + '$'),
            CallbackQueryHandler(cancel_home, pattern='^' + str(CANCEL_HOME) + '$')],
            SCARLETT_MYTICKET_CLOSED_END: [MessageHandler(Filters.text & ~Filters.command, scarlett_myticket_closed_end)],

            #IOMS
            IOMS_MYTICKET_PROCESS: [MessageHandler(Filters.text & ~Filters.command, ioms_myticket_process)],
            IOMS_MYTICKET_CLOSED: [CallbackQueryHandler(ioms_myticket_closed, pattern='^' + str(IOMS_MYTICKET_PROCESS_END) + '$'),
            CallbackQueryHandler(cancel_home, pattern='^' + str(CANCEL_HOME) + '$')],
            IOMS_MYTICKET_CLOSED_END: [MessageHandler(Filters.text & ~Filters.command, ioms_myticket_closed_end)],

            #INAP
            IPAS_MYTICKET_PROCESS: [MessageHandler(Filters.text & ~Filters.command, ipas_myticket_process)],
            IPAS_MYTICKET_CLOSED: [CallbackQueryHandler(ipas_myticket_closed, pattern='^' + str(IPAS_MYTICKET_PROCESS_END) + '$'),
            CallbackQueryHandler(cancel_home, pattern='^' + str(CANCEL_HOME) + '$')],
            IPAS_MYTICKET_CLOSED_END: [MessageHandler(Filters.text & ~Filters.command, ipas_myticket_closed_end)],

            SWFM_MYTICKET_ERROR: [MessageHandler(Filters.text & ~Filters.command, swfm_myticket_error)],
            SWFM_MYTICKET_PROCESS: [CallbackQueryHandler(swfm_myticket_process_end, pattern='^' + str(SWFM_MYTICKET_PROCESS_END) + '$'),
            CallbackQueryHandler(swfm_myticket_action_menu, pattern='^' + str(SWFM_MYTICKET_ACTION_MENU1) + '$'),
            CallbackQueryHandler(swfm_myticket_action_menu, pattern='^' + str(SWFM_MYTICKET_ACTION_MENU2) + '$'),
            CallbackQueryHandler(swfm_myticket_action_menu, pattern='^' + str(SWFM_MYTICKET_ACTION_MENU3) + '$'),
            CallbackQueryHandler(swfm_myticket_action_menu, pattern='^' + str(SWFM_MYTICKET_ACTION_MENU4) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT1) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT2) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT3) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT4) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT5) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT6) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT7) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT8) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT9) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT10) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT11) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT12) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT13) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT14) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT15) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT16) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT17) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT18) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT19) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT20) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT21) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT22) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT23) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT24) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT25) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT26) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT27) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT28) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT29) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT30) + '$'),
            CallbackQueryHandler(swfm_myticket_action_cat, pattern='^' + str(SWFM_MYTICKET_ACTION_CAT31) + '$'),
            CallbackQueryHandler(cancel_home, pattern='^' + str(CANCEL_HOME) + '$')],
            SWFM_MYTICKET_CLOSED: [MessageHandler(Filters.text & ~Filters.command, swfm_myticket_closed)],

            IOMS_BROADCAST_END: [MessageHandler(Filters.text & ~Filters.command, ioms_broadcast_end)],
            IPAS_BROADCAST_END: [MessageHandler(Filters.text & ~Filters.command, ipas_broadcast_end)],
            SWFM_BROADCAST_END: [MessageHandler(Filters.text & ~Filters.command, swfm_broadcast_end)],

            IOMS_MAKEADMIN_END: [MessageHandler(Filters.text & ~Filters.command, ioms_makeadmin_end)],
            IPAS_MAKEADMIN_END: [MessageHandler(Filters.text & ~Filters.command, ipas_makeadmin_end)],
            SWFM_MAKEADMIN_END: [MessageHandler(Filters.text & ~Filters.command, swfm_makeadmin_end)],

            IOMS_COMPLAINT_END: [MessageHandler(Filters.text & ~Filters.command, ioms_complaint_end)],
            SCARLETT_COMPLAINT_END: [MessageHandler(Filters.text & ~Filters.command, scarlett_complaint_end)],
            IPAS_COMPLAINT_END: [MessageHandler(Filters.text & ~Filters.command, ipas_complaint_end)],
            SWFM_COMPLAINT_END: [MessageHandler(Filters.text & ~Filters.command, swfm_complaint_end)],

            SWFM_USERBOT_END: [MessageHandler(Filters.text & ~Filters.command, swfm_userbot_end)],
            
            END_IOMS: [MessageHandler(Filters.text & ~Filters.command, end_ioms)],
            END_SCARLETT: [MessageHandler(Filters.text & ~Filters.command, end_scarlett)],
            END_IPAS: [MessageHandler(Filters.text & ~Filters.command, end_ipas)],
            END_REG_EXPERT_IOMS: [MessageHandler(Filters.text & ~Filters.command, end_reg_expert_ioms)],
            END_DEL_EXPERT_IOMS: [MessageHandler(Filters.text & ~Filters.command, end_del_expert_ioms)],
            END_REG_EXPERT_IPAS: [MessageHandler(Filters.text & ~Filters.command, end_reg_expert_ipas)],
            END_DEL_EXPERT_IPAS: [MessageHandler(Filters.text & ~Filters.command, end_del_expert_ipas)],
            END_SWFM: [MessageHandler(Filters.text & ~Filters.command, end_swfm)],
            END_REG_EXPERT_SWFM: [MessageHandler(Filters.text & ~Filters.command, end_reg_expert_swfm)],
            END_DEL_EXPERT_SWFM: [MessageHandler(Filters.text & ~Filters.command, end_del_expert_swfm)],
            SWFM_MYTICKET_CLOSED_END: [MessageHandler(Filters.text & ~Filters.command, swfm_myticket_closed_end)],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout),
            CallbackQueryHandler(timeout_with_inline)]},
        fallbacks=[CommandHandler('cancel', cancel),CommandHandler('batal', cancel)],conversation_timeout=90)
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
