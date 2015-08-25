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

app = Flask(__name__,static_folder='static', static_url_path="/static")

config = 'gmaps.key'

@app.route("/")
def index():

	# the_list = [ i for i in range(100) ]
	parser = ConfigParser.SafeConfigParser()
	parser.read(config)
	KEY=parser.get('KEYS', 'KEY')
	# open inventory.json to get the list of kml files
	# currently in inventory
	with open('inventory.json') as f:
		the_list = json.loads(f.read())
		# sort by date:
		sorted_list = sorted(the_list, key=lambda k: k['date'])
		return render_template("index.html", KEY=KEY, the_list=sorted_list)
	return 'Unable to open date file' 

@app.route("/kml")
def return_kml():
	label = request.args.get('label', '')
	if label:
		try:
			xml = open('static/kml/%s/doc.kml' % label)
		except Exception as e:
			return 'Could not retrieve requested record: %s ' % label
		else:
			return Response(xml, mimetype='text/xml')
	else:
		return 'Did not receive any data'

@app.route("/json")
def testjson():
	with open('inventory.json') as f:
		return f.read()

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5001, debug=True) 


