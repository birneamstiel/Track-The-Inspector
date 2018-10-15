from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def message(bot, update):
	print(update.message.text)



updater = Updater(TELEGRAM_API_KEY)

# updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message))

updater.start_polling()
updater.idle()
