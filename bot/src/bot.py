from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import sys
import requests
import time
import json
from geojson import Feature, Point
from dotenv import load_dotenv
from tinydb import TinyDB, Query
db = TinyDB('db.json')

load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
if not TELEGRAM_API_KEY:
	sys.exit("Error: Telegram bot api key is not set. Create .env file and set TELEGRAM_API_KEY.")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def message(bot, update):
	# print(update.message.text)
	getTrainStation(update.message.text)

def getTrainStation(raw_message):
	query = {'query': raw_message}
	r = requests.get('https://1.bvg.transport.rest/locations', params=query)
	print(r.url)
	# print(r.content)
	data = r.json()
	
	i = 0
	while data[i]['type'] != "stop":
		i = i + 1
	raw_station = data[i]
	print(raw_station ) 
	station_geometry = Point((raw_station['location']['longitude'], raw_station['location']['latitude']))
	station = Feature(geometry=station_geometry, properties={'name': raw_station['name'], 'rawValue': raw_message})
	print(station) 
	
	data = {}
	data['geoJson'] = station
	data['timestamp'] = time.time()
	db.insert(data)


updater = Updater(TELEGRAM_API_KEY)

updater.dispatcher.add_handler(MessageHandler(Filters.text, message))

updater.start_polling()
updater.idle()
