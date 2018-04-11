
import random
import os
from time import time
from datetime import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as pfm

#import networkx as nx
import pandas as pd 
from datetime import datetime
import argparse

# 单次试题数量. 建议在20-200题之间
QUESTION_NUM = 40
ANSWERFILE_NAME    = "answers"
HISTORYFILE_NAME   = "history"
level = 1
upper_limit = 20


def generate_question(dataset):
	dataset['question'] = dataset['x'].apply(lambda x:str(x))+dataset['op']+dataset['y'].apply(lambda x:str(x))


	gd = dataset.tail(300).groupby(['question'],axis=0).mean()
	answers = gd.sort_values(by=['time'],ascending=False)
	answers.reset_index(inplace=True)
	answers['op'] = '+'

	answers.loc[answers['question'].str.contains('-'),'op'] = "-"

	return answers[['x','op','y']].head(100)


def load_font():
    if(os.name == 'posix'):
        font = pfm.FontProperties(fname='/Library/Fonts/Songti.ttc')
    else:
        font = pfm.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')	
    return font
def gen_formular(level=0, operator = ['+','-'],mode='static'):

	dataset = pd.read_csv("answers.csv",dtype={'x':np.int32,'y':np.int32})

	if len(dataset)>=300 and mode == 'dynamic': # 如果已经有300题历史记录, 开启动态出题
		df = generate_question(dataset)
		print("=====%d dynamic questions generated=====" %len(df))
	else:
		flist = []
		for a in range (1,upper_limit+1):
			for b in range(1,upper_limit+1):
				for o in operator:
					if level >= 1:
						if a==1 or b==1 or a==10 or b==10: # 去除含1,10的运算
							continue
					r = eval("{}{}{}".format(a,o,b))
					if r>0 and r <= upper_limit: #排除结果<=0, >上限的题目
						f = [a,o,b]
						flist.append(f)
		df = pd.DataFrame(flist, columns=['x','op','y'])
		print("=====%d random questions generated[1-%d]=====" %(len(df),upper_limit))

	return df

def show_result(answers, total_time):
	avg = answers['time'].mean()
	result = "APM={:.2f}/min, 平均:{:.2f}秒, 总时长={:.2f}秒".format(
		60.0/avg,avg, total_time)
	print("average = %.2fs, APM = %.2f/min max = %.2fs, min = %.2fs " %(avg,60.0/avg,
		answers['time'].max(),answers['time'].min()))
	zhfont1 = load_font()
    

	x = np.arange(1,QUESTION_NUM+1)
	y = answers['time'].values

	plt.subplot(121)	
	plt.plot(y, x,'-',lw=2)

	plt.title(result,fontproperties=zhfont1)
	plt.grid(True)
	plt.tight_layout()
	plt.yticks(x,answers['question'].values,fontproperties=zhfont1)
	plt.axvline(1.0, color='g', ls='--')
	plt.axvline(2.0, color='r', ls='--')
	plt.axvline(y.mean(), color='b', ls=':')

	# 数据的直方图  
	plt.subplot(322)  	
	plt.hist(answers['time'].values, 5, facecolor='b', density=True)
	plt.title("overall")
	plt.tight_layout()

	plt.subplot(324)  	
	plt.hist(answers.loc[answers['op']=='+']['time'].values, 5, density=True, facecolor='g')
	plt.title("+",fontproperties=zhfont1)
	plt.tight_layout()

	plt.subplot(326)  	
	plt.hist(answers.loc[answers['op']=='-']['time'].values, 5, density=True, facecolor='g', alpha=0.75)  
	plt.title("-",fontproperties=zhfont1)
	plt.tight_layout()

	plt.show()

def get_filename():
	global upper_limit
	parser = argparse.ArgumentParser(description='debug mode')
	parser.add_argument("-d","--debug", help="print to debug.csv",action="store_true")
	parser.add_argument("-e","--easy",  help="in easy mode, will keep all questions",action="store_true")
	parser.add_argument('-u', "--upper", help="upper limit of formular", dest="upper",default=20,type=int)
	args = parser.parse_args()
	debug_mode = args.debug
	upper_limit = args.upper 

	if args.easy:
		level = 0

	#level = args.level

	if debug_mode:
		print("debug turned on")
		filename = ANSWERFILE_NAME+"_debug.csv"
		filename_history = HISTORYFILE_NAME+"_debug.csv"
	else:
		filename = ANSWERFILE_NAME+".csv"
		filename_history = HISTORYFILE_NAME+".csv"

	return filename, filename_history, debug_mode#,level

def save(answers, test_time):
	dfhistory = pd.DataFrame(columns=['timestamp','total','mean','max','min','question_num','APM','upper_limit'])
	answers['upper_limit'] = upper_limit
	dfhistory.loc[0] = [datetime.now(),test_time,
						answers['time'].mean(),answers['time'].max(),answers['time'].min(),QUESTION_NUM,60.0/answers['time'].mean(),upper_limit]

	answers.to_csv(filename,mode='a',index=False,header=(os.path.exists(filename)==False),columns=['timestamp','x','op','y','time','upper_limit'])
	dfhistory.to_csv(filename_history,mode='a',index=False,header=(os.path.exists(filename_history)==False))


if __name__=='__main__':

	filename, filename_history, debug_mode = get_filename()
	mode = 'dynamic'
	hint = "准备开始答题, 按enter开始[s/d]"
	i = input(hint)
	if i in 'sS' and len(i)>0:
		mode = 'static'

	print(mode)
	df = gen_formular(mode=mode)

	dfsample = df.sample(n=QUESTION_NUM)
	dfsample = dfsample.reset_index(drop=True)

	overall_start = time()
	cnt = 0
	for i in dfsample.index:		
		f = dfsample.loc[i].values

		question = "{}{}{}".format(f[0],f[1],f[2])
		full_question = "{}.\t{}".format(QUESTION_NUM-cnt, question)
		cnt = cnt + 1

		start = time()
		input(full_question)
		end = time()

		dfsample.loc[i,'time'] = end - start
		dfsample.loc[i,'question'] = question
		dfsample.loc[i,'timestamp'] = datetime.now()
		
	print(dfsample)
	overall_end = time()
    
	save(dfsample.sort_index(),overall_end-overall_start)
	
	show_result(dfsample.sort_index(ascending =False), overall_end-overall_start)
	dif = overall_end - overall_start
	print("overall performance: %.2f APM, total time: %f s" %(60/(dif/40),dif))

