import sys
import pandas as pd
import matplotlib.pyplot as plt
if len(sys.argv) !=2:
	print("python drwa.py data.list")
	exit(0)
def box_plot_outliers(data_ser, box_scale):
	iqr = box_scale * (data_ser.quantile(0.75) - data_ser.quantile(0.25))
	val_low = data_ser.quantile(0.25) - iqr
	val_up = data_ser.quantile(0.75) + iqr
	rule_low = (data_ser < val_low)
	rule_up = (data_ser > val_up)
	return (rule_low, rule_up), (val_low, val_up)
def outliers_proc(data, col_name, scale=3):
	data_series = data[col_name]
	rule, value = box_plot_outliers(data_series, box_scale=scale)
	index = np.arange(data_series.shape[0])[rule[0] | rule[1]]
	data = data.drop(index)
	return data

data = pd.read_table(sys.argv[1],index_col=0,header=0)
#groups = sys.argv[2].split(',')
groups = ["old_hwgs_HCC","old_hwgs_nonHCC","new_hwgs_HCC","new_hwgs_nonHCC","old_swgs_HCC","old_swgs_nonHCC","new_swgs_2020_09_nonHCC","new_swgs_2021_02_05_nonHCC","new_swgs_2021_07_10_nonHCC","new_swgs_2021_12_nonHCC"]
lst = data.columns
#labels = data.index
#print(data.index)
for feature in lst:
	label_lst = []
	for label in groups:
		data_tmp = data.loc[label,feature]
		data_filter =  outliers_proc(data.tmp,data_tmp[label])
		label_lst.append(data_filter)

	plt.boxplot(label_lst,labels=("old_hwgs_HCC","old_hwgs_nonHCC","new_hwgs_HCC","new_hwgs_nonHCC","old_swgs_HCC","old_swgs_nonHCC","new_swgs_2020_09_nonHCC","new_swgs_2021_02_05_nonHCC","new_swgs_2021_07_10_nonHCC","new_swgs_2021_12_nonHCC"))
	plt.title(feature,fontsize=14)
	#plt.xlabel("横轴",fontsize=16)
	#plt.ylabel('纵轴',fontsize=16)
	plt.xticks(fontsize=14)
	plt.yticks(fontsize=14)
	plt.savefig(feature+'.boxplot.jpg')
	plt.close()
