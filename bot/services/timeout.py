import telegram
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from utils.helper import edit_message, delete_message

def timeout(update, context):
    try:
        first_name = update.message.from_user.first_name
        message_id = update.message.message_id+3
        chat_id = update.message.from_user.id
        delete_message(chat_id, message_id)
        # bot_log.delete_message(chat_id,message_id)
        first_name = update.message.from_user.first_name
        message_id = update.message.message_id+2
        chat_id = update.message.from_user.id
        # bot_log.delete_message(chat_id,message_id)
        delete_message(chat_id, message_id)
        update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
        update.message.reply_text('Maaf Kak *{}*, session Anda sudah habis\nKlik /start'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    except:
        try:
            first_name = update.message.from_user.first_name
            message_id = update.message.message_id+2
            chat_id = update.message.from_user.id
            delete_message(chat_id, message_id)
            update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
            update.message.reply_text('Maaf Kak *{}*, session Anda sudah habis\nKlik /start'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        except:
            try:
                first_name = update.message.from_user.first_name
                message_id = update.message.message_id+1
                chat_id = update.message.from_user.id
                delete_message(chat_id, message_id)
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text('Maaf Kak *{}*, session Anda sudah habis\nKlik /start'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
            except:
                first_name = update.message.from_user.first_name
                update.message.reply_chat_action(action=telegram.ChatAction.TYPING)
                update.message.reply_text('Maaf Kak *{}*, session Anda sudah habis\nKlik /start'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
                
def timeout_with_inline(update, context):
    try:
        first_name = update.callback_query.from_user.first_name
        chat_id = update.callback_query.message.chat_id
        message_id_1 = update.callback_query.message.message_id+1
        message_id_2 = update.callback_query.message.message_id+2
        # bot_log.delete_message(chat_id,message_id_1)
        # bot_log.delete_message(chat_id,message_id_2)
        delete_message(chat_id, message_id_1)
        delete_message(chat_id, message_id_2)
        query = update.callback_query
        query.answer()
        query.message.reply_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /start'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)
    except telegram.error.BadRequest:
        try:
            first_name = update.callback_query.from_user.first_name
            chat_id = update.callback_query.message.chat_id
            message_id_3 = update.callback_query.message.message_id+3
            message_id_2 = update.callback_query.message.message_id+2
            delete_message(chat_id,message_id_3)
            delete_message(chat_id,message_id_2)
            query = update.callback_query
            query.answer()
            query.message.reply_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /start'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)
        except telegram.error.BadRequest:
            try:
                first_name = update.callback_query.from_user.first_name
                chat_id = update.callback_query.message.chat_id
                message_id_2 = update.callback_query.message.message_id+2
                delete_message(chat_id,message_id_2)
                query = update.callback_query
                query.answer()
                query.message.reply_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /start'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)
            except telegram.error.BadRequest:
                try:
                    first_name = update.callback_query.from_user.first_name
                    query = update.callback_query
                    query.edit_message_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /start'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)
                except telegram.error.BadRequest:
                    first_name = update.callback_query.from_user.first_name
                    chat_id = update.callback_query.message.chat_id
                    message_id_2 = update.callback_query.message.message_id+0
                    delete_message(chat_id,message_id_2)
                    query = update.callback_query
                    query.answer()
                    query.message.reply_text(text='Maaf Kak *{}*, session Anda sudah habis\nKlik /start'.format(first_name),parse_mode=telegram.ParseMode.MARKDOWN)
