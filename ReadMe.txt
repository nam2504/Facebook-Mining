*) config.py : 
	- Lưu các giá trị chung sẽ gọi từ các chương trình khác
	- Điều khiển việc thu thập dữ liệu dựa trên thay đổi các giá trị như id_start (vị trí bắt đầu thu thập id) id_end (vị trí kết thúc)
*) convert.py :
	- Loại bỏ các kí tự điều khiển và chuyển dữ liệu về dạng json
*) dbHangler.py
	- Xử lý đọc, viết dữ liệu
*) idBot.py :
	- Lấy danh sách bạn bè của các id từ vị trí id_start đến id_end
*) userBot.py
	- Lấy thông tin người dùng từ vị trí u_start đến u_end
	- Các thông tin đang lấy bao gồm :
		'id'
		'name'
		'locale'
		'hometown'
		'location'
		'email'
		'birthday'
	(Có thể thay đổi theo cách thêm hoặc bớt các fields ở trong def handling(fb_id) )
*) postBot.py
	Lấy thông tin về các bài post của người dùng từ vị trí p_start đến p_end
	Các fields đang lấy :
		_f_id = 'id'	
		_f_created_time = 'created_time'
		_f_message= 'message'
		#_f_reactions = 'reactions'
		_f_likes = 'likes'
		_f_shares = 'shares'