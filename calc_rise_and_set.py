#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  python3 
#  
#  Copyright 2020  <pi@RPi400sd2>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from datetime import datetime, timedelta
import ephem 
import time

class class_rise_set():
	def __init__(self,config):
		self.__observer=ephem.Observer()  
		self.__config = config
		self.__observer.lat=str(self.__config.latitude)  
		self.__observer.long=str(self.__config.longitude)  
		self.__sun=ephem.Sun()
		self.time_used = datetime.now()
		self.__observer.date = self.time_used
	def compute(self,test_offset_hours):
		self.time_used = datetime.now() + timedelta(hours = test_offset_hours)
		self.__observer.date = self.time_used
		self.__sun.compute()
		self.__next_rise = ephem.localtime(self.__observer.next_rising(self.__sun))
		self.__next_set = ephem.localtime(self.__observer.next_setting(self.__sun))
		self.next_set_time = (self.__next_set - self.time_used).total_seconds()/60/60
		self.next_rise_time = (self.__next_rise - self.time_used).total_seconds()/60/60
		if self.next_set_time < self.next_rise_time:
			self.night = False
		else:
			self.night = True

	def test_timing_calc(self,hours_ahead,step):
		for hours_to_add in range(0,hours_ahead,step):
			self.compute(hours_to_add)			
			print("In ", str(hours_to_add),' hours at : ',self.__observer.date)
			print("next_set_time in : ",self.next_set_time," hours and next_rise_time in : ",self.next_rise_time, " hours")
			if self.night:
				print("It will be Night Time so would Turn IR On \n")
			else:
				print("It will be  Day Time so would Turn IR Off \n")
			time.sleep(0.1)

