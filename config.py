#!/usr/bin/python
#File list
# in : 
f_All_ID = 'DB/in/new_id.txt' #id.txt
f_HN_id = 'DB/in/hanoi.txt'
# out :
f_user_infor = 'DB/out/infors.txt'
f_user_posts = 'DB/out/posts.txt'
f_user_comments = 'DB/out/comments.txt'
f_id_new = 'DB/out/new_id.txt'
#log
f_Log = 'DB/log.txt'

# Graph api
token = 'EAAAAUaZA8jlABANJ52SRZChVwqrZAzxpqILaLCsZBwlfoiDGphNt7dybXfK4PzHw74v6Extpgt6DEnjrIGIRQo9Y1E5zWteyorWWf72s4rI4C65JynSx3j7t9YSi2X96cx9CynOv4MYt1shONysa44gxI0iufVgZD'
# DB :
tbName = 'fb_data'
# Thread
delay = 1
num_thread = 150

# for Get Post:
time_since = '2017-10-01'
time_until = '2017-10-31'

# post: start and end
p_start = 0
p_end = 787362 # max :787362

# For user:
# user infor : start and end
u_start = 0
u_end = 12234430 # max :6198235

# len to write file :
post_len = 10000
comment_len = 10000
id_len = 1000000

#
id_start = 20000
id_end = 100000