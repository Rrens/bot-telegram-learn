import logging
import os
import telegram
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler
from config.config import *
from services.timeout import timeout, timeout_with_inline
from services.app import app_index, find_app, show_find_app
from services.form import form_index, download_form, upload_form, handle_upload_form
import string
import random
import time
from utils.helper import edit_message, delete_message

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN_BOT = os.getenv('TOKEN_BOT')
bot_log = telegram.Bot(TOKEN_BOT)

def start(update: Update, _: CallbackContext) -> None:
    try:
        user = update.message.from_user
        print('testing start')
        full_name = user.full_name
        # chatid_telegram = user.id 
        keyboard = [
            [InlineKeyboardButton("Application >>", callback_data=str(SEARCH_APP))],
            [InlineKeyboardButton("Form >>", callback_data=str(FORM))],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text('Halo {}! Selamat datang di *ACNES BOT*. Silakan gunakan perintah yang tersedia.'.format(full_name), reply_markup=reply_markup)
        
        return MENU
    except Exception as e:
        print(f"Error: {e}")
        
def main_menu(update: Update, _: CallbackContext) -> None:
    try:
        query = update.callback_query
        query.answer()
        
        chat_id = update.callback_query.message.chat_id
        message_id_1 = update.callback_query.message.message_id-1
        edit_message(query, "HOME")
        
        username = update.callback_query.from_user.username
        
        keyboard = [
            [InlineKeyboardButton("Application >>", callback_data=str(SEARCH_APP))],
            [InlineKeyboardButton("Form >>", callback_data=str(FORM))],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        query.message.reply_text('Halo {}! Selamat datang di *ACNES BOT*. Silakan gunakan perintah yang tersedia.'.format(username), reply_markup=reply_markup)
        
        return MENU
    except Exception as e:
        print(f"Error: {e}")
        
def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
    update.message.reply_text('Terima kasih telah akses di *ACNES BOT*\nKlik /start', reply_markup=ReplyKeyboardRemove(),parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END

# def end(update: Update, _: CallbackContext) -> None:

def main() -> None:
    updater = Updater(TOKEN_BOT)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            MENU: [
                CallbackQueryHandler(main_menu, pattern='^' + str(MAIN_MENU) + '$'),
                # APP
                CallbackQueryHandler(app_index, pattern='^' + str(SEARCH_APP) + '$'),
                CallbackQueryHandler(find_app, pattern='^' + str(FIND_APP) + '$'),
                # FORM
                CallbackQueryHandler(form_index, pattern='^' + str(FORM) + '$'),
                CallbackQueryHandler(download_form, pattern='^' + str(DOWNLOAD_FORM) + '$'),
                CallbackQueryHandler(upload_form, pattern='^' + str(UPLOAD_FORM) + '$'),
                
            ],
            SHOW_FIND_APP: [MessageHandler(Filters.text | Filters.command, show_find_app)],
            HANDLE_UPLOAD_FORM: [MessageHandler(Filters.document | Filters.command, handle_upload_form)],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout),
            CallbackQueryHandler(timeout_with_inline)
            ],
        },
        
        fallbacks = [CommandHandler('cancel', cancel), CommandHandler('batal', cancel)],
        conversation_timeout = int(os.getenv('TIMEOUT'))
    )
    
    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
    