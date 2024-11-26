import logging
import os
import telegram
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler
from config.config import *
from services import timeout, timeout_with_inline
from services.report_problem import report_problem, request_ticket, request_ticket_end
from services.expert_team import expert_team, reg_expert, end_reg_expert, end_del_reg_expert
from datetime import datetime
from services.log_bot import log_bot, log_bot_success
import string
import random
import time
from database.db import get_current_data_helpdesk, get_check_admin_or_not, get_ticket_data_helpdesk, get_id_data_helpdesk, alter_problem_summary, insert_helpdesk_report, get_count_ioms, get_expert
from utils.helper import edit_message, delete_message

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

chatid_app = '-1002137089074'

bot_log = telegram.Bot(token=TOKEN_BOT)

def start(update: Update, _: CallbackContext) -> None:
    try:
        user = update.message.from_user
        full_name = user.full_name
        chatid_telegram = user.id 
        data = get_current_data_helpdesk(chatid_telegram)
        if data:
            check_admin = get_check_admin_or_not(chatid_telegram)
            position = check_admin == 'admin'
            if position is True:
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(REPORT_PROBLEM))],
                    [InlineKeyboardButton("Tim Ahli >>", callback_data=str(PROFESSIONAL_TEAM))],
                    [InlineKeyboardButton("Status Laporan (Admin) >>", callback_data=str(REPORT_STATUS))],
                    [InlineKeyboardButton("Broadcast Pesan >>", callback_data=str(MESSAGE_BROADCAST))],
                    [InlineKeyboardButton("Jadikan Admin >>", callback_data=str(MAKE_ADMIN))],
                    [InlineKeyboardButton("Hapus UserBot >>", callback_data=str(DELETE_USER))],
                    [InlineKeyboardButton("Download Laporan Tiket >>", callback_data=str(DOWNLOAD_REPORT_TICKET))],
                    [InlineKeyboardButton("My Ticket List >>", callback_data=str(TICKET_LIST))],
                    [InlineKeyboardButton("Eskalasi Case >>", callback_data=str(CASE_ESCALATION))],
                ]
            else:
                keyboard = [
                    [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(REPORT_PROBLEM))],
                    [InlineKeyboardButton("Status Laporan >>", callback_data=str(REPORT_STATUS))],
                    [InlineKeyboardButton("My Ticket List >>", callback_data=str(TICKET_LIST))],
                    [InlineKeyboardButton("Eskalasi Case >>", callback_data=str(CASE_ESCALATION))],
                ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Halo {}! Selamat datang di bot kami. Silakan gunakan perintah yang tersedia.'.format(full_name), reply_markup=reply_markup)
            
            return MENU
        else:
            update.message.reply_text(f"Mohon registrasi Menu IOMS terlebih dahulu. Klik /start",parse_mode=telegram.ParseMode.MARKDOWN)
        
    except Exception as e:
        print(f"Error: {e}")


def main_menu(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    chat_id = update.callback_query.message.chat_id
    message_id_1 = update.callback_query.message.message_id-1
    edit_message(query, "HOME")
    delete_message(chat_id, message_id_1)
    
    username = update.callback_query.from_user.username
    
    keyboard = [
        [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(REPORT_PROBLEM))],
        [InlineKeyboardButton("Tim Ahli >>", callback_data=str(PROFESSIONAL_TEAM))],
        [InlineKeyboardButton("Status Laporan (Admin) >>", callback_data=str(REPORT_STATUS))],
        [InlineKeyboardButton("Broadcast Pesan >>", callback_data=str(MESSAGE_BROADCAST))],
        [InlineKeyboardButton("Jadikan Admin >>", callback_data=str(MAKE_ADMIN))],
        [InlineKeyboardButton("Hapus UserBot >>", callback_data=str(DELETE_USER))],
        [InlineKeyboardButton("Download Laporan Tiket >>", callback_data=str(DOWNLOAD_REPORT_TICKET))],
        [InlineKeyboardButton("My Ticket List >>", callback_data=str(TICKET_LIST))],
        [InlineKeyboardButton("Eskalasi Case >>", callback_data=str(CASE_ESCALATION))],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    # update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    # update.message.reply_text('Halo {}! Selamat datang di bot kami. Silakan gunakan perintah yang tersedia.'.format(full_name), reply_markup=reply_markup)
    query.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    query.message.reply_text(f"Halo {username}! Selamat datang di bot kami. Silakan gunakan perintah yang tersedia.", reply_markup=reply_markup)
    
    return MENU

def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Terima kasih telah akses di *Assitance OCHA BOT*\nKlik /start', reply_markup=ReplyKeyboardRemove(),parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END

def end(update: Update, _: CallbackContext) -> None:
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
    # client = clickhouse_connect.get_client(database="production",host='10.54.18.55', port=8123, username='app_aam_dashboard', password='AAMDashboard#2024')

    ticket = "IOM"+"".join(password)
    data = get_current_data_helpdesk(chatid_telegram)
    status = []
    val_check_ticket = data[3] == ticket
    status.append(val_check_ticket)
    if status[0] is False:
        alter_problem_summary(ticket, keterangan, date_time, chatid_telegram)
        
        data_select = get_current_data_helpdesk(chatid_telegram)
        # print(data_select)
        insert_helpdesk_report(data_select)
        time.sleep(2)
        
        ticket_status = get_ticket_data_helpdesk(chatid_telegram)
        
        print(f"TIKET STATUS {ticket_status}")
        
        check_count = get_count_ioms()
        print(f"CEK IOMS {check_count}")
        check_count = check_count == 0
        if check_count is True:
            # print('cek 1')
            username_expert = 'https://t.me/puang_ocha'
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
        else:
            # print('cek 2')
            expert = []
            data = get_expert()
            expert.append(data)
            expert = str(expert).replace('[','').replace(']','').replace("'",'').split('\\n')
            expert = expert[0]
            username_expert = 'https://t.me/{}'.format(expert)
            telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
            button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            buttons = [[button1]]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket_status}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
            
    elif status[0] is True:
        characters = list(string.digits)
        length = 10
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        ticket = "IOM"+"".join(password)
        alter_problem_summary(ticket, keterangan, date_time, chatid_telegram)
        
        time.sleep(2)
        data_select = get_current_data_helpdesk(chatid_telegram)
        insert_helpdesk_report(data_select)
        
        time.sleep(2)
        data = get_ticket_data_helpdesk(chatid_telegram)
        ticket_status = data
        data = get_expert('IOMS')
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
            data = get_expert('IOMS')
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
    log_bot(update)
    log_bot_success(update, '*Tiket* ➞ Telah Membuat Tiket 🎟')
    
    return ConversationHandler.END


