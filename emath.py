
import random
from time import time, clock
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as pfm
import pandas as pd 
from datetime import datetime

# 单次试题数量. 建议在20-200题之间
QUESTION_NUM = 20

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
		60.0/avg,avg, overall_end-overall_start)
	print("average = %.2fs, APM = %.2f/min max = %.2fs, min = %.2fs " %(avg,60.0/avg,
		answers['time'].max(),answers['time'].min()))
	zhfont1 = pfm.FontProperties(fname='C:\Windows\Fonts\simsun.ttc') # 非windows需要修改为本机字体路径

	x = np.arange(1,count+1)
	y = answers['time'].values

	plt.subplot(212)  
	plt.plot(x, y,'-',lw=2)

	plt.title(result,fontproperties=zhfont1)
	plt.grid(True)
	plt.tight_layout()
	plt.xticks(x,answers['question'].values,rotation='vertical',fontproperties=zhfont1)
	plt.axhline(1.0, color='g', ls='--')
	plt.axhline(2.0, color='r', ls='--')
	#plt.subplots_adjust(bottom=-0.1)
	# 数据的直方图  
	plt.subplot(231)  	
	plt.hist(answers['time'].values, 5, normed=1, facecolor='b', alpha=0.75)
	plt.title("overall")
	plt.tight_layout()

	plt.subplot(232)  	
	plt.hist(answers.loc[answers['op']=='+']['time'].values, 5, normed=1, facecolor='g', alpha=0.75)
	plt.title("+",fontproperties=zhfont1)
	plt.tight_layout()

	plt.subplot(233)  	
	plt.hist(answers.loc[answers['op']=='-']['time'].values, 5, normed=1, facecolor='g', alpha=0.75)  
	plt.title("-",fontproperties=zhfont1)
	plt.tight_layout()

	plt.show()

if __name__=='__main__':
	max = 20
	count = QUESTION_NUM

	flist = gen_formular(max)
	df = pd.DataFrame(flist, columns=['x','op','y'])
	dfsample = df.sample(n=count)

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
		
	overall_end = clock()
	dfsample = dfsample.sort_index()	

	filename = "emathis2.csv"
	dfsample.to_csv(filename,mode='a',index=False,header=False,columns=['x','op','y','time'])

	show_result(dfsample, clock()-overall_start)

