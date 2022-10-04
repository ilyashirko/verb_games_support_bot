from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
from environs import Env


def start(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text='Здавствуйте'
    )


def message_handler(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text=update.message.text
    )


def run_bot():
    updater = Updater(token=env.str('TELEGRAM_BOT_TOKEN'), use_context=True)
    updater.dispatcher.add_handler(
        CommandHandler(command='start', callback=start)
    )
    updater.dispatcher.add_handler(
        MessageHandler(filters=Filters.all, callback=message_handler)
    )
    updater.start_polling()
    updater.idle()


if __name__=='__main__':
    env = Env()
    env.read_env()
    run_bot()