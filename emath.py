
import random
from time import time, clock
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as pfm
import networkx as nx
import pandas as pd 
from datetime import datetime


def gen_formular(max=20, operator = ['+','-']):

	flist=[]
	for a in range (1,max+1):
		for b in range(1,max+1):
			for o in operator:
				
				if o == '-' and a==b:# 去除相同数字相减
					continue
				if o == '+' and a<=3 and b<=3:# 去除10以内加法
					continue

				r = eval("{}{}{}".format(a,o,b))
				if r>=0 and r <= max:
					f = [a,o,b]
					flist.append(f)
	print("%d formulation totally generated." %len(flist))
	return flist

if __name__=='__main__':
	max = 20
	count = 60

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
		#duration.append(end-start)
	overall_end = clock()
	dfsample = dfsample.sort_index()	

	avg = dfsample['time'].mean()
	result = "APM={:.2f}/min, 平均:{:.2f}秒, 总时长={:.2f}秒".format(
		60.0/avg,avg, overall_end-overall_start)
	print("average = %.2fs, APM = %.2f/min max = %.2fs, min = %.2fs " %(avg,60.0/avg,
		dfsample['time'].max(),dfsample['time'].min()))

	filename = "emathis_test.csv"
	dfsample.to_csv(filename,mode='a',index=False,header=False,columns=['x','op','y','time'])

	zhfont1 = pfm.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')	

	x = np.arange(1,count+1)
	y = dfsample['time'].values

	plt.subplot(212)  
	plt.plot(x, y,'-',lw=2)

	plt.title(result,fontproperties=zhfont1)
	plt.grid(True)
	plt.tight_layout()
	plt.xticks(x,dfsample['question'].values,rotation='vertical',fontproperties=zhfont1)
	plt.axhline(1.0, color='g', ls='--')
	plt.axhline(2.0, color='r', ls='--')
	#plt.subplots_adjust(bottom=-0.1)
	# 数据的直方图  
	plt.subplot(231)  	
	plt.hist(dfsample['time'].values, 5, normed=1, facecolor='b', alpha=0.75)
	plt.title("overall")
	plt.tight_layout()

	plt.subplot(232)  	
	plt.hist(dfsample.loc[dfsample['op']=='+']['time'].values, 5, normed=1, facecolor='g', alpha=0.75)
	plt.title("+",fontproperties=zhfont1)
	plt.tight_layout()

	plt.subplot(233)  	
	plt.hist(dfsample.loc[dfsample['op']=='-']['time'].values, 5, normed=1, facecolor='g', alpha=0.75)  
	plt.title("-",fontproperties=zhfont1)
	plt.tight_layout()

	plt.show()
