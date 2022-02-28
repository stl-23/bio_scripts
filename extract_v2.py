import sys
import pandas as pd

if len(sys.argv) != 3:
	print("python extrac.py marker.info matrix.file")
	exit(0)

data = pd.read_csv(sys.argv[2],sep="\t",header=0)
cols = list(data.columns)
cols_new = [ i.split('_')[-1] for i in cols ]
#with open(sys.argv[1]) as fh1:
fh1= open(sys.argv[1]).readlines()
for index,lines in enumerate(fh1):
	index_lst = []
	if lines.startswith('paper'):continue
	line = lines.strip().split('\t')
	pos,anno= line[1],line[2:]
	anno_new = [ i.split('_')[-1] for i in anno ]
	inter = [a for a in anno_new if a in cols_new]
	if inter:
		anno_new_add = anno_new + ['health','standard']
	else:
		anno_new_add = anno_new
	for k in anno_new_add:
		for i,v in enumerate(cols_new):
			if k == v:
				index_lst.append(i)
	if len(index_lst) != 0:
		index_lst_new = [0,1,2]+ index_lst
		subdata  = data.iloc[[index-1] ,index_lst_new]
		subdata.to_csv(pos+'.list',sep="\t",index=0)
