import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import os
import json
from config.config import *

async def req_ticket(update: Update, context: CallbackContext) -> None:
    # print('okeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    
    query = update.callback_query
    select_data = query.data
    print(f"INI LOO {select_data}")
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    # data = json.loads(data)
    # for data in data['inline_keyboard']:
    #     if data['callback_data'] == select_data:
    #         data_text = str(data['text']).replace(" >>","")
    
    keyboard = [
        [InlineKeyboardButton("Application Error >>", callback_data=str(REQ_APP_ERROR))],
        [InlineKeyboardButton("Acceptance >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Budget >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Deployment >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Issue Partial Baut >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Process >>", callback_data=str(MENU_REGISTRATION))],[InlineKeyboardButton("Download Laporan Tiket", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Login >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Dashboard >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Tasklist >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Planning >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Knowledge >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("eligibility Check >>", callback_data=str(MENU_REGISTRATION))],
        # [InlineKeyboardButton("Kembali", callback_data=str(REPORT_MENU))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query = update.callback_query
    await query.answer()  # Mengkonfirmasi bahwa callback query telah diterima
    # print(query)
    message_id = query.message.message_id+1
    chat_id = update.callback_query.from_user.id
    # await bot_log.delete_message(chat_id,message_id)
    
    # await query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    await query.message.reply_text("Penjelasan Kategori: \n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*Acceptance :* Add Case, Cancel Case, Change Case, Document Case, Error Case, Generate Case, Requests Case, Submit & Resubmit Case, Update Case, Approval RFI, BOQ List Empty, Data Not Synchrone, Database Timeout Query, Duplicate SOWID, Fallback Status eOA, Guideline, Propose Milestone, Request OA, Reviewer User, Signature Blank, Status Workflow, Sync NEID\n*Budget :* Capex Balance, Justification, FBP (KBR/KPAA), Corsec, Reporting\n*Deployment :* Add Menu, Data Not Synchrone, Document Workflow, Error Data, Error Download Data, Error Export Data, Error Login, Error Menu, Request Delete Milestone, Request New Menu, Status Workflow\n*Issue Partial Baut :* Request Milestone\n*Process :* Data Not Synchrone, Request Mapping SOWID\n*Login :* Add User, Cant Login\n*Dashboard :* Data Not Synchrone, Duplicate Site, Duplicate SOWID, Request New Menu, Status Workflow\n*Tasklist :* Data Not Synchrone, Document Workflow, Duplicate eLV, Duplicate eOA, Error Duplicate ATP, Error Menu, Status Workflow\n*Planning :* Data Not Synchronice, Document Workflow, Request Delete eMOM, Request Delete Site List, Request Take Out eKKST, Update Data, Update Menu, Update NE ID\n*Knowledge :* Update Menu\n*Eligibility Check :* Data Not Synchrone\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*")
    # await query.message.reply_text(f"INI YANG DIPILIH {select_data}")
    await query.message.reply_text("Pilih :",reply_markup=reply_markup)
    
async def req_ticket_add(update: Update, _: CallbackContext) -> None:
    chatid_telegram = update.callback_query.from_user.id
    query = update.callback_query
    select_data = query.data
    reply_markup = query.message.reply_markup.inline_keyboard

    for row in reply_markup:
        for button in row:
            if button.callback_data == select_data:
                data_text = button.text.replace(" >>", "")
                await query.message.reply_text(data_text)
    
    await query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan")
    return END
