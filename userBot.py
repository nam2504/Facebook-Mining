#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import time
import facebook
import warnings
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
	_f_name = 'name'
	_f_locale = 'locale'
	_f_hometown = 'hometown'
	_f_location = 'location'
	_f_email = 'email'
	_f_birthday = 'birthday'
	try:		
		#	1.2 : inint request :
		_fields = '?fields=' + _f_id + ',' + _f_name + ',' +\
				_f_locale + ',' + _f_hometown + ',' + _f_location + ',' +\
				_f_email + ',' + _f_birthday
		#
		_request = str(fb_id) + _fields
		
		#	1.3 : Send request and get respon data:
		#global graph
		respon = graph.get_object(_request)
		
		# 2 : Conver data to update DB
		try:
			# convert :
			# Hometown
			try:
				respon[_f_hometown] = respon[_f_hometown]['name']
			except:
				respon[_f_hometown] = ""
			#_f_location
			try:
				respon[_f_location] = respon[_f_location]['name']
			except:
				respon[_f_location] = ""
			#
			#print respon
			# Update DB :
			# Get lock
			#global add_data_lock
			global list_infor
			global read_succe
			# Get lock
			add_data_lock.acquire()
			# add to list
			list_infor.append(respon)
			# increase read_succes
			read_succe += 1
			#
			add_data_lock.release()
			#
			#
			if (len(list_infor) > config.post_len):
				add_data_lock.acquire()
				_list_data = [item for item in list_infor]
				list_infor = []
				add_data_lock.release()
				#
				global total_infor
				write_data_lock.acquire()
				dbHangler.wire_convert_file(config.f_user_infor, _list_data)
				total_infor += len(_list_data)
				write_data_lock.release()
		except IOError as err:
			dbHangler.logMessage('error', "Get information of user Error at Step 3")
			add_data_lock.release()
			print err
	except facebook.GraphAPIError as err:
		#print err, "\n", fb_id
		print '.',
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
			#global get_id_lock
			get_id_lock.acquire()
			global index
			if (index >= self._end):
				self.isLive = False
				get_id_lock.release()
				continue
			else:
				_index = index
				index += 1
				get_id_lock.release()
			# get ID of user at index
			global list_id	
			fb_id = list_id[_index]	# id of user to get infor
			#fb_id = _index
			# Get Infor of user:
			try:
				handling(fb_id)
			except Exception as e:
				print e
			
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
		message = ('\nTreads running: \t%d')%(thread_live) +\
				  '\nRun at index : \t' + str(index)+\
				  ('\nRun persent : \t%.2f')%(run_percent)+\
				  ('\nTime running : \t%2d:%2d:%2d')%(running_time/3600, (running_time%3600)/60, running_time%60)+\
				  ('\nTime to done : \t%2d:%2d:%2d')%(done_time/3600, (done_time%3600)/60, done_time%60)+\
				  ('\nTime all : \t%2d:%2d:%2d')%(all_time/3600, (all_time%3600)/60, all_time%60) +\
				  ("\nRead succes: %10d") % (read_succe)
		print message + '\n'
		if run_percent >= 100:
			for thread in threads:
				if thread.isLive:
					thread.isLive = False
					thread.join()
			print 'Read succes: ' + str(read_succe)
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
	for index in range(num_threads):
		t_name = 'Thread ' + str(index)
		threads.append(MyThread(t_name, end))
		threads[index].start()
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
	# print list (user)
	global list_infor
	dbHangler.wire_convert_file(config.f_user_infor, list_infor)
	
	global total_infor
	total_infor += len(list_infor)
	print 'Total infor: ', total_infor
	#
	end_time = time.time()
	print 'Read %d users in %d second'%((end - start), (end_time - start_time))
	#
	return 0
	
# inint	
graph = facebook.GraphAPI(config.token)
warnings.filterwarnings("ignore")
#

threads = []
#
read_succe = 0
start_time = time.time()
#
list_id = dbHangler.load_file_ID(config.f_All_ID)
# inint for user :
start = config.u_start
end = config.u_end
index = start
#
list_infor = []
total_infor = 0

# Thread Lock
get_id_lock = threading.Lock()
add_data_lock = threading.Lock()
write_data_lock = threading.Lock()
#
if __name__ == "__main__":
	main()