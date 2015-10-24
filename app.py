from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
import json
import pycountry 
import ConfigParser 
import datetime

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
DB_NAME = 'fitness'

app = Flask(__name__,static_folder='static', static_url_path="/static")

config = 'gmaps.key'

@app.route("/")
def index():
	""" sort kml files in db and return list,
            load index page """

	collection = connection[DB_NAME]['trails']
	parser = ConfigParser.SafeConfigParser()
	parser.read(config)
	KEY=parser.get('KEYS', 'KEY')
	# query db to get the list of kml files
	# currently in inventory:
	the_list = [i for i in collection.find({}, {'_id': False})]
	# convert date to datetime object for template formatting:
	for item in the_list:
		item['date'] = datetime.datetime.strptime(item['date'],'%Y-%m-%d %H:%M:%S')
	# sort by date:
	sorted_list = sorted(the_list, key=lambda k: k['date'])
	return render_template("index.html", KEY=KEY, the_list=sorted_list)
	return 'Unable to open date file' 

@app.route("/kml")
def return_kml():
	""" not used anymore """
	uid = request.args.get('uid', '')
	if uid:
		try:
			xml = open('static/kml/%s/doc.kml' % uid)
		except Exception as e:
			return 'Could not retrieve requested record: %s ' % uid 
		else:
			return Response(xml, mimetype='text/xml')
	else:
		return 'Did not receive any data'

@app.route("/json")
def testjson():
	""" just for testing output of db content """
        collection = connection[DB_NAME]['trails']
        the_list = [i for i in collection.find({}, {'_id': False})]
	sorted_list = sorted(the_list, key=lambda k: k['date'])
	return json.dumps(sorted_list)

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5001, debug=True) 
