import random
import os
from time import time, clock
from datetime import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as pfm
from matplotlib.patches import Polygon

import networkx as nx
import pandas as pd 

from datetime import datetime
import argparse

def draw_network(dataset):
	G = nx.from_pandas_edgelist(minusset,'x','y',create_using=nx.Graph(),edge_attr=['time'])
	M = G.number_of_edges()
	edge_colors = range(2, M + 2)
	edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

	#pos = nx.circular_layout(G)
	pos = nx.spring_layout(G)
	#plt.clf()
	print(pos)
	nx.draw(G, pos, edgelist=list(G.edges()), node_size=500, with_labels=True, node_color='red', alpha=0.8)
	edges = nx.draw_networkx_edges(G,pos,style='solid',alpha=0.2,width=minusset['time'].values,edge_color=edge_colors,edge_cmap=plt.cm.Blues,arrowstyle='->',arrowsize=6)
	#nx.draw_networkx_labels(G,pos,style='solid',alpha=0.2,color='')
	#for i in range(M):
	#    edges[i].set_alpha(edge_alphas[i])
	ax = plt.gca()
	ax.set_axis_off()
	plt.show()

def data_process(dataset):
	#dataset["rma5"]=dataset["time"].rolling(center=False,window=5).mean()
	#dataset["rma10"]=dataset["time"].rolling(center=False,window=10).mean()
	dataset["rma20"]=dataset["time"].rolling(center=False,window=20).mean()
	dataset['std']=dataset["time"].rolling(center=False,window=30).std(ddof = 0).fillna(0)
	dataset['uplimit']=dataset["rma20"] + dataset["std"]
	dataset['downlimit']=dataset["time"] - dataset["std"]
	return dataset

def draw_subplot(dataset, pre_title):
	
	total_average = dataset['time'].mean()
	total_training_time = dataset['time'].sum()
	total_training_question = dataset['time'].count()
	result = pre_title+"APM={:.2f}/min, 平均:{:.2f}秒, 总时长={:.2f}秒/共{}题".format(
		60.0/total_average,total_average, total_training_time,total_training_question)

	zhfont1 = pfm.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')		
	x = np.arange(1,dataset['time'].count()+1)
	y = dataset['time'].values
	plt.plot(x, y,'-',lw=1, alpha=0.7)
	plt.plot(x,dataset['rma20'].values,'--',lw=2,color='r')

	plt.grid(True, alpha=0.2)
	plt.tight_layout()
	#plt.yticks(x,dataset['question'].values,fontproperties=zhfont1)
	#plt.axhline(1.0, color='g', ls='--')
	#plt.axhline(2.0, color='r', ls='--')
	plt.axhline(y.mean(), color='y', ls='-')
	plt.ylim(ymin=-5)
	plt.xlim(xmin=-5)

	# Make the shaded region
	plt.fill_between(x,dataset['uplimit'].tolist(),dataset['downlimit'].tolist(),color='r',facecolor='0.9', alpha = 0.1)
	plt.title(result,fontproperties=zhfont1)

def draw_stat(dataset):
	plusset = dataset.loc[dataset['op']=='+'].reset_index(drop=True).drop(['op'],axis=1)
	minusset = dataset.loc[dataset['op']=='-'].reset_index(drop=True).drop(['op'],axis=1)
	dataset = data_process(dataset)	
	plusset = data_process(plusset)	
	minusset = data_process(minusset)	
	#print(dataset)


	#answers['question'] =str(answers['x']) + str(answers['op'])+str(answers['y'])
	plt.subplot(311)	
	draw_subplot(dataset,"Overall: ")

	plt.subplot(312)	
	draw_subplot(plusset,"+: ")
	plt.subplot(313)	
	draw_subplot(minusset,"-: ")
	#dataset[dataset['std']==0] =dataset['time']
	dataset['outlier'] = dataset['time'] > dataset['uplimit']
	print(dataset[(dataset['outlier']==True) & (dataset['std']>0.0)])
	filename = "report_"+datetime.now().date().isoformat()+".csv"
	dataset.to_csv(filename,index=False)
	'''
	# 数据的直方图  
	plt.subplot(322)  	
	plt.hist(answers['time'].values, 5, density=False, facecolor='b', cumulative =True)
	plt.title("overall")
	#plt.tight_layout()

	plt.subplot(324)  	
	plt.hist(answers.loc[answers['op']=='+']['time'].values, 5, density=True, facecolor='g')
	plt.title("+",fontproperties=zhfont1)
	#plt.tight_layout()

	plt.subplot(326)  	
	plt.hist(answers.loc[answers['op']=='-']['time'].values, 5, density=True, facecolor='g', alpha=0.75)  
	plt.title("-",fontproperties=zhfont1)
	#plt.tight_layout()
	'''
	plt.show()

dataset = pd.read_csv("data_analysis.csv",dtype={'x':np.int32,'y':np.int32})

#dataset['question'] = dataset['x'].to_string()+dataset['op'].to_string()+dataset['y'].to_string()
#print(dataset)
#gb = dataset.groupby(['x','op','y'],axis=0).mean()
#print(gb)
draw_stat(dataset)

