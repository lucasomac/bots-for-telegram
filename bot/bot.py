import logging as log
import os
import sys

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler

from bot.messages import main_menu_message, continue_menu_message, list_lottery_message
from web.loteria import get_result

# Enabling logging
log.basicConfig(level=log.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = log.getLogger(__name__)

mode = os.getenv("MODE")
token = os.getenv("TOKEN")


def run(updater):
    if mode == "dev":
        updater.start_polling()
    elif mode == "prd":
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=token)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, token))
    else:
        logger.error("No MODE specified!")
        sys.exit(1)


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Id', callback_data='get_id'),
                 InlineKeyboardButton('Loteria', callback_data='list_lottery')]]
    return InlineKeyboardMarkup(keyboard)


# def start(update: Update, context: CallbackContext):
def start(update, context):
    logger.info("Boot Iniciado")
    context.bot.send_message(chat_id=update.effective_chat.id, text=main_menu_message(),
                             reply_markup=main_menu_keyboard())
    # update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def start_continue(update, context):
    logger.info("Retorno do menu")
    context.bot.send_message(chat_id=update.effective_chat.id, text=continue_menu_message(),
                             reply_markup=main_menu_keyboard())


def get_id(update, context):
    logger.info("Retorna o id do Usuario")
    query = update.callback_query
    response_message = query.message.chat_id
    query.edit_message_text(response_message)
    start_continue(update, context)


def get_lottery(update, context):
    query = update.callback_query
    logger.info("Chamou a loteria {}".format(query.data))
    dados = get_result(query.data)
    query.edit_message_text(text="Concurso nª {} \nDezenas sorteadas: {}".format(dados[0], dados[1:len(dados) + 1]))
    start_continue(update, context)


def list_lottery_keyboard():
    keyboard = [[InlineKeyboardButton('DIADESORTE', callback_data='diadesorte'),
                 InlineKeyboardButton('DUPLASENA', callback_data='duplasena'),
                 InlineKeyboardButton('LOTOFACIL', callback_data='lotofacil')],
                [InlineKeyboardButton('LOTOMANIA', callback_data='lotomania'),
                 InlineKeyboardButton('MEGASENA', callback_data='megasena'),
                 InlineKeyboardButton('QUINA', callback_data='quina')],
                [InlineKeyboardButton('TIMEMANIA', callback_data='timemania')]]
    return InlineKeyboardMarkup(keyboard)


def list_lottery(update, context):
    query = update.callback_query
    context.bot.send_message(chat_id=query.message.chat_id,
                             text=list_lottery_message(),
                             reply_markup=list_lottery_keyboard())


def main_bot():
    logger.info("Starting bot")
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    run(updater)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(get_id, pattern='get_id'))
    dispatcher.add_handler(CallbackQueryHandler(list_lottery, pattern='list_lottery'))
    dispatcher.add_handler(CallbackQueryHandler(get_lottery))
    updater.idle()
