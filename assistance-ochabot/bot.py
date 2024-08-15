import logging
import os
import telegram
# import json
from dotenv import load_dotenv
# from telegram.constants import ParseMode
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler
from config.config import *
from services import timeout, timeout_with_inline
from services.user_management import create_user
# from services.app_error.index import app_error
from datetime import datetime
# import string
# import random

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
        [InlineKeyboardButton("Registrasi User >>", callback_data=str(CREATE_USER))],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Halo {}! Selamat datang di bot kami. Silakan gunakan perintah yang tersedia.'.format(full_name), reply_markup=reply_markup)
    
    return MENU

def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Terima kasih telah akses di *Assitance OCHA BOT*\nKlik /menu', reply_markup=ReplyKeyboardRemove(),parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END

def main() -> None:
    updater = Updater(TOKEN_BOT)
    dispatcher = updater.dispatcher 
    
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            MENU: [
                CallbackQueryHandler(create_user, pattern='^' + str(CREATE_USER) + '$'),
                CommandHandler('add', create_user),
            ],
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
