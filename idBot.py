#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import time
import logging
import facebook
import warnings
import sys
from sets import Set
import json
#
import config
import dbHangler
# 

#
def handling(fb_id):
	################################################# 
	#												#
	#		 Get information of User				#
	# 												#
	#################################################
	#1. Send respon and get request data:
	#1.1. Inint feilds for request:
	_f_id = 'id'
	# list friend request
	_friends = 'friends.limit(5000){id}'
		
	try:
		#	1.2 : inint request :
		_fields = '?fields=' + _f_id + ',' + _friends
		#
		_request = fb_id + _fields
		#print request
		#	1.3 : Send request and get respon data:
		#global graph
		respon = graph.get_object(_request)
		
		# 2 : Conver data to update DB
		if not respon.has_key('friends'):
			return
		try:
			# convert :
			#list friends have format [id1,id2,...]
			_user_friends = [f[_f_id] for f in respon['friends']['data']]
			
			# Add to list new_ids
			if _user_friends:
				add_lock.acquire()
				global new_ids
				new_ids.update(_user_friends)
				add_lock.release()
				# if list new_ids > config.id_len, update new_ids to list_id
				if len(new_ids) > config.id_len:
					add_lock.acquire()
					# set new id not in id_All
					diff_ids = new_ids.difference(list_id)
					new_ids = Set([])
					list_id.extend(diff_ids)
					add_lock.release()
					# Update DB :
					# Get lock
					global total_id
					global file_lock
					file_lock.acquire()
					total_id += len(diff_ids)
					dbHangler.write_list_file(config.f_id_new, diff_ids)
					file_lock.release()
					
				
			read_lock.acquire()
			# increase read_succes
			global read_succe
			read_succe += 1
			read_lock.release()
		except IOError as err:
			dbHangler.logMessage('error', "Get information of user Error at Step 3")
			print err
	except facebook.GraphAPIError as err:
		dbHangler.logMessage('error', err)
	return
#
# Thread get Infor
class MyThread(threading.Thread):
	def __init__(self, name, end):
		threading.Thread.__init__(self)
		#
		self._end = end
		self._name = name
		self.isLive = True
		
	def run(self):
		# Start Thread
		
		# Run
		while (self.isLive):
			# request to access shared resource
			#global list_lock
			list_lock.acquire()
			global index
			if (index >= self._end):
				self.isLive = False
				list_lock.release()
				continue
			else:
				_index = index
				index += 1
				list_lock.release()
			# get ID of user at index
			#global list_id
			global start
			fb_id = list_read[_index - start]	# id of user to get infor
			
			# Get Infor of user:
			handling(fb_id)
			
# Show Runable of Bot :
def display():
	#global threads
	#global start, end, index, start_time
	while True:
		run_percent = 100.0 * (index - start) / (end - start)
		thread_live = 0
		for t in threads:
			if t.isLive:
				thread_live += 1
		running_time = time.time() - start_time
		done_time = running_time * (100.0 - run_percent) / run_percent
		all_time = done_time + running_time
		message = ('Treads running: \t%d')%(thread_live) +\
				  '\nRun at index : \t' + str(index)+\
				  ('\nRun persent : \t%.2f')%(run_percent)+\
				  ('\nTime running : \t%2d:%2d:%2d')%(running_time/3600, (running_time%3600)/60, running_time%60)+\
				  ('\nTime to done : \t%2d:%2d:%2d')%(done_time/3600, (done_time%3600)/60, done_time%60)+\
				  ('\nTime all : \t%2d:%2d:%2d')%(all_time/3600, (all_time%3600)/60, all_time%60)
		print message + '\n'
		if run_percent >= 100:
			for thread in threads:
				if thread.isLive:
					thread.isLive = False
					thread.join()
			print 'Read : ' + str(read_succe)
			break
		time.sleep(config.delay)
	return
#inint Thread
def inintThread():	
	#	
	num_threads = config.num_thread
	if num_threads is None:
		try:
			num_threads = os.cpu_count()
		except AttributeError:
			num_threads = 4
	#global end	
	#global threads
	# inint and run thread get infor of user
	for _index in range(num_threads):
		t_name = 'Thread ' + str(_index)
		threads.append(MyThread(t_name, end))
		threads[_index].start()
	#
	display()
	return
# Main : 
def main():
	#print "Start get friend's imformation!"
	# get all Id exited in DB
	#global end, start
	#global start_time
	# Inint
	t = threading.Thread(target = inintThread)
	t.start()
	try:
		t.join()
	except:
		print 'thread t join fail'
	# write id 
	global new_ids
	new_ids = new_ids.difference(list_id)
	dbHangler.write_list_file(config.f_id_new, new_ids)
	global total_id
	total_id += len(new_ids)
	print 'Total new id: ', total_id
	#
	end_time = time.time()
	print 'Read %d users in %d second'%((end - start), (end_time - start_time))
	#
	return 0
	
# inint	
graph = facebook.GraphAPI(config.token)
warnings.filterwarnings("ignore")
#
list_id = dbHangler.load_file_ID(config.f_All_ID)
threads = []
#
read_succe = 0
start_time = time.time()
#
# inint for user :
start = config.id_start
end = min(config.id_end, len(list_id))
#
list_read = list_id[start : end]
index = start
#
new_ids = Set([])
total_id = 0

# Thread Lock
list_lock = threading.Lock()
file_lock = threading.Lock()
add_lock = threading.Lock()
read_lock = threading.Lock()
#
if __name__ == "__main__":
	main()