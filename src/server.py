from flask import Flask, render_template, request
from tinydb import TinyDB, Query
from dotenv import load_dotenv
import os
import time
import requests
from geojson import Feature, Point

app = Flask(__name__)
db = TinyDB('db.json')

load_dotenv()
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
if not MAPBOX_TOKEN:
	sys.exit("Error: mapbox api token is not set. Create .env file and set MAPBOX_TOKEN.")
if not TELEGRAM_API_KEY:
	sys.exit("Error: Telegram bot api key is not set. Create .env file and set TELEGRAM_API_KEY.")


@app.route('/')
def hello_world():
	inspectors = db.all()

	for inspector in inspectors:
		relevance = get_relevance_from_time_passed(time.time() - inspector['timestamp'])
		inspector['geoJson']['properties']['relevance'] = relevance
		print (relevance)

		handle_inspector(inspector)
	return render_template('map.html', inspectors=inspectors, mapboxToken=MAPBOX_TOKEN)
	

@app.route("/{}".format(TELEGRAM_API_KEY), methods=["POST"])
def process_update():
	if request.method == "POST":
		update = request.get_json()
		if "message" in update:
			print('message!')
			getTrainStation(update['message']['text'])
		return "ok!", 200

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
	print('inserting: ', station) 
	
	data = {}
	data['geoJson'] = station
	data['timestamp'] = time.time()
	db.insert(data)

def handle_inspector(inspector):
	print(inspector['geoJson'])

def get_relevance_from_time_passed(time_passed):
	# two hours 
	if time_passed > 7200:
		return 10
	elif time_passed > 3600:
		return 20
	elif time_passed > 1800:
		return 50
	else:
		return 100