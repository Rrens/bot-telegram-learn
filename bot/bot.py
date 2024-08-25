import logging
import os
import telegram
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler
from config.config import *
from services import timeout, timeout_with_inline
from services.report_problem import report_problem, request_ticket, request_ticket_end
from datetime import datetime
import string
import random
from utils.helper import edit_message, delete_message

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN_BOT = os.getenv('TOKEN_BOT')
bot_log = telegram.Bot(token=TOKEN_BOT)

def start(update: Update, _: CallbackContext) -> None:
    full_name = update.message.from_user.full_name
    
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
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Halo {}! Selamat datang di bot kami. Silakan gunakan perintah yang tersedia.'.format(full_name), reply_markup=reply_markup)
    
    return MENU


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
    status = []
    # query = f"select * from production.helpdesk_bot_swfm where chatid_telegram = '{chatid_telegram}'"
    # data = client.command(query)
    # val_check_ticket = data[3] == ticket
    # status.append(val_check_ticket)
    telegram_channel = "https://t.me/+3pmsEG9xTtw3ZTc1"
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
    buttons = [[button1]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)
    return ConversationHandler.END

def main() -> None:
    updater = Updater(TOKEN_BOT)
    dispatcher = updater.dispatcher 
    
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            MENU: [
                CallbackQueryHandler(main_menu, pattern='^' + str(MAIN_MENU) + '$'),
                CallbackQueryHandler(report_problem, pattern='^' + str(REPORT_PROBLEM) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(CREATE_TICKET) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(ACCEPTANCE) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(BUDGET) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(DEPLOYMENT) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(ISSUE_PARTIAL_BAUT) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(PROCESS) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(PROFESSIONAL_TEAM) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(LOGIN) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(DASHBOARD) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(TASKLIST) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(PLANNING) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(KNOWLEDGE) + '$'),
                CallbackQueryHandler(request_ticket, pattern='^' + str(ELIGIBILITY_CHECK) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_APP_ERR_1) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_APP_ERR_2) + '$'),
                CallbackQueryHandler(request_ticket_end, pattern='^' + str(REQUEST_TICKET_END_APP_ERR_3) + '$'),
            ],
            END: [MessageHandler(Filters.text & ~Filters.command, end)],
            # MENU_REPORT: [
            #     CallbackQueryHandler(main_menu, pattern='^' + str(MAIN_MENU) + '$'),
            #     CallbackQueryHandler(report_problem, pattern='^' + str(REPORT_PROBLEM) + '$'),
            # ],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)]
        },
        
        fallbacks = [CommandHandler('cancel', cancel), CommandHandler('batal', cancel)],
        conversation_timeout = int(os.getenv('TIMEOUT', 30))
    )
    
    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
