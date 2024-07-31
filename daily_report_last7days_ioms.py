from dataclasses import dataclass
from urllib import response
from datetime import datetime,timedelta
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,CallbackContext
import telegram
import os
import clickhouse_connect
from collections import Counter


os.environ['https_proxy'] = 'https://10.37.190.29:8080'
os.environ['HTTPS_PROXY'] = 'https://10.37.190.29:8080'

syanticbot = telegram.Bot('1087167235:AAGahG5GsxkffRCbns9S-aXwklzyGYHlpME')
# chatid = {'Group Internal':'462124845'}
chatid = {'Group Internal':'-1002122441022'}
# 
def generate_text_report(response):
    today = datetime.now()
    today = today.strftime("%d-%m-%Y %H:%M:%S WIB")
    today = datetime.now()
    query_year = today.strftime("%Y")

    client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
    query = f"""SELECT * FROM production.helpdesk_report_swfm WHERE category = 'IOMS' and parseDateTime32BestEffortOrNull(replace(replace(open_ticket_date, ' WIB', ''), ',', '')) >= timestamp_sub(hour, 168, now()) ORDER BY parseDateTime32BestEffortOrNull(replace(replace(open_ticket_date, ' WIB', ''), ',', '')) ASC"""
    data = client.command(query)
    data_list = str(data).replace("[","").replace("]","").replace("'","").replace("2023,","2023 ").replace("\\\\n",' ').split('\\n')
    
    count_open_swfm = []
    count_closed_swfm = []
    for data in data_list:
        data = str(data).split(', ')
        if 'open' in data:
            count_open_swfm.append(data[16])
        if 'closed' in data:
            count_closed_swfm.append(data[16])
    today = datetime.now()
    today = today.strftime("%d-%m-%Y %H:%M:%S WIB")
    text = ''
    text += '🪧 *Daily Report "Lapor Kendala" IOMS Last 24 Hours*\n'
    text += f'📆 Last Updated : {today}\n\n'
    text += f'📘 Total All Ticket : {len(count_open_swfm)+len(count_closed_swfm)}\n'
    text += f'📗 Open : {len(count_open_swfm)}\n'
    text += f'📕 Closed : {len(count_closed_swfm)}\n\n'
    
    query = f"SELECT * FROM production.helpdesk_report_swfm WHERE category = 'IOMS' and parseDateTime32BestEffortOrNull(replace(replace(open_ticket_date, ' WIB', ''), ',', '')) >= timestamp_sub(hour, 24, now()) ORDER BY parseDateTime32BestEffortOrNull(replace(replace(open_ticket_date, ' WIB', ''), ',', '')) ASC"
    data = client.command(query)
    data_list_swfm = str(data).replace("[","").replace("]","").replace("'","").replace("2023,","2023 ").replace("2025,","2025 ").replace("\\\\n",' ').split('\\n')
    
    text += f'🎟 *Ticket by Category : (Open|Closed|Total)* \n'
    try:
        count_open_swfm = []
        count_closed_swfm = []
        x = []
        for data in data_list_swfm:
            data = str(data).split(', ')
            problem_title = str(data[14]).split(' ➞ ')[0]
            if 'open' in data:
                count_open_swfm.append(problem_title)
                x.append(problem_title)
            if 'closed' in data:
                count_closed_swfm.append(problem_title)
                x.append(problem_title)

        counter_open = Counter(count_open_swfm)
        counter_closed = Counter(count_closed_swfm)
        counter_total = Counter(x)

        sourted_closed = counter_closed.most_common()
        sourted_open = counter_open.most_common()
        sourted_total = counter_total.most_common()
        x = []
        for nama_total, jumlah_total in sourted_total:
            for name_open, jumlah_open in sourted_open:
                if nama_total == name_open:
                    x.append(name_open)
                    text += f'{name_open} : ({jumlah_open}|{jumlah_total-jumlah_open}|{jumlah_total})\n'
        for name_closed, jumlah_closed in sourted_closed:
            if name_closed not in x:
                jumlah_open = 0
                text += f'{name_closed} : ({jumlah_open}|{jumlah_closed}|{jumlah_open+jumlah_closed})\n'
    except:
        text += '✅ Ticket Not Found\n'
    text += '\n'

    text += f'🎟 *Ticket by Sub-Category : (Open|Closed|Total)* \n'
    try:
        count_open_swfm = []
        count_closed_swfm = []
        x = []
        for data in data_list_swfm:
            data = str(data).split(', ')
            problem_title = str(data[14]).split(' ➞ ')[0]
            if problem_title != 'Other Problems':
                problem_case = str(data[14]).split(' ➞ ')[1]
                if 'open' in data:
                    count_open_swfm.append(problem_case)
                    x.append(problem_case)
                if 'closed' in data:
                    count_closed_swfm.append(problem_case)
                    x.append(problem_case)
            else:
                problem_case = str(data[14]).replace(' ➞ Other Problems','')
                if 'open' in data:
                    count_open_swfm.append(problem_case)
                    x.append(problem_case)
                if 'closed' in data:
                    count_closed_swfm.append(problem_case)
                    x.append(problem_case)

        counter_open = Counter(count_open_swfm)
        counter_closed = Counter(count_closed_swfm)
        counter_total = Counter(x)

        sourted_closed = counter_closed.most_common()
        sourted_open = counter_open.most_common()
        sourted_total = counter_total.most_common()
        x = []
        for nama_total, jumlah_total in sourted_total:
            for name_open, jumlah_open in sourted_open:
                if nama_total == name_open:
                    x.append(name_open)
                    text += f'{name_open} : ({jumlah_open}|{jumlah_total-jumlah_open}|{jumlah_total})\n'
        for name_closed, jumlah_closed in sourted_closed:
            if name_closed not in x:
                jumlah_open = 0
                text += f'{name_closed} : ({jumlah_open}|{jumlah_closed}|{jumlah_open+jumlah_closed})\n'
    except:
        text += '✅ Ticket Not Found\n'
    text += '\n'


    text += '\nRegards\nOCHABOT & Team'
    print('Sukses Terkirim')
    return text

def send_message(text, chat_id):
    # pass
    print(text, chat_id)
    # syanticbot.send_message(chat_id, text=text,parse_mode = telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    # syanticbot.pin_chat_message(chat_id, msg.message_id)    


for data_chatid in chatid:
    # print('send to bot on group {}'.format(data_chatid))
    if ( isinstance(chatid[data_chatid], list) ):
        for chat_id in chatid[data_chatid]:
            send_message(generate_text_report(response), chat_id)
    else:
        send_message(generate_text_report(response), chatid[data_chatid])