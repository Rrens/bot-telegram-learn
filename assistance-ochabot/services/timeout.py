import telegram
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
# from telegram.constants import ChatAction, ParseMode

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
    