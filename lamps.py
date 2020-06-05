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
import smbus
import time


class class_bright_pi_lamps():
	def __init__(self):
		self.__device_address = 0x70
		self.__led_status_register = 0x00
		self.__gain_register = 0x09
		self.__max_gain = 0b1111
		self.__max_dim = 0x32
		self.__LED_ALL = (1, 2, 3, 4, 5, 6, 7, 8)
		self.__LED_IR = self.__LED_ALL[4:8]
		self.__LED_WHITE = self.__LED_ALL[0:4]
		self.__smb_bus = smbus.SMBus(1)
		self.__ON = 1
		self.__OFF = 0
		self.__default_gain = 0b1000
		self.__max_dim = 0x32
		self.__led_dim = [0 for i in range(0, 8)]
		self.white_day_sch = [0]*10
		self.white_night_sch = [0]*10
		self.ir_day_sch = [0]*10
		self.ir_night_sch = [50]*10

	def set_gain(self,gain):
		if gain >= 0 and gain <= self.__max_gain:
			gain = gain
			self.__smb_bus.write_byte_data(self.__device_address, self.__gain_register, gain)

	def set_led_dim(self,leds, dim):
		if dim >= 0 and dim <= self.__max_dim:
			for led in leds:
				if led >= 1 and led <= 8:
					self.__led_dim[led - 1] = dim
					self.__smb_bus.write_byte_data(self.__device_address, led, self.__led_dim[led - 1])

	def set_led_on_off(self,leds, state):
		led_hex = (0x02, 0x08, 0x10, 0x40, 0x01, 0x04, 0x20, 0x80)
		if state == self.__ON or state == self.__OFF:
			for led in leds:
				if led >= 1 and led <= 8:
					led_on_off = self.__smb_bus.read_byte_data(self.__device_address, self.__led_status_register)
					if state == self.__ON:
						led_on_off = led_on_off | led_hex[led - 1]
					else:
						led_on_off = led_on_off & ~ led_hex[led - 1]
				self.__smb_bus.write_byte_data(self.__device_address, self.__led_status_register, led_on_off)

	def reset(self):
		# This method is used to reset the SC620 to its original state
		self.set_gain(self.__default_gain)
		self.set_led_dim(self.__LED_ALL, self.__max_dim)
		self.set_led_on_off(self.__LED_ALL, self.__OFF)

	def IR_on(self):
		self.set_led_on_off(self.__LED_IR, self.__ON)

	def WHITE_on(self):
		self.set_led_on_off(self.__LED_WHITE, self.__ON)

class class_rise_set():
	def __init__(self,latitude,longitude):
		self.__observer=ephem.Observer()  
		self.__observer.lat=latitude  
		self.__observer.long=longitude  
		self.__sun=ephem.Sun()  
	def compute(self,test_offset_hours):
		self.__sun.compute()
		self.__next_rise = ephem.localtime(self.__observer.next_rising(self.__sun))
		self.__next_set = ephem.localtime(self.__observer.next_setting(self.__sun))
		self.datetime_now = datetime.now()
		self.time_used = self.datetime_now + timedelta(hours = test_offset_hours)
		self.next_set_time = (self.__next_set - self.time_used).total_seconds()/60/60
		if self.next_set_time < 0 : self.next_set_time = self.next_set_time + 24
		self.next_rise_time = (self.__next_rise - self.time_used).total_seconds()/60/60
		if self.next_rise_time < 0 : self.next_rise_time = self.next_rise_time + 24
		if self.next_set_time < self.next_rise_time:
			self.night = False
			self.night_length = round(self.next_rise_time - self.next_set_time,1)
			self.day_length = 24 - self.night_length
			self.posn = int(10 - (10*(self.day_length - self.next_set_time)/self.day_length))
			print("Day Length : ",self.day_length," and Night : ",self.night_length," We are " + str(self.posn) + " tenths through the day")
			self.posn = (self.day_length - self.next_set_time)/self.day_length
		else:
			self.night = True
			self.day_length = round(self.next_set_time - self.next_rise_time,1)
			self.night_length = 24 - self.day_length
			self.posn = int(10 - (10*(self.night_length - self.next_rise_time)/self.day_length))
			print("Day length : ",self.day_length," and Night : ",self.night_length," We are " + str(self.posn) + " tenths through the night")

def test_timing_calc():
	for hours_to_add in range(0,48,1):
		rise_set.compute(hours_to_add/2)
		print("At : " +  str(rise_set.time_used))
		print("In " + str(hours_to_add) +  " hours")
		print ("Next Sunrise Time : "+ str(rise_set.next_rise_time))
		print ("Next Sunset  Time : "+ str(rise_set.next_set_time))
		if rise_set.night:
			print("Its Night Time Turn IR On \n")
			lamps.WHITE_on()
			time.sleep(2)
			lamps.reset()
			lamps.IR_on()
		else:
			print("Its Day Time Turn IR Off \n")
			lamps.WHITE_on()
			time.sleep(0.25)
			lamps.reset()
			lamps.reset()
		time.sleep(4)

print(datetime.now())
latitude = '52.97'
longitude = '-2.69'
rise_set = class_rise_set(latitude,longitude)
lamps = class_bright_pi_lamps()

lamps.reset()
print ("IR On")
lamps.IR_on()
time.sleep(20)
lamps.reset()
print("IR off White ON")
lamps.WHITE_on()
time.sleep(20)
lamps.reset()
print("all off")


#test_timing_calc()

while True:
	rise_set.compute(0)
	if rise_set.night:
		print("Its Night Time Turn IR On \n")
		#print("White pn")
		#lamps.WHITE_on()
		#time.sleep(0.5)
		#lamps.reset()
		#print("White off, IR On")
		lamps.IR_on()
	else:
		print("Its Day Time Turn IR Off \n")
		#lamps.WHITE_on()
		#time.sleep(0.25)
		#lamps.reset()
		lamps.reset()
	time.sleep(300)
	print(datetime.now())
	#lamps.reset()
	#print("All Off")
