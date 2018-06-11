
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
import click
import colorama

def generate_dynamic_question(dataset,size=100):
	dataset['question'] = dataset['x'].apply(lambda x:str(x))+dataset['op']+dataset['y'].apply(lambda x:str(x))

	gd = dataset.tail(300).groupby(['question'],axis=0).mean()
	answers = gd.sort_values(by=['time'],ascending=False)
	answers.reset_index(inplace=True)
	answers['op'] = '+'
	answers.loc[answers['question'].str.contains('-'),'op'] = "-"

	return answers[['x','op','y']].head(size)

def generate_fullset(op, limit):
	flist = []
	for a in range (1,limit+1):
		for b in range(1,limit+1):
			for o in op:
				r = eval("{}{}{}".format(a,o,b))
				if r>0 and r <= limit: #排除结果<=0, >上限的题目
					f = [a,o,b]
					flist.append(f)
	df = pd.DataFrame(flist, columns=['x','op','y'])
	return df

def load_font():
    if(os.name == 'posix'):
        font = pfm.FontProperties(fname='/Library/Fonts/Songti.ttc')
    else:
        font = pfm.FontProperties(fname='C:\\Windows\\Fonts\\simsun.ttc')	
    return font

def get_paper(umode, uamount, uname, limit):
	op = ['+','-']	
	answer_file = "answers_"+str(uname)+"_"+str(limit)+".csv"
	full_questions = generate_fullset(op, limit)

	try:
		if umode == 'd':
			dataset = pd.read_csv(answer_file)
			if len(dataset)>=300:
				dynamic_questions = generate_dynamic_question(dataset)

				dysample = dynamic_questions.sample(n=int(uamount*0.8))
				dysample = dysample.reset_index(drop=True)
				rdsample = full_questions.sample(n=int(uamount*0.2))
				rdsample = rdsample.reset_index(drop=True)
				paper = pd.concat([dysample,rdsample])
				paper = paper.sample(frac=1)
				paper = paper.reset_index(drop = True)
			else:
				umode = 'r'

	except FileNotFoundError:
		umode = 'r'

	if umode == 'r':
		paper = full_questions.sample(n=uamount)
		paper = paper.reset_index(drop = True)


	return paper

def show_result(answers, total_time,uamount):
	avg = answers['time'].mean()
	result = "APM={:.2f}, 平均:{:.2f}秒, 总时长={:.2f}秒".format(
		60.0/avg,avg, total_time)
	print("average = %.2fs, APM = %.2f, max = %.2fs, min = %.2fs " %(avg,60.0/avg,
		answers['time'].max(),answers['time'].min()))
	zhfont1 = load_font()
    
	x = np.arange(1,uamount+1)
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

def save(answers, test_time, uname,limit,uamount):
	answer_file  = "answers_"+uname+"_"+str(limit)+".csv"
	history_file = "history_"+uname+"_"+str(limit)+".csv"
	dfhistory = pd.DataFrame(columns=['timestamp','total','mean','max','min','question_num','APM'])
	dfhistory.loc[0] = [datetime.now(),test_time,
						answers['time'].mean(),answers['time'].max(),answers['time'].min(),uamount,60.0/answers['time'].mean()]

	answers.to_csv(answer_file,mode='a',index=False,header=(os.path.exists(answer_file)==False),columns=['timestamp','x','op','y','time'])
	dfhistory.to_csv(history_file,mode='a',index=False,header=(os.path.exists(history_file)==False))

@click.command()
@click.option('--ulimit', default=100, help='upper limit for your question')
@click.option('--amount', default=40, help='amount of questions')
@click.option('--name',   default='eason', help="user name. program will create history for different user name")
@click.option('--mode',   default='d', help="select paper mode. d=dyanmic, r=random")

def run(mode, amount, name, ulimit):
	print("用户名：%s,范围：1-%d,数量=%d,类型=%s" %(name,ulimit,amount,mode))
	print("----------------------------------")
	hint = "按enter开始答题"
	level = input(hint)

	dfsample = get_paper(mode, amount, name, ulimit)

	overall_start = time()
	cnt = 0
	for i in dfsample.index:		
		f = dfsample.loc[i].values

		question = "{}{}{}".format(f[0],f[1],f[2])
		full_question = "{}.\t{}".format(amount-cnt, question)
		cnt = cnt + 1

		start = time()
		input(full_question)
		end = time()

		dfsample.loc[i,'time'] = end - start
		dfsample.loc[i,'question'] = question
		dfsample.loc[i,'timestamp'] = datetime.now()
		
	print(dfsample)
	overall_end = time()
    
	save(dfsample.sort_index(),overall_end-overall_start, name, ulimit, amount)
	
	show_result(dfsample.sort_index(ascending =False), overall_end-overall_start,amount)
	dif = overall_end - overall_start
	print("Overall performance: %.2f APM, total time: %f s" %(60/(dif/40),dif))
	
if __name__=='__main__':

	run()


