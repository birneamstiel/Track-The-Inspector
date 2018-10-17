from flask import Flask, render_template
from tinydb import TinyDB, Query
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)
db = TinyDB('db.json')

load_dotenv()
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
if not MAPBOX_TOKEN:
	sys.exit("Error: mapbox api token is not set. Create .env file and set MAPBOX_TOKEN.")


@app.route('/')
def hello_world():
	inspectors = db.all()

	for inspector in inspectors:
		relevance = get_relevance_from_time_passed(time.time() - inspector['timestamp'])
		inspector['geoJson']['properties']['relevance'] = relevance
		print (relevance)

		handle_inspector(inspector)
	return render_template('map.html', inspectors=inspectors, mapboxToken=MAPBOX_TOKEN)
	

    

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