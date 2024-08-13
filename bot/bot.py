import logging
import os
import telegram
# import json
from dotenv import load_dotenv
# from telegram.constants import ParseMode
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler
from config.config import *
from services import req_ticket, timeout, timeout_with_inline, req_ticket_add
from services.app_error.index import app_error
from datetime import datetime
import string
import random

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
    # username = update.message.from_user.username
    # chatid_telegram  = update.message.from_user.id 
    # grup_name = update.message.chat.title
    print(full_name)
    # query = update.callback_query
    # print(query)
    # query.answer()
    # chatid_telegram = update.message.from_user.id

    # Buat inline keyboard
    # keyboard = [
    #     [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(REQ_TICKET))],
    #     [InlineKeyboardButton("Tim Ahli >>", callback_data=str(MENU_REGISTRATION))],
    #     [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(MENU_REGISTRATION))],
    #     [InlineKeyboardButton("Broadcast Pesan", callback_data=str(MENU_REGISTRATION))],
    #     [InlineKeyboardButton("Jadikan Admin", callback_data=str(MENU_REGISTRATION))],
    #     [InlineKeyboardButton("Hapus UserBot", callback_data=str(MENU_REGISTRATION))],[InlineKeyboardButton("Download Laporan Tiket", callback_data=str(MENU_REGISTRATION))],
    #     [InlineKeyboardButton("My Ticket List", callback_data=str(MENU_REGISTRATION))],
    #     [InlineKeyboardButton("Eskalasi Case", callback_data=str(MENU_REGISTRATION))],
    #     [InlineKeyboardButton("Kembali", callback_data=str(MENU_REGISTRATION))]
    # ]
    # reply_markup = InlineKeyboardMarkup(keyboard)

    # Kirim pesan
    # bot_log.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.TYPING)
    # query.message.reply_text("Pilih :", reply_markup=reply_markup)

    # return REPORT_MENU

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    # print(user)
    update.message.reply_chat_action(action=telegram.constants.ChatAction.TYPING)
    update.message.reply_text(
        text=f"data User {user}",
        reply_markup=ReplyKeyboardRemove(),
        # parse_mode=ParseMode.MARKDOWN
    )
    return ConversationHandler.END

def end(udpate: Update, context: CallbackContext)-> None:
    user = Update.message.from_user
    now = datetime.now()
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    keterangan = update.message.text.replace(',',' ').replace(', ',' ').replace("'","").replace('"',"")
    
    # Create Ticket 
    char = list(string.digits)
    length = 10
    random.shuffle(char)
    password = []
    for i in range(length):
        password.append(random.choice(char))
    random.shuffle(password)
    
    ticket = f"IOM{password}"
    update.message.reply_chat_action(action=telegram.constants.ChatAction.TYPING)
    Update.message.reply_text(f"TICKET: {ticket}")
    button1 = InlineKeyboardButton("» Klik, join & diskusi", url=telegram_channel)
            # button2 = InlineKeyboardButton("Expert : Rosady" , url=username_expert)
    buttons = [[button1]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(f'⬇️ Klik dan Join Room dibawah ini untuk lacak tiket anda : *{ticket}*',parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard)

def main() -> None:
    updater = Updater(TOKEN_BOT)
    dispatcher = updater.dispatcher 
    # application = Application.builder().token(TOKEN_BOT).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
                REPORT_MENU: [
                    CallbackQueryHandler(req_ticket, pattern='^' + str(REQ_TICKET) + '$'),
                    CallbackQueryHandler(app_error, pattern='^' + str(REQ_APP_ERROR) + '$'),
                    CallbackQueryHandler(req_ticket_add, pattern='^' + str(REQ_TICKET_ADD) + '$'),
                    # CallbackQueryHandler(timeout_with_inline)
                ],
                END: [MessageHandler(Filters.text & Filters.command, end)],
                ConversationHandler.TIMEOUT: [
                    MessageHandler(Filters.text | Filters.command, timeout),
                    CallbackQueryHandler(timeout_with_inline)
                ]
            },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('batal', cancel)],
        conversation_timeout=os.getenv('TIMEOUT')
    )
    
    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
