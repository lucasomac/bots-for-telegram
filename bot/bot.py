import logging as log
import os
import sys

from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler, ApplicationBuilder, ContextTypes, Application

from bot.menu import main_menu_keyboard, lottery_menu_keyboard
from features.lottery.loteria import get_result
from features.messages.messages import main_menu_message, continue_menu_message, list_lottery_message

# Enabling logging
log.basicConfig(level=log.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = log.getLogger(__name__)

MODE = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
PORT = os.getenv("PORT", "8443")
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Boot Iniciado")
    """Sends a message with three two buttons attached."""
    await update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard("get_id", "list_lottery"))


async def start_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Retorno do menu: Continuar")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=continue_menu_message(),
                                   reply_markup=main_menu_keyboard("get_id", "list_lottery"))


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPEt):
    logger.info("Retorna o id do Usuario")
    await update.callback_query.edit_message_text(
        text="Hi! Your chat id is: {}".format(update.effective_chat.id))
    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text="Hi! Your chat id is: {}".format(update.effective_chat.id)
    # )
    # After the initial menu, ask again what the user wants to do
    await start_continue(update, context)


async def get_lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    logger.info("Chamou a loteria {}".format(query.data))
    dados = get_result(query.data)
    await query.edit_message_text(
        text="Concurso nª {} \nDezenas sorteadas: {}".format(dados[0], dados[1:len(dados) + 1]))
    await start_continue(update, context)


async def list_lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        text=list_lottery_message(), reply_markup=lottery_menu_keyboard())


def run(application: Application):
    if MODE == "dev":
        application.run_polling()
    elif MODE == "prd":
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        application.run_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            secret_token=TOKEN,
            webhook_url="https://{}.herokuapp.com/".format(HEROKU_APP_NAME)
        )
    else:
        logger.error("No MODE specified!")
        sys.exit(1)


def main_bot():
    logger.info("Starting bot")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(get_id, pattern="get_id"))
    application.add_handler(CallbackQueryHandler(list_lottery, pattern="list_lottery"))
    application.add_handler(CallbackQueryHandler(get_lottery,
                                                 pattern="^(diadesorte|duplasena|lotofacil|lotomania|megasena|quina|timemania|supersete|milionaria)$"))
    run(application)