def main() -> None:
    updater = Updater(TOKEN_BOT)
    dispatcher = updater.dispatcher
    
    timeout_time = 30
    
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            MENU: [
                # # # Report Problem
                CallbackQueryHandler(main_menu, pattern='^' + str(MAIN_MENU) + '$'),
                CallbackQueryHandler(report_problem, pattern='^' + str(REPORT_PROBLEM) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(CREATE_TICKET) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(ACCEPTANCE) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(BUDGET) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(DEPLOYMENT) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(ISSUE_PARTIAL_BAUT) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(PROCESS) + '$'),
                CallbackQueryHandler(expert_team, pattern='^' + str(PROFESSIONAL_TEAM) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(LOGIN) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(DASHBOARD) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(TASKLIST) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(PLANNING) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(KNOWLEDGE) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(ASK_PROCESS) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(ELIGIBILITY_CHECK) + '$'),
                
                # APP ERROR
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_APP_ERR_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_APP_ERR_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_APP_ERR_3) + '$'),
                
                #DEPLOYMENT
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_3) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_4) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_5) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_6) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_7) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_8) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_9) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_10) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_11) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DEPLOYMENT_12) + '$'),
                
                # ACCEPTANCE
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_3) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_4) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_5) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_6) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_7) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_8) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_9) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_10) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_11) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_12) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_13) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_14) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_15) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_16) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_17) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_18) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_19) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_20) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_21) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ACCEPTANCE_22) + '$'),
                
                # BUDGET
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_BUDGET_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_BUDGET_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_BUDGET_3) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_BUDGET_4) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_BUDGET_5) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_BUDGET_6) + '$'),
                
                # ISSUE PARTIAL BAUT
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ISSUE_PARTIAL_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ISSUE_PARTIAL_2) + '$'),
                
                # PROCESS
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PROCESS_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PROCESS_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PROCESS_3) + '$'),
                
                # LOGIN
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_LOGIN_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_LOGIN_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_LOGIN_3) + '$'),
                
                # Dashboard
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DASHBOARD_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DASHBOARD_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DASHBOARD_3) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DASHBOARD_4) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DASHBOARD_5) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_DASHBOARD_6) + '$'),
                
                # Tasklist
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_TASKLIST_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_TASKLIST_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_TASKLIST_3) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_TASKLIST_4) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_TASKLIST_5) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_TASKLIST_6) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_TASKLIST_7) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_TASKLIST_8) + '$'),
                
                # Planning
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PLANNING_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PLANNING_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PLANNING_3) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PLANNING_4) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PLANNING_5) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PLANNING_6) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PLANNING_7) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PLANNING_8) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_PLANNING_9) + '$'),
                
                # Knowledge
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_KNOWLEDGE_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_KNOWLEDGE_2) + '$'),
                
                # Eligibility 
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ELIGIBILITY_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_ELIGIBILITY_2) + '$'),
                
                # # # Expert Team
                CallbackQueryHandler(expert_team, pattern='^' + str(EXPERT_TEAM) + '$'),
                CallbackQueryHandler(reg_expert, pattern='^' + str(REG_EXPERT) + '$'),
                # CallbackQueryHandler(end_reg_expert, pattern='^' + str(END_EXPERT) + '$'),
            ],
            END_EXPERT: [MessageHandler(Filters.text & ~Filters.command, end_reg_expert)],
            END_DEL_EXPERT: [MessageHandler(Filters.text & ~Filters.command, end_del_reg_expert)],
            END: [MessageHandler(Filters.text & ~Filters.command, end)],
            # MENU_REPORT: [
            #     CallbackQueryHandler(main_menu, pattern='^' + str(MAIN_MENU) + '$'),
            #     CallbackQueryHandler(report_problem, pattern='^' + str(REPORT_PROBLEM) + '$'),
            # ],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout),
            CallbackQueryHandler(timeout_with_inline)
            ],
        },
        
        fallbacks = [CommandHandler('cancel', cancel), CommandHandler('batal', cancel)],
        conversation_timeout = int(timeout_time)
    )
    
    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
