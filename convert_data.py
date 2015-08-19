#!/usr/bin/python

import os
import uuid
import subprocess


kmz_dir = './kmz'

for kmz in os.listdir(kmz_dir):
	if kmz[-3:] == 'kmz':
		try:
			zipped = open(os.path.join(kmz_dir, kmz), 'rb')
			subprocess.check_call('/usr/bin/unzip', 
			# open random file name:
			with open('static/kml/%s' % uuid.uuid4(), 'wb') as f:
				f.write(zipped.read())
				f.close()
		except Exception as e:
			print('Failed for %s: %s' % (kmz, e))
		finally:
			zipped.close()
	
		
"""
list files in directory:
	if file ends with 'kmz':
		unzip it, cp it with a uuid as filename to static/kml folder
		 
"""
