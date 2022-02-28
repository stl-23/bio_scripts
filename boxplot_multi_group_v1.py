import sys
import pandas as pd
import matplotlib.pyplot as plt
if len(sys.argv) !=2:
	print("python drwa.py data.list")
	exit(0)
data = pd.read_table(sys.argv[1],index_col=0,header=0)
#groups = sys.argv[2].split(',')
groups = ["old_hwgs_HCC","old_hwgs_nonHCC","new_hwgs_HCC","new_hwgs_nonHCC","old_swgs_HCC","old_swgs_nonHCC","new_swgs_2020_09_nonHCC","new_swgs_2021_02_05_nonHCC","new_swgs_2021_07_10_nonHCC","new_swgs_2021_12_nonHCC"]
lst = data.columns
#labels = data.index
#print(data.index)
for feature in lst:
	label_lst = []
	for label in groups:
		label_lst.append(data.loc[label,feature])
	plt.boxplot(label_lst,labels=("old_hwgs_HCC","old_hwgs_nonHCC","new_hwgs_HCC","new_hwgs_nonHCC","old_swgs_HCC","old_swgs_nonHCC","new_swgs_2020_09_nonHCC","new_swgs_2021_02_05_nonHCC","new_swgs_2021_07_10_nonHCC","new_swgs_2021_12_nonHCC"))    #### labels that from arguments always report wrong using the boxplot function, I wrote directly in the script ugly...
	plt.title(feature,fontsize=14)
	#plt.xlabel("横轴",fontsize=16)
	#plt.ylabel('纵轴',fontsize=16)
	plt.xticks(fontsize=14)
	plt.yticks(fontsize=14)
	plt.savefig(feature+'.boxplot.jpg')
	plt.close()
