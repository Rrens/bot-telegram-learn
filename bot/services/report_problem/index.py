import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import os
import json
from config.config import *
from utils.helper import edit_message, delete_message

def report_problem(update: Update, context: CallbackContext) -> None:
    try:
        
        query = update.callback_query
        query.answer()
        edit_message(query, "LAPORAN KENDALA")
        
        keyboard = [
            [InlineKeyboardButton("Aplication Error >>", callback_data=str(CREATE_TICKET))],
            [InlineKeyboardButton("Acceptance >>", callback_data=str(ACCEPTANCE))],
            [InlineKeyboardButton("Budget >>", callback_data=str(BUDGET))],
            [InlineKeyboardButton("Deployment >>", callback_data=str(DEPLOYMENT))],
            [InlineKeyboardButton("Issue Partial Baut >>", callback_data=str(ISSUE_PARTIAL_BAUT))],
            [InlineKeyboardButton("Process >>", callback_data=str(PROCESS))],
            [InlineKeyboardButton("Download Laporan Tiket", callback_data=str(PROFESSIONAL_TEAM))],
            [InlineKeyboardButton("Login >>", callback_data=str(LOGIN))],
            [InlineKeyboardButton("Dashboard >>", callback_data=str(DASHBOARD))],
            [InlineKeyboardButton("Tasklist >>", callback_data=str(TASKLIST))],
            [InlineKeyboardButton("Planning >>", callback_data=str(PLANNING))],
            [InlineKeyboardButton("Knowledge >>", callback_data=str(KNOWLEDGE))],
            [InlineKeyboardButton("eligibility Check >>", callback_data=str(ELIGIBILITY_CHECK))],
            [InlineKeyboardButton("Kembali", callback_data=str(MAIN_MENU))]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        query.message.reply_text("Penjelasan Kategori: \n*ANT :* *TOTI ➞ Create Ticket, TOTI ➞ View File Evidence, RPM ➞ Approval Ticket, RPM ➞ View File Evidence*\n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*BPS Manual :* Cant Submit Ticket, Menu Error, Service Variable Activity, BPS Ticket Not Appearing\n*CGL (IMBAS PETIR) :* Data Not Synchrone, Menu Error, Interference Lightning Claim\n*Cant Check In :* Site Refference, Ticketing Handling, Teritory Operation, TS Manual\n*KPI :* Data Not Found, Data Not Synchrone, Menu Error, Requests Takeout Ticket\n*Master Data Management :* *Site List Management ➞ Area, Site List Management ➞ Cluster, Site List Management ➞ Longlat, Site List Management ➞ NOP, Site List Management ➞ Regional, Site List Management ➞ Site Class, Site List Management ➞ Site Name, Site List Management ➞ Site Owner, Site List Management ➞ Site Type*\n*Mobile :* Change Role, Connection, Data Not Found, Data Not Synchrone, Daya Listrik, GPS Error, Knowladge, Menu Error, Register with Another Device\n*Performance :* *eBAIP ➞ Export BAIP, eBAIP ➞ Fill Form BAIP, eBAPP ➞ Signature Configuration, eBAPP ➞ Submit BAPP, eBAPP ➞ Fill Form BAPP, eKPI ➞ Submit KPI*\n*Preventive Maintenance :* Data Not Synchrone, Menu Error, New Menu, Cant Approve, Cant Follow Up, Genset, Sampling, Site, *SPlanning ➞ Approval, SPlanning ➞ Menu Error, SPlanning ➞ Change Schedule, SPlanning ➞ Notification Error, SPlanning ➞ Login, SPlanning ➞ Add Site, SPlanning ➞ Take Out Site, SPlanning ➞ Switch Site, SPlanning ➞ Change Date, SPlanning ➞ Extend Permit, SPlanning ➞ Print Permit*\n*RH Visit :* Cant Follow Up Ticket, Data Not Synchrone, Cant Approve, Menu Error\n*Site Refference :* Change Area, Data Not Found\n*Teritory Operation :* Add Area, Data Not Synchrone, Data Site Wrong\n*Ticketing Handling : *Alarm Ticket, Cant Approve, Cant Close, Change Area, Clear Time Delay, Data Not Found, Data Not Synchrone, Menu MBP Error, Import Area, Menu Error, Menu TS Error, Wrong Mapping Ticket, *Personal Tracking ➞ Info Clock In or Clock Out TO, Personal Tracking ➞ Tickets Handled, Personal Tracking ➞ Export, Fault Center ➞ Export PDF, Fault Center ➞ Manual Dispatch, Fault Center ➞ Escalate to INSERA TELKOM, Fault Center ➞ Escalate to TP Site Owner, Fault Center ➞ Update RCA, Fault Center ➞ Resolved Ticket, SVA ➞ Create Ticket, SVA ➞ Export Ticket, SVA ➞ Update Draft Ticket*\n*TPAS :* *Permit Approval ➞ Approval Permit, Permit Approval ➞ View Detail Permit, Permit Approval ➞ Search Permit*\n*TS Manual : *Menu Error\n*User Management : *Change Area User, Change Role, Invalid Email, Invalid Password, Menu Error, New User, Registered with Another Device, Req Double Area, Reset Password, User Not Found, Delete User, *Manage User Mobile ➞ Change Data User Mobile, Manage User Mobile ➞ Add User Mobile*\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
        query.message.reply_text("Pilih :", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        
    # return MENU_REPORT

def request_ticket(update: Update, _: CallbackContext) -> None:
    try:
        print('INI LAGI')
        query = update.callback_query
        select_data = query.data
        data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
        data = json.loads(data)
        # print(data)
        for data in data['inline_keyboard']:
            if data['callback_data'] == select_data:
                data_text = str(data['text']).replace(" >>","")
        chat_id = update.callback_query.message.chat_id
        message_id_1 = update.callback_query.message.message_id-1
        delete_message(chat_id, message_id_1)
        edit_message(query, data_text)
        print(f"--------- Request Ticket {data_text}")
        
        if 'Aplication Error' in data_text:
            print('ini')
            keyboard = [
                [InlineKeyboardButton("Loading after Login (Loading Setelah Login)", callback_data=str(REQUEST_TICKET_END_APP_ERR_1))],
                [InlineKeyboardButton("Log out Yourself (Logout Sendiri)", callback_data=str(REQUEST_TICKET_END_APP_ERR_2))],
                [InlineKeyboardButton("Hang (Gantung)", callback_data=str(REQUEST_TICKET_END_APP_ERR_3))],
                # [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali ke Menu", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Acceptance' in data_text:
            keyboard = [
                [InlineKeyboardButton("Add Case (Semua Kasus Tambah) >>", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Cancel Case (Semua Kasus Batal) >>", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Change Case (Semua Kasus Perubahan) >>", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Document Case (Semua Kasus Dokumen) >>", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Error Case (Semua Kasus Kesalahan) >>", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Generate Case (Semua Kasus Generate) >>", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Requests Case (Semua Kasus Permintaan) >>", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Submit & Resubmit Case (Semua Kasus Kirim & Kirim Ulang) >>", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Update Case (Semua Kasus Update) >>", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Approval RFI (Persetujuan RFI)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("BOQ List Empty (Daftar BOQ Kosong)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Database Timeout Query (Kueri Batas Waktu Database)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Duplicate SOWID (Duplikat SOWID)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Fallback Status eOA (Status Penggantian eOA)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Guideline (Pedoman)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Propose Milestone (Usulkan Tonggak Pencapaian)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Request OA (Permintaan OA)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Reviewer User (Pengguna Peninjau)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Signature Blank (Tanda Tangan Kosong)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Status Workflow (Alur Kerja Status)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Sync NEID (Sinkronkan NEID)", callback_data=str(MAIN_MENU))],
                # [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Penjelasan Kategori: \n*Add Case :* Add Menu, Add User\n*Cancel Case :* Cancel ATP, Cancel BOQ, Cancel eATP\n*Change Case :* Change Approval QC, Change BOQ\n*Document Case :* Document Not Appearing, Document Not Synchrone, Document Workflow \n*Error Case :* Error Data, Error Database, Error Document, Error Download Data, Error Export Data, Error Generate ATP, Error Generate QC, Error Generate SQAC, Error Input Data, Error Menu, Error Submit ATP, Error Submit ELV, Error Upload BOQ, Error User\n*Generate Case :* Cant Generate QC, Cant Generate ATP, Cant Generata eOA, Cant Generata QC\n*Requests Case :* Request BOQ, Request Cancel, Request Delete eMOM, Request Delete LV, Request Delete MOS, Request Mapping SOWID, Request New Menu, Request Reupload ATP, Request User\n*Submit & Resubmit Case :* Cant Submit eLV, Cant Resubmit OA\n*Update Case :* Update ATP, Update Data, Update Database, Update Menu, Update NE ID, Update PO, Update SOW\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*",parse_mode=telegram.ParseMode.MARKDOWN)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Deployment' in data_text:
            keyboard = [
                [InlineKeyboardButton("Add Menu (Tambah Menu)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Document Workflow (Alur Kerja Dokumen)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Error Data (Kesalahan Data)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Error Download Data (Kesalahan Unduh Data)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Error Export Data (Kesalahan Ekspor Data)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Error Login (Kesalahan Gabung)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Error Menu (Kesalahan Menu)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Request Delete Milestone (Permintaan Hapus Tonggak Pencapaian)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Request New Menu (Permintaan Menu Baru)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Status Workflow (Alur Kerja Status)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Process' in data_text:
            keyboard = [
                [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Request Mapping SOWID (Permintaan Pemetaan SOWID)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Issue Partial Baut' in data_text:
            keyboard = [
                [InlineKeyboardButton("Request Milestone (Permintaan Tonggak Pencapaian)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Login' in data_text:
            keyboard = [
                [InlineKeyboardButton("Add User (Tambah User)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Cant Login (Tidak Dapat Gabung)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Dashboard' in data_text:
            keyboard = [
                [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Duplicate Site (Situs Duplikat)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Duplicate SOWID (Duplikat SOWID)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Request New Menu (Permintaan Menu Baru)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Status Workflow (Alur Kerja Status)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Tasklist' in data_text:
            keyboard = [
                [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Document Workflow (Alur Kerja Dokumen)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Duplicate eLV (Duplikat eLV)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Duplicate eOA (Duplikat eOA)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Error Duplicate ATP (Kesalahan Duplikat ATP)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Error Menu (Kesalahan Menu)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Status Workflow (Alur Kerja Status)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Planning' in data_text:
            keyboard = [
                [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Document Workflow (Alur Kerja Dokumen)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Request Delete eMOM (Permintaan Hapus eMOM)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Request Delete Site List (Permintaan Hapus Daftar Situs)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Request Take Out eKKST (Permintaan Hapus eKKST)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Update Data (Perbaharui Data)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Update Menu (Perbaharui Manu)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Update NE ID (Perbaharui NE ID)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Knowledge' in data_text:
            keyboard = [
                [InlineKeyboardButton("Update Menu (Perbaharui Menu)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Eligibility Check' in data_text:
            keyboard = [
                [InlineKeyboardButton("Data Not Synchrone (Data Tidak Sinkron)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Budget' in data_text:
            keyboard = [
                [InlineKeyboardButton("Capex Balance (Saldo Belanja Modal)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Justification (Pembenaran)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("FBP (KBR/KPAA) (FBP (KBR/KPAA))", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Corsec (Corsec)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Reporting (Laporan)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Other Problems (Lainnya)", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
        elif 'Other Problems' in data_text:
            chatid_telegram = update.callback_query.from_user.id

            # client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            # query = f"select problem_title from production.helpdesk_bot_swfm where chatid_telegram = {chatid_telegram}"
            # data_select = client.command(query)
            # client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            # query = f"ALTER TABLE production.helpdesk_bot_swfm update problem_title = '{data_select}' where chatid_telegram = '{chatid_telegram}'"
            # client.command(query)
            
            # client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')
            # query = f"ALTER TABLE production.helpdesk_bot_swfm update channel_chatid = 'None', ticket = 'None',problem_summary = 'None', status = 'None', category = 'None', open_ticket_date = 'None', fcaps = 'None', action_menu = 'None', action_category = 'None', action_handle_by = 'None', action_resolution = 'None', post_link = 'None', regional = 'None' WHERE chatid_telegram = '{chatid_telegram}'"
            # client.command(query)
            query = update.callback_query
            query.answer()
            query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
            return END
        elif 'TANYA PROSES ?' in data_text:
            keyboard = [
                [InlineKeyboardButton("Acceptance", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Budget", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Deployment", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Issue Partial Baut", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Process", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Login", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Dashboard", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Tasklist", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Planning", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Knowledge", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Eligibility Check", callback_data=str(MAIN_MENU))],
                [InlineKeyboardButton("Kembali", callback_data=str(REPORT_PROBLEM))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text("Pilih :",reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")

def request_ticket_end(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    # print(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    chat_id = query.message.chat_id
    message_id = query.message.message_id - 1
    delete_message(chat_id, message_id)
    edit_message(query, data_text)
    print(f"--------- Request End {data_text}")
    try:
        query.message.reply_text(text="Masukkan ringkasan rinci masalah....\n\n#Note : Upload evidence problem setelah buat laporan",parse_mode=telegram.ParseMode.MARKDOWN)
        return END
    except Exception as e:
        print('------------------------------------------------------------------------')
        print(f"Error REQUEST TICKET END: {e}")
        print('------------------------------------------------------------------------')
        return END