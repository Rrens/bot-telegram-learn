import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config.config import *

async def app_error(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    select_data = query.data
    print(f"INI LOO ERROR DAT {select_data}")
    
    keyboard = [
        [InlineKeyboardButton("Loading After Login >>", callback_data=str(REQ_TICKET_ADD))],
        [InlineKeyboardButton("Acceptance >>", callback_data=str(REQ_TICKET_ADD))],
        [InlineKeyboardButton("Kembali", callback_data=str(REQ_TICKET))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text(f"INI APP ERROR DIPILIH {select_data}")
    
    await query.message.reply_text("Pilih :",reply_markup=reply_markup)
    
