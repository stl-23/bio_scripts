import sys
import matplotlib.pyplot as plt
from pylab import *
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

#label = 'health','colorectal','esophageal','gastric','ovarian'
subplots_adjust(left=0.15,bottom=0.1,top=0.9,right=0.95,hspace=0.5,wspace=0.5)
plt.subplot(211)
plt.boxplot(cancers1,labels=names1)
plt.title('new',fontsize=12)
plt.xticks(fontsize=10)
plt.xticks(fontsize=10)

plt.subplot(212)
plt.boxplot(cancers2,labels=names2)
plt.title('old',fontsize=12)
plt.xticks(fontsize=10)
plt.xticks(fontsize=10)
plt.savefig(id+'.boxplot.jpg')
plt.close()
