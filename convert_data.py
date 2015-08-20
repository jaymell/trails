#!/usr/bin/python

import os
import uuid
import zipfile
import datetime
import xml.etree.ElementTree as ET

""" iterate through kmz files,
	extract to unique folder name
	open kml file -- get date/time and location
"""

kmz_dir = './kmz'
gmt = datetime.tzinfo('UTC')

for kmz in os.listdir(kmz_dir):
	if kmz[-3:] == 'kmz':
		try:
			label = uuid.uuid4()
			zipped = zipfile.ZipFile(os.path.join(kmz_dir, kmz))
			zipped.extractall('static/kml/%s' % label)
		except Exception as e:
			print('Failed for %s: %s' % (kmz, e))
		else:
			with open('static/kml/%s/doc.kml' % label, 'rb') as kml:
				try:
					# open doc.kml in appropriate folder
					# open xml parser, get date
					tree = ET.parse(kml)
					root = tree.getroot()
					# get time in first 'when' tag that appears --
					# need to variable-ize the version ???
					time_txt = root.find('.//{http://www.opengis.net/kml/2.2}when').text
					# strip off last 5 chars, ie '.135Z in '2015-08-01T00:06:29.135Z'
					time = datetime.datetime.strptime(time_txt[:-5], '%Y-%m-%dT%H:%M:%S')
					print(time)
				except Exception as e:
					print('Failed to open %s: %s' % (kml, e))
		finally:
			zipped.close()
	
		
"""
# first when tag:
root.find('.//{http://www.opengis.net/kml/2.2}Placemark//{http://www.opengis.net/kml/2.2}when').text
# simpler way to do the same:
root.find('.//{http://www.opengis.net/kml/2.2}when').text
 
"""
