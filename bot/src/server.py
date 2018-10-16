from flask import Flask, render_template
from tinydb import TinyDB, Query
from dotenv import load_dotenv
import os

app = Flask(__name__)
db = TinyDB('db.json')

load_dotenv()
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
if not MAPBOX_TOKEN:
	sys.exit("Error: mapbox api token is not set. Create .env file and set MAPBOX_TOKEN.")


@app.route('/')
def hello_world():
	inspectors = db.all()
	data = []
	for inspector in inspectors:
		handle_inspector(inspector)
	return render_template('map.html', inspectors=inspectors, mapboxToken=MAPBOX_TOKEN)
	

    

def handle_inspector(inspector):
	print(inspector['geoJson'])