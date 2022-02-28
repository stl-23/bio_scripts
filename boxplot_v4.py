import sys
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
if len(sys.argv) != 6:
	print("python draw.py id input1 input2 names1 names2")
	exit(0)
id = sys.argv[1].strip()
fh1= open(sys.argv[2]).readlines()
fh2= open(sys.argv[3]).readlines()
names1 = sys.argv[4].strip().split(',')
names2 = sys.argv[5].strip().split(',')
lst1 = [ i.split('_')[-1] for i in fh1[0].strip().split('\t')]
lst2 = [ i.split('_')[-1] for i in fh2[0].strip().split('\t')]
cancers1 = []
cancers2 = []
for cancer in names1:
	index_list = [ int(i) for i,v in enumerate(lst1) if v == cancer]
	cancer_data = [float(fh1[1].strip().split('\t')[i]) for i in index_list ]
	cancers1.append(cancer_data)
for cancer in names2:
        index_list2 = [ int(i) for i,v in enumerate(lst2) if v == cancer]
        cancer_data2 = [float(fh2[1].strip().split('\t')[i]) for i in index_list2 ]
        cancers2.append(cancer_data2)

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

sig_v1 = sig(cancers1)
sig_v2 = sig(cancers2)
colo_lst1 = ['white']*len(cancers1)
colo_lst2 = ['white']*len(cancers2)
if len(sig_v1) > 1:
        for i in sig_v1:
                colo_lst1[i] = 'red'
else:
        if sig_v1[0] != 0:
                colo_lst1[sig_v1[0]] = 'red'

if len(sig_v2) > 1:
        for i in sig_v2:
                colo_lst2[i] = 'red'
else:
        if sig_v2[0] != 0:
                colo_lst2[sig_v2[0]] = 'red'

#label = 'health','colorectal','esophageal','gastric','ovarian'
subplots_adjust(left=0.15,bottom=0.1,top=0.9,right=0.95,hspace=0.5,wspace=0.5)
plt.subplot(211)
bp = plt.boxplot(cancers1,labels=names1,patch_artist=True)
[bp['boxes'][i].set(facecolor=colo_lst1[i],alpha=0.7) for i in range(len(cancers1))]
plt.title('new',fontsize=12)
plt.xticks(fontsize=10)
plt.xticks(fontsize=10)

plt.subplot(212)
bp = plt.boxplot(cancers2,labels=names2,patch_artist=True)
[bp['boxes'][i].set(facecolor=colo_lst2[i],alpha=0.7) for i in range(len(cancers2))]
plt.title('old',fontsize=12)
plt.xticks(fontsize=10)
plt.xticks(fontsize=10)
plt.savefig(id+'.boxplot.jpg')
plt.close()
