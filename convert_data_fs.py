#!/usr/bin/python

import os
import uuid
import zipfile
import datetime
import dateutil.tz
import xml.etree.ElementTree as ET
import json

""" iterate through kmz files,
	extract to unique folder name
	open kml file -- get date/time and location
"""

kmz_dir = './kmz'
utc = dateutil.tz.tzutc() 
central = dateutil.tz.gettz('America/Chicago')
out_file = 'inventory.json'
summary = []

def is_duplicate(item, summary):
	""" check against a list of items to check whether
		item is a duplicate """
	for record in summary:
		if ( item['name'] == record['name']
			and item['date'] == record['date']):
			print
			print('Duplicate found! %s' % item)
			print
			return True
	return False

for kmz in os.listdir(kmz_dir):
	if kmz[-3:] == 'kmz':
		try:
			label = uuid.uuid4()
			zipped = zipfile.ZipFile(os.path.join(kmz_dir, kmz))
			zipped.extractall('static/kml/%s' % label)
		except Exception as e:
			print('Failed for %s: %s' % (kmz, e))
		else:
			print('FILE NAME: %s' % kmz)
			with open('static/kml/%s/doc.kml' % label, 'rb') as kml:
				try:
					# open doc.kml in appropriate folder
					# open xml parser, get date
					tree = ET.parse(kml)
					root = tree.getroot()
					name = root.find('.//{http://www.opengis.net/kml/2.2}name').text
					# get time in first 'when' tag that appears --
					# need to variable-ize the version ???
					time = root.find('.//{http://www.opengis.net/kml/2.2}when').text
					## strip off last 5 chars, ie '.135Z in '2015-08-01T00:06:29.135Z'
					time = datetime.datetime.strptime(time[:-5], '%Y-%m-%dT%H:%M:%S')
					time = time.replace(tzinfo=utc)
					time = time.astimezone(central)
					print('Name: %s\tTime: %s' % (name, time) )
					# convert to dict:
					item = { 'label': label.__str__(), 'date': time.strftime('%Y-%m-%d %H:%M:%S'), 'name': name }
					# append to list if it's not a duplicate:
					if not is_duplicate(item, summary): summary.append(item)
				except Exception as e:
					print('Failed to open %s: %s' % (kml, e))
		finally:
			zipped.close()
		
with open(out_file, 'w') as f:
	json.dump(summary, f)
		
"""
# first when tag:
root.find('.//{http://www.opengis.net/kml/2.2}Placemark//{http://www.opengis.net/kml/2.2}when').text
# simpler way to do the same:
root.find('.//{http://www.opengis.net/kml/2.2}when').text
 
"""
