import logging
import os
import telegram
import json
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.constants import ParseMode
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, CallbackContext

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

async def timeout(update: Update, context: CallbackContext) -> None:
    print('okee TIMEOUT')
    try:
        first_name = update.message.from_user.first_name
        message_id = update.message.message_id + 3
        chat_id = update.message.from_user.id
        await context.bot.delete_message(chat_id, message_id)
        message_id = update.message.message_id + 2
        await context.bot.delete_message(chat_id, message_id)
        await update.message.reply_chat_action(action=ChatAction.TYPING)
        await update.message.reply_text(
            text=f'Maaf Kak *{first_name}*, session Anda sudah habis\nKlik /menu',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardRemove()
        )
    except:
        try:
            message_id = update.message.message_id + 2
            await context.bot.delete_message(chat_id, message_id)
            await update.message.reply_chat_action(action=ChatAction.TYPING)
            await update.message.reply_text(
                text=f'Maaf Kak *{first_name}*, session Anda sudah habis\nKlik /menu',
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=ReplyKeyboardRemove()
            )
        except:
            try:
                message_id = update.message.message_id + 1
                await context.bot.delete_message(chat_id, message_id)
                await update.message.reply_chat_action(action=ChatAction.TYPING)
                await update.message.reply_text(
                    text=f'Maaf Kak *{first_name}*, session Anda sudah habis\nKlik /menu',
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=ReplyKeyboardRemove()
                )
            except:
                await update.message.reply_chat_action(action=ChatAction.TYPING)
                await update.message.reply_text(
                    text=f'Maaf Kak *{first_name}*, session Anda sudah habis\nKlik /menu',
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=ReplyKeyboardRemove()
                )
    return ConversationHandler.END
    
                
async def timeout_with_inline(update: Update, context: CallbackContext) -> None:
    print('okee TIMEOUT WITHINLINE')
    try:
        first_name = update.callback_query.from_user.first_name
        chat_id = update.callback_query.message.chat_id
        message_id_1 = update.callback_query.message.message_id + 1
        message_id_2 = update.callback_query.message.message_id + 2
        await context.bot.delete_message(chat_id, message_id_1)
        await context.bot.delete_message(chat_id, message_id_2)
        query = update.callback_query
        await query.answer()
        await query.message.reply_text(
            text=f'Maaf Kak *{first_name}*, session Anda sudah habis\nKlik /menu',
            parse_mode=ParseMode.MARKDOWN
        )
    except telegram.error.BadRequest:
        try:
            message_id_3 = update.callback_query.message.message_id + 3
            message_id_2 = update.callback_query.message.message_id + 2
            await context.bot.delete_message(chat_id, message_id_3)
            await context.bot.delete_message(chat_id, message_id_2)
            query = update.callback_query
            await query.answer()
            await query.message.reply_text(
                text=f'Maaf Kak *{first_name}*, session Anda sudah habis\nKlik /menu',
                parse_mode=ParseMode.MARKDOWN
            )
        except telegram.error.BadRequest:
            try:
                message_id_2 = update.callback_query.message.message_id + 2
                await context.bot.delete_message(chat_id, message_id_2)
                query = update.callback_query
                await query.answer()
                await query.message.reply_text(
                    text=f'Maaf Kak *{first_name}*, session Anda sudah habis\nKlik /menu',
                    parse_mode=ParseMode.MARKDOWN
                )
            except telegram.error.BadRequest:
                try:
                    query = update.callback_query
                    await query.edit_message_text(
                        text=f'Maaf Kak *{first_name}*, session Anda sudah habis\nKlik /menu',
                        parse_mode=ParseMode.MARKDOWN
                    )
                except telegram.error.BadRequest:
                    query = update.callback_query
                    await query.answer()
                    await query.message.reply_text(
                        text=f'Maaf Kak *{first_name}*, session Anda sudah habis\nKlik /menu',
                        parse_mode=ParseMode.MARKDOWN
                    )    
    return ConversationHandler.END
    

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

async def req_ticket(update: Update, context: CallbackContext) -> None:
    # print('okeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    
    query = update.callback_query
    select_data = query.data
    data = "{}".format(query.message.reply_markup).replace("'",'"').replace("[[","[").replace("]]","]").replace("], [",",")
    data = json.loads(data)
    for data in data['inline_keyboard']:
        if data['callback_data'] == select_data:
            data_text = str(data['text']).replace(" >>","")
    
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='option_1')],
        [InlineKeyboardButton("Option 2", callback_data='option_2')],
        [InlineKeyboardButton("Option 3", callback_data='option_3')],
        [InlineKeyboardButton("Kembali", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query = update.callback_query
    await query.answer()  # Mengkonfirmasi bahwa callback query telah diterima
    # print(query)
    message_id = query.message.message_id+1
    chat_id = update.callback_query.from_user.id
    # await bot_log.delete_message(chat_id,message_id)
    
    await query.edit_message_text(text=f"Anda memilih : *{data_text}*",parse_mode=telegram.ParseMode.MARKDOWN)
    await query.message.reply_text("Penjelasan Kategori: \n*Aplication Error :* Loading after Login, Log out yourself, Hang\n*Acceptance :* Add Case, Cancel Case, Change Case, Document Case, Error Case, Generate Case, Requests Case, Submit & Resubmit Case, Update Case, Approval RFI, BOQ List Empty, Data Not Synchrone, Database Timeout Query, Duplicate SOWID, Fallback Status eOA, Guideline, Propose Milestone, Request OA, Reviewer User, Signature Blank, Status Workflow, Sync NEID\n*Budget :* Capex Balance, Justification, FBP (KBR/KPAA), Corsec, Reporting\n*Deployment :* Add Menu, Data Not Synchrone, Document Workflow, Error Data, Error Download Data, Error Export Data, Error Login, Error Menu, Request Delete Milestone, Request New Menu, Status Workflow\n*Issue Partial Baut :* Request Milestone\n*Process :* Data Not Synchrone, Request Mapping SOWID\n*Login :* Add User, Cant Login\n*Dashboard :* Data Not Synchrone, Duplicate Site, Duplicate SOWID, Request New Menu, Status Workflow\n*Tasklist :* Data Not Synchrone, Document Workflow, Duplicate eLV, Duplicate eOA, Error Duplicate ATP, Error Menu, Status Workflow\n*Planning :* Data Not Synchronice, Document Workflow, Request Delete eMOM, Request Delete Site List, Request Take Out eKKST, Update Data, Update Menu, Update NE ID\n*Knowledge :* Update Menu\n*Eligibility Check :* Data Not Synchrone\n\n*» Silahkan scroll ke bawah untuk klik tombol menu «*")
    await query.message.reply_text("Pilih :",reply_markup=reply_markup)
    # if query.data == 'REQ_TICKET':
    #     # Menanggapi klik tombol
    # elif query.data == 'back':
    #     syanticbot = 'https://t.me/syanticbot'
    #     keyboard = [[InlineKeyboardButton("SYANTIC BOT", url=syanticbot)]]
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #     await query.edit_message_text(
    #         text='*SYANTIC BOT* hanya bisa diakses melalui private chatBOT. Terima kasih \nKlik tombol di bawah ini',
    #         reply_markup=reply_markup,
    #         parse_mode='Markdown'
    #     )

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
    
    # Start the Bot
    application.run_polling()
    # application = Application.builder().token(TOKEN_BOT).build()

    # Daftarkan handler
    # application.add_handler(CommandHandler('start', start))
    # application.add_handler(CallbackQueryHandler(button))

    # # Mulai bot
    # application.run_polling()

if __name__ == '__main__':
    main()
