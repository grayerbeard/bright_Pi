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
import time

from bright_pi_lamps import class_bright_pi_lamps
from calc_rise_and_set import class_rise_set
from config import class_config
from sys import exit as sys_exit

from cpu import class_cpu
from config import class_config
from bright_pi_lamps import class_bright_pi_lamps
from text_buffer import class_text_buffer
from utility import fileexists   #,pr,make_time_text

print(datetime.now())
config = class_config()
if fileexists(config.config_filename):		
	print( "will try to read Config File : " ,config.config_filename)
	config.read_file() # overwrites from file
else : # no file so my_sensorneeds to be written
	config.write_file()
	print("New Config File Made with default values, you may need to edit it")

config.scan_count = 0

if config.lamps_control:
	headings = ["Count","Cpu Load-%","Temp-C","Cpu Freq-GHz","Cpu Mem-%","Cpu Disk-%","IR Lamp","Hrs to Sunrise","Hrs to Sunset","Errors"]
else:
	headings = ["Count","Cpu Load-%","Temp-C","Cpu Freq-GHz","Cpu Mem-%","Cpu Disk-%"]
log_buffer = class_text_buffer(headings,config)

rise_set = class_rise_set(config)
bright_pi = class_bright_pi_lamps()
cpu = class_cpu()
Error_Text = ""

if config.lamps_control:
	try:
	#	bright_pi.reset()
	#	print("IR off White ON")
	#	bright_pi.WHITE_on()
	#	time.sleep(20)
	#	bright_pi.reset()
	#	print("all off")
		

	#	print ("IR On")
	#	bright_pi.IR_on()
	#	time.sleep(20)
	#	bright_pi.reset()
	#	print("IR off White ON")
	#	bright_pi.WHITE_on()
	#	time.sleep(10)
	#	bright_pi.reset()
	#	print("all off")
	
	#	bright_pi.reset()
	#	print ("IR On")
	#	bright_pi.IR_on()
	#	time.sleep(20)
	#	bright_pi.reset()
	#	print("IR off White ON")
	#	bright_pi.WHITE_on()
	#	time.sleep(10)
	#	bright_pi.reset()
	#	print("all off")

		bright_pi.reset()
		print ("IR On")
		bright_pi.IR_on()
		time.sleep(20)
		bright_pi.reset()
		print("IR off White ON")
		bright_pi.WHITE_on()
		time.sleep(10)
		bright_pi.reset()
		print("all off")
	except:
		Error_Text = Error_Text + " Lamp Test Fail,"

# Following line for test only
# rise_set.test_timing_calc()

while (config.scan_count <= config.max_scans) or (config.max_scans == 0):
	try:
		config.scan_count += 1
		rise_set.compute(0)
		cpu.get_data()
		# print(rise_set.datetime_now.strftime(' Time is :  %H hrs %M min'))
		if rise_set.night and config.lamps_control:
			# Following l;ine for debugging only
			# print("Its Night Time Turn IR On")
			try:
				bright_pi.IR_on()
				log_buffer.line_values[6] = "On"
			except:
				Error_Text = Error_Text + " IR On Fail,"
		elif config.lamps_control:
			# Following l;ine for debugging only
			# print("Its Day Time Turn IR Off")
			try:
				bright_pi.reset()
				log_buffer.line_values[6] = "Off"
			except:
				Error_Text = Error_Text + " IR Off Fail,"			
		time.sleep(config.scan_delay)
		# print(datetime.now().strftime(' Time is :  %H hrs %M min'))
		log_buffer.line_values[0] = str(config.scan_count)
		log_buffer.line_values[1] = str(cpu.cpu_load)
		log_buffer.line_values[2] = str(round(cpu.temp,2) ) 
		log_buffer.line_values[3] = str(cpu.cpu_freq.current/1000)
		log_buffer.line_values[4] = str(cpu.cpu_mem) 
		log_buffer.line_values[5] = str(cpu.cpu_disk)

		if config.lamps_control:
			log_buffer.line_values[7] = str(round(rise_set.next_rise_time,2))
			log_buffer.line_values[8] = str(round(rise_set.next_set_time,2))
			log_buffer.line_values[9] = Error_Text
			Error_Text = ""
		
		buffer_increment_flag = True
		log_buffer.pr(buffer_increment_flag,0,rise_set.datetime_now,1234)

	except KeyboardInterrupt:
		print(".........Ctrl+C pressed...")
		sys_exit()
