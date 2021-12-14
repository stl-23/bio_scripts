import sys
import matplotlib.pyplot as plt
if len(sys.argv) !=4:
	print("python drwa.py data.list cancer_num health_num")
	exit(0)
cancer = int(sys.argv[2])
norm = int(sys.argv[3])
with open(sys.argv[1]) as fh1:
	for lines in fh1:
		if lines.startswith('id'):
			stand_labels = [ i.split('_')[0] for i in lines.strip().split('\t')[2+cancer+norm:]]
		else:
			line = lines.strip().split('\t')
			id = line[0]
			cancers = [ float(i) for i in line[2:2+cancer]]
			norms = [ float(i) for i in line[2+cancer:2+cancer+norm] ]
			stand = [ float(i) for i in line[2+cancer+norm:] ]
			plt.title(id,fontsize=14)
			plt.xticks(rotation=90)
			plt.plot(stand_labels,stand)
			plt.margins(0.2)
			plt.subplots_adjust(bottom=0.3)
			plt.savefig(id+'.plot.jpg')
			plt.close()
