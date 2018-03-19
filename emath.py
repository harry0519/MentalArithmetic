
import random
import os
from time import time, clock
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
QUESTION_NUM = 10
ANSWERFILE_NAME    = "answers"
HISTORYFILE_NAME   = "history"

def gen_formular(max=20, operator = ['+','-']):

	flist=[]
	for a in range (1,max+1):
		for b in range(1,max+1):
			for o in operator:
				if o == '+' and a<=3 and b<=3:# 去除10以内加法
					continue

				r = eval("{}{}{}".format(a,o,b))
				if r>0 and r <= max: #排除结果<=0, >上限的题目
					f = [a,o,b]
					flist.append(f)
	print("%d questions totally generated." %len(flist))
	return flist

def show_result(answers, total_time):
	avg = answers['time'].mean()
	result = "APM={:.2f}/min, 平均:{:.2f}秒, 总时长={:.2f}秒".format(
		60.0/avg,avg, total_time)
	print("average = %.2fs, APM = %.2f/min max = %.2fs, min = %.2fs " %(avg,60.0/avg,
		answers['time'].max(),answers['time'].min()))
	zhfont1 = pfm.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')	

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
	plt.hist(answers['time'].values, 5, density=False, facecolor='b', cumulative =True)
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

	'''
	colors = ['red', 'green', 'blue', 'yellow'] 
	#有向图 
	DG = nx.DiGraph() 
	#一次性添加多节点，输入的格式为列表 
	DG.add_nodes_from(['A', 'B', 'C', 'D']) 
	#添加边，数据格式为列表 
	DG.add_edges_from([('A', 'B'), ('A', 'C'), ('A', 'D'), ('D','A')]) 
	#作图，设置节点名显示,节点大小，节点颜色 
	nx.draw(DG,with_labels=True, node_size=900, node_color = colors) 
	plt.show()
	'''
def get_filename():
	parser = argparse.ArgumentParser(description='debug mode')
	parser.add_argument("-d","--debug", help="print to debug.csv",action="store_true")
	args = parser.parse_args()
	debug_mode = args.debug
	if debug_mode:
		print("debug turned on")
		filename = ANSWERFILE_NAME+"_debug.csv"
		filename_history = HISTORYFILE_NAME+"_debug.csv"
	else:
		filename = ANSWERFILE_NAME+".csv"
		filename_history = HISTORYFILE_NAME+".csv"

	return filename, filename_history, debug_mode

if __name__=='__main__':
	max = 20

	filename, filename_history, debug_mode = get_filename()
	flist = gen_formular(max)
	if debug_mode:
		print(flist)
	df = pd.DataFrame(flist, columns=['x','op','y'])


	dfsample = df.sample(n=QUESTION_NUM)
	dfsample = dfsample.reset_index(drop=True)
	
	if debug_mode:
		print(dfsample)

	input("准备开始答题, 按enter开始")
	overall_start = clock()
	cnt = 0
	for i in dfsample.index:		
		f = dfsample.loc[i].values

		start = clock()
		cnt = cnt + 1
		question = "{}{}{}".format(f[0],f[1],f[2])
		input("{}.\t".format(cnt)+question)

		end = clock()
		dfsample.loc[i,'time'] = end - start
		dfsample.loc[i,'question'] = question
		dfsample.loc[i,'timestamp'] = datetime.now()
		
	print(dfsample)
	
	overall_end = clock()
	dfsample = dfsample.sort_index()	

	dfhistory = pd.DataFrame(columns=['timestamp','total','mean','max','min','question_num','APM'])
	dfhistory.loc[0] = [datetime.now(),clock()-overall_start,
						dfsample['time'].mean(),dfsample['time'].max(),dfsample['time'].min(),QUESTION_NUM,60.0/dfsample['time'].mean()]

	withHead = False
	if os.path.exists(filename) == False:
		withHead = True

	dfsample.to_csv(filename,mode='a',index=False,header=(os.path.exists(filename)==False),columns=['timestamp','x','op','y','time'])
	dfhistory.to_csv(filename_history,mode='a',index=False,header=(os.path.exists(filename_history)==False))


	show_result(dfsample.sort_index(ascending =False), clock()-overall_start)

