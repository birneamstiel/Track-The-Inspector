import os
import sys
import time
import re
import json
import requests

from dotenv import load_dotenv
from geojson import Feature, Point
from fuzzywuzzy import fuzz

from flask import Flask, render_template, request
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')
this_directory = os.path.dirname(__file__)

load_dotenv()
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
if not MAPBOX_TOKEN:
    sys.exit(
        "Error: mapbox api token is not set. Create .env file and set MAPBOX_TOKEN.")
if not TELEGRAM_API_KEY:
    sys.exit(
        "Error: Telegram bot api key is not set. Create .env file and set TELEGRAM_API_KEY.")


@app.route('/')
def get_inspectors():
    inspectors = db.all()
    relevant_inspectors = []
    for inspector in inspectors:
        passed_time = time.time() - inspector['timestamp']
        relevance = get_relevance_from_time_passed(passed_time)

        inspector['geoJson']['properties']['relevance'] = relevance
        inspector['geoJson']['properties']['passedTime'] = passed_time
        print(relevance)

        handle_inspector(inspector)
        # only show recent inspectors
        if relevance > 0:
            relevant_inspectors.append(inspector)
    return render_template('map.html', inspectors=relevant_inspectors, mapboxToken=MAPBOX_TOKEN)


@app.route("/{}".format(TELEGRAM_API_KEY), methods=["POST"])
def process_update():
    if request.method == "POST":
        update = request.get_json()
        if "message" in update:
            print('message!')
            improved_station_name = cleanseInput(update['message']['text'])
            getTrainStation(improved_station_name)
        return "ok!", 200


def getTrainStation(preprocessed_message):
    query = {'query': preprocessed_message['name']}
    r = requests.get('https://1.bvg.transport.rest/locations', params=query)
    print(r.url)
    # print(r.content)
    data = r.json()
    # import pdb; pdb.set_trace()
    i = 0
    while data[i]['type'] != "stop" and i < len(data) - 1:
        i = i + 1
    raw_station = data[i]
    if raw_station['type'] != "stop":
        raise ValueError('Could not find matching stop!')
        return
    print(raw_station)
    station_geometry = Point(
        (raw_station['location']['longitude'], raw_station['location']['latitude']))
    station = Feature(geometry=station_geometry, properties={
                      'name': raw_station['name'], 'rawValue': preprocessed_message['raw_message']})
    print('inserting: ', station)

    data = {}
    data['geoJson'] = station
    data['timestamp'] = time.time()
    db.insert(data)


def cleanseInput(raw_message):
    test1 = "Uhlanstr"
    test2 = "3 männlich gelesene Kontrolleure Yorckstraße U7 ausgestiegen"
    print("ratio: ", fuzz.token_set_ratio(test1, test2))
    regex = '((M|U|S|m|u|s)\d+)'
    match = re.search(regex, raw_message)
    # import pdb; pdb.set_trace()
    if not match:
        raise ValueError('Could not find line in raw message!')
        return raw_message
    line = match.group(0)

    # transform to upper case
    line = line.upper()


    data_path = os.path.join(this_directory, './data/lines.json')
    with open(data_path) as file:
        static_data = json.load(file)
    stations = static_data[line]

    scores_for_stations = []
    for station in stations:
        score = fuzz.token_set_ratio(station, raw_message)
        scores_for_stations.append({'name': station, 'score': score, 'raw_message': raw_message})
    scores_for_stations.sort(reverse=True, key=lambda x: x['score'])
    result = scores_for_stations[0]

    print('line: ', line)
    return result


def handle_inspector(inspector):
    print(inspector['geoJson'])


def get_relevance_from_time_passed(time_passed):
    # three hours
    if time_passed > 10800:
        return 0
    # two hours
    elif time_passed > 7200:
        return 10
    elif time_passed > 3600:
        return 20
    elif time_passed > 1800:
        return 50
    else:
        return 100
