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
import smbus

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
