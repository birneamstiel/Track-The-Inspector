from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import sys
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
if not TELEGRAM_API_KEY:
	sys.exit("Error: Telegram bot api key is not set. Create .env file and set TELEGRAM_API_KEY.")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def message(bot, update):
	print(update.message.text)

updater = Updater(TELEGRAM_API_KEY)

updater.dispatcher.add_handler(MessageHandler(Filters.text, message))

updater.start_polling()
updater.idle()
