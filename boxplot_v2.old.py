import sys
import matplotlib.pyplot as plt
import numpy as np
if len(sys.argv) != 4:
	print("python draw.py id input names")
	exit(0)
id = sys.argv[1].strip()
fh1= open(sys.argv[2]).readlines()
names = sys.argv[3].strip().split(',')
lst = [ i.split('_')[-1] for i in fh1[0].strip().split('\t')]
cancers = []
for cancer in names:
	index_list = [ int(i) for i,v in enumerate(lst) if v == cancer]
	cancer_data = [float(fh1[1].strip().split('\t')[i]) for i in index_list ]
	cancers.append(cancer_data)
def sig(cancers,v=0.5):
        health1 = cancers[0]
        cancer_datas = cancers[1:]
        con_mean = np.mean(health1)
        con_std = np.std(health1)
        diff_lst = {}
        for index,data in enumerate(cancer_datas):
                case_mean = np.mean(data)
                case_std = np.std(data)
                std_diff =  (case_mean - con_mean) / case_std
                if std_diff > v:
                        diff_lst[index] = std_diff
        if diff_lst:
                max_sig = max(diff_lst.values())
                sig_v = [ k+1 for k,v in diff_lst.items() if v == max_sig ]
        else:
                sig_v = [0]
        return sig_v

sig_v1 = sig(cancers)
colo_lst1 = ['white']*len(cancers)
if len(sig_v1) > 1:
	for i in sig_v1:
		colo_lst1[i] = 'red'
else:
	if sig_v1[0] != 0:
        	colo_lst1[sig_v1[0]] = 'red'

#label = 'health','colorectal','esophageal','gastric','ovarian'
bp = plt.boxplot(cancers,labels=names,patch_artist=True)
[bp['boxes'][i].set(facecolor=colo_lst1[i],alpha=0.7) for i in range(len(cancers))]
plt.title('old',fontsize=12)
plt.savefig(id+'.boxplot.jpg')
plt.close()
