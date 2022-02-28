import sys
import matplotlib.pyplot as plt
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
#label = 'health','colorectal','esophageal','gastric','ovarian'
plt.boxplot(cancers,labels=names)
plt.title(id,fontsize=18)
plt.savefig(id+'.boxplot.jpg')
plt.close()
