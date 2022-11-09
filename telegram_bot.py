import logging

from environs import Env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, CallbackContext
from telegram import Update

from dialogflow_processing import detect_intent_text
from log_handlers import TelegramLogsHandler

logger = logging.getLogger('log.log')


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        update.effective_chat.id,
        text='Здавствуйте'
    )


def message_handler(update: Update, context: CallbackContext) -> None:
    dialogflow_response = detect_intent_text(
        env.str('GOOGLE_PROJECT_ID'),
        update.effective_chat.id,
        update.message.text,
    )
    context.bot.send_message(
        update.effective_chat.id,
        text=dialogflow_response.fulfillment_text
    )


def errors_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg='[TELEGRAM BOT ERROR]\n', exc_info=context.error)


def run_bot() -> None:
    updater = Updater(token=env.str('TELEGRAM_BOT_TOKEN'), use_context=True)
    
    logger.setLevel(logging.INFO)
    logger.addHandler(
        TelegramLogsHandler(updater.bot, env.int('ADMIN_TELEGRAM_ID'))
    )
    logger.info('[TELEGRAM] Support bot started')

    updater.dispatcher.add_handler(
        CommandHandler(command='start', callback=start)
    )
    updater.dispatcher.add_handler(
        MessageHandler(filters=Filters.all, callback=message_handler)
    )
    updater.dispatcher.add_error_handler(errors_handler)
    updater.start_polling()
    updater.idle()
    

if __name__=='__main__':
    env = Env()
    env.read_env()
    
    

    run_bot()
