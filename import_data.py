#!/usr/bin/python

import os
import uuid
import zipfile
import datetime
import dateutil.tz
import xml.etree.ElementTree as ET
import json
from pymongo import MongoClient


""" iterate through kmz files,
	extract to unique folder name
	open kml file -- get date/time and location
"""

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'fitness'
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = 'trails'

kmz_dir = './kmz'
utc = dateutil.tz.tzutc() 
central = dateutil.tz.gettz('America/Chicago')
out_file = 'inventory.json'

def Kml(kml):

	def _get_time(self):
		""" get time in first 'when' tag that appears --
			there may be a better way to do this """ 
		# need to variable-ize the version ??? 
		time = root.find('.//{http://www.opengis.net/kml/2.2}when').text
		## strip off last 5 chars, ie '.135Z in '2015-08-01T00:06:29.135Z'
		time = datetime.datetime.strptime(time[:-5], '%Y-%m-%dT%H:%M:%S')
		time = time.replace(tzinfo=utc)
		time = time.astimezone(central)

	def _get_activity(self):
		pass

	def __init__(self, kml):
		self.kml = kml
		self.tree = ET.parse(kml)
		self.root = tree.getroot()
		self.name = root.find('.//{http://www.opengis.net/kml/2.2}name').text
		self.time = self._get_time()
		
def is_duplicate(item, collection):
	""" check whether a record with EXACT same
		date already exists in given mongo collection
	"""
	
	results = [ i for i in collection.find({'date': item['date']}) ]
	if results:
		print
		print('Duplicate found! %s' % item)
		print
		return True
	else:
		return False

for kmz in os.listdir(kmz_dir):
	if kmz[-3:] == 'kmz':
		try:
			uid = uuid.uuid4()
			zipped = zipfile.ZipFile(os.path.join(kmz_dir, kmz))
			kml = zipfile.ZipFile.open('doc.kml')
		except Exception as e:
			print('Failed for %s: %s' % (kmz, e))
		else:
			print('FILE NAME: %s' % kmz)
			# open doc.kml in appropriate folder
			# open xml parser, get date

			print('Name: %s\tTime: %s' % (name, time) )
			# convert to dict:
			item = { 'uid': uid.__str__(), 'date': time.strftime('%Y-%m-%d %H:%M:%S'), 'name': name }
			# append to list if it's not a duplicate:
			if not is_duplicate(item, collection): 
				# try to update database AND extract
				# extract files to right place; if one
				# fails, undo the other:	
				try:
					collection.insert_one(item)
				except Exception as e:
					print('Failed to update database with %s: %s' % (item, e))
				else:
					try:
						zipped.extractall('static/kml/%s' % uid)
					except Exception as e:
						print('Failed to extract files: %s\n\tTring to remove record from database...' % e)
						try:
							collection.remove(item)
						except Exception as e:
							print('Failed to remove item from database -- db is no longer consistent w/ file system: %s' % e)
		finally:
			zipped.close()
		
"""
# first when tag:
root.find('.//{http://www.opengis.net/kml/2.2}Placemark//{http://www.opengis.net/kml/2.2}when').text
# simpler way to do the same:
root.find('.//{http://www.opengis.net/kml/2.2}when').text
 
"""
