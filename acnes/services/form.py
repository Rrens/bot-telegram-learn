import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from utils.helper import edit_message, delete_message
from config.config import *
import json
import pandas as pd
from database.db import get_app_by_ip_address

def form_index(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        select_data = query.data
        data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
        data = json.loads(data)
        for data in data['inline_keyboard']:
            if data['callback_data'] == select_data:
                data_text = str(data['text']).replace(" >>","")
        edit_message(query, data_text)
        
        keyboard = [
            [InlineKeyboardButton("Download Form >>", callback_data=str(DOWNLOAD_FORM))],
            [InlineKeyboardButton("Upload Form >>", callback_data=str(UPLOAD_FORM))],
            [InlineKeyboardButton("Kembali", callback_data=str(MAIN_MENU))]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        query.message.reply_text("Pilih :", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        
def download_form(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        select_data = query.data
        data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
        data = json.loads(data)
        for data in data['inline_keyboard']:
            if data['callback_data'] == select_data:
                data_text = str(data['text']).replace(" >>","")
        edit_message(query, data_text)
        
        query.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        query.message.reply_text("Form akan segera di unduh....")
        
        file_path = os.path.join(os.getcwd(), 'assets', 'Catalogue Teknis Infrastruktur Aplikasi dan Backup System.xlsx')
        context.bot.send_document(chat_id=query.message.chat_id, document=open(file_path, 'rb'))
        
        query.message.reply_text("Tekan /start untuk memulai bot kembali.")
        
        return ConversationHandler.END
        
    except Exception as e:
        print(f"Error: {e}")
        
def upload_form(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        select_data = query.data
        data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
        data = json.loads(data)
        for data in data['inline_keyboard']:
            if data['callback_data'] == select_data:
                data_text = str(data['text']).replace(" >>","")
        edit_message(query, data_text)
        
        query.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        query.message.reply_text("Silakan unggah FORM dalam bentuk CSV atau XLSX...")

        return HANDLE_UPLOAD_FORM
        
    except Exception as e:
        print(f"Error: {e}")
        
def handle_upload_form(update: Update, context: CallbackContext) -> None:
    try:
        # GET DOCUMENT
        document = update.message.document
        file_id = document.file_id
        
        # GET DOCUMENT FROM TELEGRAM SERVER
        file = context.bot.getFile(file_id)
        
        # Path for saving the file
        uploads_dir = os.path.join(os.getcwd(), 'assets', 'uploads')
        
        # Create 'uploads' directory if it doesn't exist
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        # Save file to local server
        file_path = os.path.join(uploads_dir, document.file_name)
        file.download(file_path)

        # Notify user that the file has been successfully uploaded
        update.message.reply_text(f"File '{document.file_name}' berhasil diunggah dan disimpan di server.")
        
        # Process the file based on its format (XLSX or CSV)
        if document.file_name.endswith('.xlsx'):
            data = pd.read_excel(file_path, engine="openpyxl")
            data = data.iloc[1:].reset_index(drop=True)
            update.message.reply_text(f"File XLSX berhasil dibaca! Jumlah baris: {data.shape[0]}")
            # update.message.reply_text(f"Contoh data:\n{data.head().to_string()}")
            print(data.shape)
        elif document.file_name.endswith('.csv'):
            data = pd.read_csv(file_path)
            update.message.reply_text(f"File CSV berhasil dibaca! Jumlah baris: {data.shape[0]}")
            update.message.reply_text(f"Contoh data:\n{data.head().to_string()}")
        else:
            update.message.reply_text('Harap unggah file dalam format CSV atau XLSX.')

        return ConversationHandler.END
    except Exception as e:
        print(f"Error: {e}")