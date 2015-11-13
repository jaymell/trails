#!/usr/bin/python
import ephem
import datetime
from time import localtime, strftime
from dateutil import tz

# thanks:
# https://gist.github.com/jj1bdx/202755

""" get sunrise / sunset time """
utc = tz.gettz('UTC')
central = tz.gettz('America/Chicago')
home = ephem.city("Dallas")
sun = ephem.Sun()

now = datetime.datetime.now()
ninety_days = now + datetime.timedelta(days=90)

while now < ninety_days:
		home.date = now
		sun.compute(home)
		nextrise = home.next_rising(sun).datetime().replace(tzinfo=utc).astimezone(central)
		nextset = home.next_setting(sun).datetime().replace(tzinfo=utc).astimezone(central)
		now = now + datetime.timedelta(days=1)
		print("date: %s\t sunrise: %s\t sunset: %s" % ( now, nextrise, nextset))
