import random

# 单次试题数量. 建议在20-200题之间
QUESTION_NUM = 40
debug_mode = True
PAPER_NUM = 5
classnum = "211"
name = "何逸晨"
qlib = ["16+5","48-5","53-8" ,"63+4" ,"56-4" ,"45-7" ,"61-5" ,"44-7" ,"37-2" ,"27+5",
		"69-3","34-9","42-9" ,"18+32","27+18","68-54","97-72","29-14","49-26","30-16",
		"61-7","90-72","55-8","46+30+7","42-7-9","19+5+7","23+26+9","68-35-8","58-45-8","30-7",
		"43-8","50-48","72-49","33-21","36-18","52-27","71-2","72-6","89+7","47-9",
		"26+8","69+2","92-35","43-6"]

def gen_html_question(questions,seq):
	head = "<html><HEAD><META http-equiv=Content-Type content='text/html;charset=gb2312'></head>"
	body_title = "<body><center><br><br><h2>二年级第一学期口算复习卷({})<br></h2>班级___{}___&nbsp;&nbsp;&nbsp;姓名__{}___&nbsp;&nbsp;&nbsp;时间___________&nbsp;&nbsp;&nbsp;得分_________ <br><br>".format(seq+1,classnum,name)
	body_table_begin = "<table border=0 width=640 cellspacing=10>"
	body_table_end   = "</tr><tr></tr></table><br><br><br><br><br></center></body></html>"
	body_tr1 = "<tr>"
	body_tr2 = "</tr>"
	body_td1 = "<td>"
	body_td2 = "</td>"
	body_content =""
	body_equal = " = "
	i = 0

	for q in questions:
		if i == 0:
			body_content = body_content + body_tr1
		body_content = body_content + body_td1 + q + body_equal + body_td2
		i = i + 1
		if i == 4:
			body_content = body_content + body_tr2
			i = 0

	html = head + body_title + body_table_begin + body_content + body_table_end
	return html

if __name__=='__main__':
	for i in range(PAPER_NUM):
		random.shuffle(qlib)
		
		html = gen_html_question(qlib[:QUESTION_NUM],i)
			
		print(html)
		filename = "goover{}.html".format(i)
		f = open(filename,'w')
		f.write(html) 
		f.close()