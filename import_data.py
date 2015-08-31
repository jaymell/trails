#!/usr/bin/python

import os
import shutil
import uuid
import zipfile
import datetime
import dateutil.tz
import xml.etree.ElementTree as ET
import json
from pymongo import MongoClient
import re

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
DB_NAME = 'fitness'
collection = connection[DB_NAME]['trails']


class Kml:
	""" for getting data out of google tracks kml files """ 
	def _get_time(self):
		""" get time in first 'when' tag that appears --
			there may be a better way to do this """ 
		# need to variable-ize the version ??? 
		time = self.root.find('.//{http://www.opengis.net/kml/2.2}when').text
		## strip off last 5 chars, ie '.135Z in '2015-08-01T00:06:29.135Z'
		utc = dateutil.tz.tzutc() 
		central = dateutil.tz.gettz('America/Chicago')
		time = datetime.datetime.strptime(time[:-5], '%Y-%m-%dT%H:%M:%S')
		time = time.replace(tzinfo=utc)
		self.time = time.astimezone(central)
	def __init__(self, kml):
		""" expects to be passed a file handle for kml file """
		self.uid = uuid.uuid4()
		self.tree = ET.parse(kml)
		self.root = self.tree.getroot()
		# don't catch error on this -- we want it to fail if no time:
		self._get_time()
		try:
			self.name = self.root.find('.//{http://www.opengis.net/kml/2.2}name').text
		except Exception as e:
			#print('self.name failed: %s' % e)
			self.name = 'Unnamed'
		try:
			self.activity = self.root.find('.//{http://www.opengis.net/kml/2.2}Data//{http://www.opengis.net/kml/2.2}value').text.title()
		except Exception as e:
			#print('self.activity failed: %s' % e)
			self.activity = 'Unknown'
		try:
			# just a big string of text, but there is lots
			# to pull out of it, eg activity type:
			self.description = self.root.find('.//{http://www.opengis.net/kml/2.2}description').text
		except Exception as e:
			print('self.description failed: %s' % e)

	def as_dict(self):
		return {'name': self.name, 'activity': self.activity, 'date': self.time.strftime('%Y-%m-%d %H:%M:%S'), 'uid': self.uid.__str__()}
	def as_json(self):
		return json.dumps(self.as_dict())
		
		
def is_duplicate(kml, collection):
	""" check whether a record with EXACT same
		date already exists in given mongo collection
	"""
	
	results = [ i for i in collection.find({'date': kml['date']}) ]
	if results:
		print('\nDuplicate found! %s\n' % item)
		return True
	else:
		return False

def process(kml_file, kmz=False):
	""" expects to be passed either a kmz or kml file """
	try:
		if kmz:
			zipped = zipfile.ZipFile(kml_file)
			kml = Kml(zipped.open('doc.kml'))
		else: 
			kml = Kml(open(kml_file))
	except Exception as e:
		print('Failed for %s: %s' % (kml_file, e))
	else:
		print('FILE NAME: %s' % kml_file)
		if not is_duplicate(kml.as_dict(), collection): 
			# try to update database AND
			# extract files to right place; if one
			# fails, undo the other:	
			try:
				collection.insert_one(kml.as_dict())
			except Exception as e:
				print('Failed to update database with %s: %s' % (kml, e))
			else:
				try:
					dest = 'static/kml/%s' % kml.uid
					if kmz:
						zipped.extractall(dest)
					else:
						if not os.path.exists(os.path.dirname(dest)):
							os.makedirs(os.path.dirname(dest))
							shutil.copy(kml_file, '%s/doc.kml' % dest)
				except Exception as e:
					print('Failed to extract files: %s\n\tTring to remove record from database...' % e)
					try:
						collection.remove(kml.as_json())
					except Exception as e:
						print('Failed to remove item from database -- db is no longer consistent w/ file system: %s' % e)
	finally:
		if kmz:
			zipped.close()
		else:
			kml.close()
		
if __name__ == '__main__':
	""" iterate through files (currently specified by location below) -- 
		determine whether kmz or kml and call process()
		appropriately """

	location = './kmz'
	for item in os.listdir(location):
		if item[-3:] == 'kmz':
			process(os.path.join(location,item), kmz=True)
		elif item[-3:] == 'kml':
			process(os.path.join(location,item))

		

"""
# first when tag:
root.find('.//{http://www.opengis.net/kml/2.2}Placemark//{http://www.opengis.net/kml/2.2}when').text
# simpler way to do the same:
root.find('.//{http://www.opengis.net/kml/2.2}when').text
 
"""
