#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
import logging
import facebook
import warnings
import sys
import json
#
import config
import dbHangler
# 

#
def handling(fb_id):
	################################################# 
	#												#
	#		 Get post and comment information		#
	# 												#
	#################################################
	#
	# 1. Send respon and get request data:
	# 1.1. inint feilds for request:
	_f_id = 'id'	
	_f_created_time = 'created_time'
	_f_message= 'message'
	# _f_reactions = 'reactions'
	_f_likes = 'likes'
	_f_shares = 'shares'
	# list friend request
	#_f_comment = 'comments{id,from,created_time,like_count,message}'
	# since and until
	_since = config.time_since.strip()
	_until = config.time_until.strip()
	if _until:
		since = '&since=' + _since
	if _until:
		until = '&until=' + _until
	
	try:		
		#global graph
		#		
		_fields = '/posts?fields=%(_f_id)s,%(_f_created_time)s,%(_f_message)s,%(_f_likes)s,%(_f_shares)s%(since)s%(until)s'% locals()
		# 1.2 : ininit request :
		_request = '%(fb_id)s%(_fields)s' % locals()
		# 1.3 : Send request and get respon data:
		respon = graph.get_object(_request)
		
		# 2 : Conver data to update DB :
		try:
			#list_comments_of_user = []
			list_posts = respon['data']
			if len(list_posts) == 0:
				return
			# Conver posts :
			for post in list_posts:
				# add post's user
				post['from'] = fb_id
				# shares : dictonary {"count" : int} => int
				try:
					post[_f_shares] = post[_f_shares]['count']
				except:
					post[_f_shares] = 0
				
				try:
					post[_f_likes] = post[_f_likes]['count']
				except:
					post[_f_likes] = 0
				
			# 3 : Save to DB			
			# write list post file and list_comments_of_user :
			#global list_post, list_comment, total_post, total_comment
			
			global add_data_lock
			add_data_lock.acquire()
			
			# add to list
			global list_post
			list_post.extend(list_posts)
			#list_comment.extend(list_comments_of_user)
			#
			# increase read succes:
			global read_succes
			read_succes += 1
			# release lock
			add_data_lock.release()
			#
			# if length of list > length in config => write to DB
			if (len(list_post) > config.post_len):
				add_data_lock.acquire()
				# clone list 
				list_data = [item for item in list_post]
				# clear list :
				global total_post
				list_post = []
				add_data_lock.release()
				# write data :
				write_data_lock.acquire()
				#
				dbHangler.wire_convert_file(config.f_user_posts, list_data)
				# increate total post
				total_post += len(list_data)
				#
				write_data_lock.release()
			
		except IOError as err:
			print "Get information of user Error at Step 2 in Handling",
			print err
	except facebook.GraphAPIError as err:
		print err
	return
#
# Thread get user Infor
class MyThread(threading.Thread):
	def __init__(self, name, end):
		threading.Thread.__init__(self)
		#
		self._end = end	
		self._name = name
		self.isLive = True
		
	def run(self):
		#global list_id
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
			fb_id = list_id[_index]	# id of user to get infor
			
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
			print 'Read : ' + str(read_succes)
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
	print "Start get users'posts!"	
	
	# Start thread get post:
	t = threading.Thread(target = inintThread)
	t.start()
	try:
		t.join()
	except:
		print 'thread t join fail'
	#
	# write post:
	#global list_post, list_comment
	dbHangler.wire_convert_file(config.f_user_posts, list_post)
	#dbHangler.wire_convert_file(config.f_user_comments, list_comment)
	#
	
	global total_post
	total_post += len(list_post)
	#
	print 'Total post: ', total_post
	#print 'Total comment: ', total_comment
	#
	end_time = time.time()
	print 'Read %d users in %d second'%((end - start), (end_time - start_time))
	#
	return 0
	
# inint	
graph = facebook.GraphAPI(config.token)
warnings.filterwarnings("ignore")
#
list_id = dbHangler.load_file_ID(config.f_HN_id)
threads = []

#
read_succes = 0
start_time = time.time()
#
start = config.p_start
end = min(config.p_end, len(list_id))
index = start
#


#
# inint for post :
list_post = []
#list_comment = []
total_post = 0
#total_comment =  0
# Lock for thread :
get_id_lock = threading.Lock()
add_data_lock = threading.Lock()
write_data_lock = threading.Lock()
#
if __name__ == "__main__":	
	main()	