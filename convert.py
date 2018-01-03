#!/usr/bin/python
# -*- coding: utf-8 -*-

# import facebook
# import warnings
# import time
# import config

specialChar = {
	# ASCII control characters
	'\x00' : '', #null
	'\x01' : '', #start of header
	'\x02' : '', #start of text
	'\x03' : '', #end of text
	'\x04' : '', #end of transmission
	'\x05' : '', #enquiry
	'\x06' : '', #acknowledge
	'\x07' : '', #bell
	'\x08' : '', #backspace
	'\x09' : '\\t', #horizontal tab
	'\x0A' : '\\n', #line feed
	'\x0B' : '\\t', #vertical tab
	'\x0C' : '', #form feed
	'\x0D' : '', #enter / carriage return
	'\x0E' : '', #shift out
	'\x0F' : '', #shift in
	'\x10' : '', #data link escape
	'\x11' : '', #device control 1
	'\x12' : '', #device control 2
	'\x13' : '', #device control 3
	'\x14' : '', #device control 4
	'\x15' : '', #negative acknowledge
	'\x16' : '', #synchronize
	'\x17' : '', #end of trans. block
	'\x18' : '', #cancel
	'\x19' : '', #end of medium
	'\x1A' : '', #substitute
	'\x1B' : '', #escape
	'\x1C' : '', #file separator
	'\x1D' : '', #group separator
	'\x1E' : '', #record separator
	'\x1F' : '', #unit separator
	'\x7F' : '', #delete
	#ASCII printable characters
	'\x22' : "'", # "
	'\x5c' : '|'   # \
}

def convert(data):	
	if isinstance(data, basestring):		
		# Replace key in special:
		for key,value in specialChar.iteritems():
			data = data.replace(key, value)
		line = data.encode('utf-8').strip()
		return '"%s"'%line
	elif isinstance(data, dict):
		# dict type:
		slist = ['%s : %s' % (convert(k), convert(v)) for k,v in data.items()]
		line = '{%s}' % ", ".join(slist)		
	elif isinstance(data, list):
		# list type:
		slist = ['%s' % (convert(k)) for k in data]
		line = '[%s]' % ", ".join(slist)		
	else:
		# int, float type
		line = str(data)
	return line

# # Test
# def handling(fb_id):
	# list_post = []
	# ################################################# 
	# #												#
	# #		 Get post and comment information		#
	# # 												#
	# #################################################
	# #
	# # 1. Send respon and get request data:
	# # 1.1. inint feilds for request:
	# _f_id = 'id'	
	# _f_created_time = 'created_time'
	# _f_message= 'message'
	# # _f_reactions = 'reactions'
	# _f_likes = 'likes'
	# _f_shares = 'shares'
	# # list friend request
	# #_f_comment = 'comments{id,from,created_time,like_count,message}'
	# # since and until
	# _since = '2017-01-01'
	# _until = '2017-02-30'
	# if _until:
		# since = '&since=' + _since
	# if _until:
		# until = '&until=' + _until
	
	# try:		
		# #global graph				
		# #		
		# _fields = '/posts?fields=%(_f_id)s,%(_f_created_time)s,%(_f_message)s,%(_f_likes)s,%(_f_shares)s%(since)s%(until)s'% locals()
		# # 1.2 : ininit request :
		# _request = '%(fb_id)s%(_fields)s' % locals()
		# # 1.3 : Send request and get respon data:
		# respon = graph.get_object(_request)
		
		# # 2 : Conver data to update DB :
		# try:
			# #list_comments_of_user = []
			# list_posts = respon['data']
			# if len(list_posts) == 0:
				# return
			# # Conver posts :
			# print type(list_posts[0][_f_message])
			# for post in list_posts:
				# # add post's user
				# post['from'] = fb_id				
				# # shares : dictonary {"count" : int} => int				
				# try:
					# post[_f_shares] = post[_f_shares]['count']
				# except:
					# post[_f_shares] = 0
				
				# try:
					# post[_f_likes] = post[_f_likes]['count']
				# except:
					# post[_f_likes] = 0	
			
			# # add to list			
			# list_post.extend(list_posts)			
		# except IOError as err:
			# print "Get information of user Error at Step 2 in Handling",
			# print err
	# except facebook.GraphAPIError as err:
		# print err
	# return list_post
# # Main : 
# def main():
	
	# id = '100005871390128'	
	# # list_post = handling(id)
	# # try:
		# # with open('DB/conver_test.txt', 'a') as f:
			# # f.writelines(["%s\n" % item  for item in list_post])
	# # except IOError as err:
		# # print "    OS error : ", err
	
	# my_unicode = u'ch\u1ee7 nh\u1eadt m\u1edbi ra'
	# print type(my_unicode)		
	# print 'print repr unicode: \n\t', repr(my_unicode)
	# list_unicode = [u'ch\u1ee7 nh\u1eadt m\u1edbi ra ']
	# print 'print list of unicode : \n\t', list_unicode
	
	# #
	# return 0
	
# # inint	
# token = 'EAAAAUaZA8jlABADVJMZAyFpKKEZAzrzrrOKHqzsYbJoOd2OC0rUIhKKc6OvCY8x3V0ZADwOKwGI5gvyzgAhd5ujF6AB8F4bgj7bqZAKGX68jZBFilkYky6hoSgufzGAQxWaWaQFq9nB67IeWUIrx7UaICUiOhnAj3Sk8CND1wrXwZDZD'
# import facebook
# graph = facebook.GraphAPI(token)
# import warnings
# warnings.filterwarnings("ignore")
# #

# #
# if __name__ == "__main__":	
	# main()	