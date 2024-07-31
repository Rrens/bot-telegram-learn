import logging
import os
import telegram
# import json
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.constants import ParseMode
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, CallbackContext
from services import req_ticket, timeout, timeout_with_inline

load_dotenv()

# Konfigurasi logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN_BOT = os.getenv('TOKEN_BOT')
# print(TOKEN_BOT)
# TOKEN_BOT='7048693889:AAHOk6XHLsrFj5vwShHH7Le1CugmjF7t2V0'
bot_log = Bot(token=TOKEN_BOT)



# Definisikan state untuk ConversationHandler
MENU = range(1)
MENU_REGISTRATION, REQ_TICKET = range(2)

async def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    # chatid_telegram = update.message.from_user.id

    # Buat inline keyboard
    keyboard = [
        [InlineKeyboardButton("Laporan Kendala >>", callback_data=str(REQ_TICKET))],
        [InlineKeyboardButton("Tim Ahli >>", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Status Laporan (Admin)", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Broadcast Pesan", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Jadikan Admin", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Hapus UserBot", callback_data=str(MENU_REGISTRATION))],[InlineKeyboardButton("Download Laporan Tiket", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("My Ticket List", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Eskalasi Case", callback_data=str(MENU_REGISTRATION))],
        [InlineKeyboardButton("Kembali", callback_data=str(MENU_REGISTRATION))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    
    

    # Kirim pesan
    await update.message.reply_chat_action(action=telegram.constants.ChatAction.TYPING)
    await update.message.reply_text(
        text=f"Full Name: {user.full_name}\nUsername: {user.username}\nChat ID Telegram: {user.id}",
        reply_markup=reply_markup
    )

    return MENU

async def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    print(user)
    await update.message.reply_chat_action(action=telegram.constants.ChatAction.TYPING)
    await update.message.reply_text(
        text=f"data User {user}",
        reply_markup=ReplyKeyboardRemove(),
        # parse_mode=ParseMode.MARKDOWN
    )
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TOKEN_BOT).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
                MENU: [
                    CallbackQueryHandler(req_ticket, pattern='^' + str(REQ_TICKET) + '$'),
                    CallbackQueryHandler(timeout_with_inline)
                ],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.TEXT | filters.COMMAND, timeout)]
            },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('batal', cancel)],
        conversation_timeout=os.getenv('TIMEOUT')
    )
    
    application.add_handler(conv_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()
