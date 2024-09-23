import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.helper import edit_message, delete_message
from config.config import *
import json
from database.db import get_app_by_ip_address

def app_index(update: Update, context: CallbackContext): 
    try:
        query = update.callback_query
        # query.answer()
        select_data = query.data
        data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
        data = json.loads(data)
        for data in data['inline_keyboard']:
            if data['callback_data'] == select_data:
                data_text = str(data['text']).replace(" >>","")
        edit_message(query, data_text)
        
        keyboard = [
            [InlineKeyboardButton("Find APP >>", callback_data=str(FIND_APP))],
            [InlineKeyboardButton("Kembali", callback_data=str(MAIN_MENU))]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        query.message.reply_text("Pilih :", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")

def find_app(update: Update, context: CallbackContext): 
    try:
        query = update.callback_query
        # query.answer()
        select_data = query.data
        select_data = query.data
        data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
        data = json.loads(data)
        for data in data['inline_keyboard']:
            if data['callback_data'] == select_data:
                data_text = str(data['text']).replace(" >>","")
        edit_message(query, data_text)
        
        query.message.reply_text(text="Masukan IP atau Domain Aplikasi....",parse_mode=telegram.ParseMode.MARKDOWN)
        
        return SHOW_FIND_APP
    except Exception as e:
        print(f"Error: {e}")
        
def show_find_app(update: Update, _:CallbackContext) -> None:
    try:
        text_ip = update.message.text
        data = get_app_by_ip_address(text_ip)
        index_offset = 1
        response = ""
        print(f"Total Data")
        if data:
            print('ada')
            print(f"INI ROW NYA {data} DAN TOTAL DATANYA {len(data)}")
            response += f"Tenant Application: {data[0 + index_offset]}\n"
            response += f"Total Field: {data[1 + index_offset]}\n"
            response += f"Total Terisi: {data[2 + index_offset]}\n"
            response += f"TSA: {data[3 + index_offset]}\n"
            response += f"PIC Mitra: {data[4 + index_offset]}\n"
            response += f"No HP: {data[5 + index_offset]}\n"
            response += f"PIC AAM: {data[6 + index_offset]}\n"
            response += f"PIC Tsel: {data[7 + index_offset]}\n"
            response += f"PIC Tsel Dept Division: {data[8 + index_offset]}\n"
            response += f"Platform: {data[9 + index_offset]}\n"
            response += f"App Consolidation: {data[10 + index_offset]}\n"
            response += f"Vendor Principal: {data[11 + index_offset]}\n"
            response += f"Vendor Local Partner: {data[12 + index_offset]}\n"
            response += f"Tautan URL Akses: {data[13 + index_offset]}\n"
            response += f"Description: {data[14 + index_offset]}\n"
            response += f"Category: {data[14 + index_offset]}\n"
            response += f"APP version: {data[15 + index_offset]}\n"
            response += f"Device IP Address: {data[16 + index_offset]}\n"
            response += f"Host or Device Name: {data[17 + index_offset]}\n"
            response += f"Device Type: {data[18 + index_offset]}\n"
            response += f"OS: {data[19 + index_offset]}\n"
            response += f"Function: {data[20 + index_offset]}\n"
            response += f"Language: {data[21 + index_offset]}\n"
            response += f"CPU: {data[22 + index_offset]}\n"
            response += f"Memory: {data[23 + index_offset]}\n"
            response += f"Disk: {data[24 + index_offset]}\n"
            response += f"Backup and Recovery: {data[25 + index_offset]}\n"
            response += f"Integration with other app: {data[26 + index_offset]}\n"
            response += f"Pengguna Utama: {data[27 + index_offset]}\n"
            response += f"Jumlah pengguna: {data[28 + index_offset]}\n"
            response += f"Asset Type: {data[29 + index_offset]}\n"
            response += f"Asset Name: {data[30 + index_offset]}\n"
            response += f"Data Management: {data[31 + index_offset]}\n"
            response += f"Asset Owner: {data[32 + index_offset]}\n"
            response += f"Application Owner: {data[33 + index_offset]}\n"
            response += f"Public Facing: {data[34 + index_offset]}\n"
            response += f"Contain pii Data: {data[35 + index_offset]}\n"
            response += f"Data pii Detail: {data[36 + index_offset]}\n"
            response += f"URL: {data[37 + index_offset]}\n"
            response += f"Asset Site ID: {data[38 + index_offset]}\n"
            response += f"Asset Site Name: {data[39 + index_offset]}\n"
            response += f"Inhouse Vendor: {data[40 + index_offset]}\n"
            response += f"Access Management: {data[41 + index_offset]}\n"
            response += f"Documentation: {data[42 + index_offset]}\n"
            response += f"Status: {data[43 + index_offset]}\n"
            response += f"PIC App Ops Vendor Name: {data[44 + index_offset]}\n"
            response += f"PIC App Ops Vendor Email: {data[45 + index_offset]}\n"
            response += f"PIC App Ops Vendor Telp: {data[46 + index_offset]}\n"
            response += f"Periode PO TSA Nomor: {data[47 + index_offset]}\n"
            response += f"Periode PO TSA Awal: {data[48 + index_offset]}\n"
            response += f"Periode PO TSA Akhir: {data[49 + index_offset]}\n"
            response += f"Data State Statefull Stateless: {data[50 + index_offset]}\n"
            response += f"Function Load Balancer Mail Server Web Service Other: {data[51 + index_offset]}\n"
            response += f"Technology Stack Backend: {data[52 + index_offset]}\n"
            response += f"Technology Stack Mobile: {data[53 + index_offset]}\n"
            response += f"Technology Stack Frontend: {data[54 + index_offset]}\n"
            response += f"Technology Stack Database: {data[55 + index_offset]}\n"
            response += f"Database Architecture Clustered Standalone: {data[56 + index_offset]}\n"
            response += f"Downtime Yes No: {data[57 + index_offset]}\n"
            response += f"Priority 1 2 3 4: {data[58 + index_offset]}\n"
            response += f"Platform Platform: {data[59 + index_offset]}\n"
            response += f"Compatibility in Rhosp: {data[60 + index_offset]}\n"
            response += f"VM to VM or Openshift: {data[61 + index_offset]}\n"
            response += f"PHP CGI Remote Code Exec Vulnerability PHP Installed: {data[62 + index_offset]}\n"
            response += f"PHP CGI Remote Code Exec Vulnerability PHP Version: {data[63 + index_offset]}\n"
        else:
            print('gaada')
            # response = "IP/Domain tidak ditemukan"
        
        
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text('Berikut adalah detail App: \n\n{}'.format(response))
    except Exception as e:
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text("IP/Domain tidak ditemukan")
        print(f"Error: {e}")