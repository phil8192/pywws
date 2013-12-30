#!/usr/bin/env python


# weather.ini:
#[live]
#services = []
#yowindow = 
#twitter = []
#plot = []
#text = [('pusher.json', 'P'), 'index.html']
#
#[pusher]
#app_id = x
#key = y
#secret = z
#channel = live_weather
#event = update

#phil@beaufort ~/weather/pywws/pywws $ cat ../../templates/pusher.json 
##live#
#{
#  #idx "'idx' : '%Y-%m-%d %H:%M:%S',"#
#  #temp_out "'temp_out' : '%.1f',"#
#  #wind_dir "'wind_dir' : '%.0f'," "" "winddir_degrees(x)"#
#  #wind_ave "'wind_ave' : '%.1f',"#
#  #wind_gust "'wind_gust' : '%.1f',"#
#  #hum_out "'hum_out' : '%.d',"#
#  #rel_pressure "'rel_pressure' : '%.1f',"#
#  #calc "rain_hour(data)" "'rain_hour' : '%.1f',"#
#  #calc "rain_day(data)" "'rain_day' : '%.1f',"#
#  #calc "dew_point(data['temp_out'], data['hum_out'])" "'dew_point' : '%.1f',"#
#}


# pywws - Python software for USB Wireless Weather Stations
# http://github.com/jim-easterbrook/pywws
# Copyright (C) 2008-13  Jim Easterbrook  jim@jim-easterbrook.me.uk

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import logging
#import sys

import pusher

#from pywws import DataStore
#from pywws import Localisation
#from pywws.Logger import ApplicationLogger

class ToPusher(object):
    def __init__(self, params):
        self.logger = logging.getLogger("pywws.ToPusher")
        self.old_ex = None
        # get parameters
	app_id = params.get("pusher", "app_id")
        key = params.get("pusher", "key")
        secret = params.get("pusher", "secret")
        if (not app_id) or (not key) or (not secret):
            raise RuntimeError("Authentication data not found")

	# pusher api
	self.api = pusher.Pusher(
  		app_id = app_id,
  		key = key,
  		secret = secret
	)

	self.channel = params.get("pusher", "channel")
        self.event = params.get("pusher", "event")

    def Upload(self, push_dict):
        if not push_dict:
            return True
	try:
		return self.api[self.channel].trigger(self.event, push_dict)
	except Exception, ex:
		self.logger.error(str(ex))
	return False

