import flask
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
import json
import pycountry 
import ConfigParser 
import datetime

app = flask.Flask(__name__,static_folder='static', static_url_path="/static")

p = ConfigParser.ConfigParser()
p.read("config")

app.config.update(
	KEY = p.get("KEYS", "KEY"),
	MONGODB_HOST = p.get("DB", "MONGODB_HOST"),
	MONGODB_PORT = int(p.get("DB", "MONGODB_PORT")),
	DB_NAME = p.get("DB", "DB_NAME"),
	COLLECTION = p.get("DB", "COLLECTION"),
	PORT = int(p.get("WEB", "PORT")),
	LISTEN_ADDR = p.get("WEB", "LISTEN_ADDR"),
	PUBLIC_URL = p.get("WEB", "PUBLIC_URL"),
)
	

def get_collection():
	""" handles connections to Mongo; pymongo.MongoClient does its own 
		pooling, so nothing fancy required --- just make a handle to 
		the db collection available """

	con = getattr(flask.g, '_connection', None)
	if con is None:
		flask.g._connection = MongoClient(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
		collection_name = app.config["COLLECTION"]
		db_name = app.config["DB_NAME"]
		collection = flask.g._connection[db_name][collection_name]
	return collection

@app.route("/")
def index():
	""" sort kml files in db and return list,
            load index page """

	collection = get_collection()
	# query db to get the list of kml files
	# currently in inventory:
	the_list = [i for i in collection.find({}, {'_id': False})]
	# convert date to datetime object for template formatting:
	for item in the_list:
		item['date'] = datetime.datetime.strptime(item['date'],'%Y-%m-%d %H:%M:%S')
	# sort by date:
	sorted_list = sorted(the_list, key=lambda k: k['date'])

	return flask.render_template(
		"index.html", 
		key = app.config["KEY"], 
		public_url = app.config["PUBLIC_URL"],
		the_list = sorted_list)

@app.route("/kml/<uid>")
def return_kml(uid):
	print("uid = %s" % uid)
	if uid:
		try:
			xml = open('./static/kml/%s/doc.kml' % uid)
		except Exception as e:
			return 'Could not retrieve requested record: %s ' % uid 
		else:
			return flask.Response(xml, mimetype='text/xml')
	else:
		return 'Did not receive any data'

@app.route("/json")
def testjson():
	""" just for testing output of db content """
        collection = get_collection()
        the_list = [i for i in collection.find({}, {'_id': False})]
	sorted_list = sorted(the_list, key=lambda k: k['date'])
	return json.dumps(sorted_list)

if __name__ == "__main__":
        app.run(host=app.config["LISTEN_ADDR"], port=app.config["PORT"], debug=True) 
