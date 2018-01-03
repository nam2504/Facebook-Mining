#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import convert
# 
def logMessage(type, message):
	print message
	print	
	return
# Write data :
def write_list_file(filename, list_data):
	if not list_data:
		return
	try:
		with open(filename, 'a') as f:
			f.writelines(["%s\n" % item  for item in list_data])
	except IOError as err:
		print "    OS error : ", err
	return
#
def wire_convert_file(filename, data):
	if not data:
		return
	with open(filename, 'a') as f:
		if type(data) is list:		
			f.writelines(["%s\n" % convert.convert(item) for item in data])
		elif type(data) is dict:
			line = convert.convert(data) + '\n'
			f.write(line)
	return
# Read data :
def load_file_ID(filename):
	list_id = []
	try:
		with open(filename, 'r') as f:
			for line in f:
				id = line.strip()
				if id:
					list_id.append(id)
	except IOError as err:
		print "    OS error : ", err
	print 'Length of list ID : ' + str(len(list_id))
	return list_id
#
# def mainTest():
	# write_list_file('test.txt', [])
	# write_list_file('test.txt', [{'Myname: ' : "Anh Nam"}])
	# return

# mainTest()