import sys
from scipy.stats import spearmanr
import numpy as np
if len(sys.argv) != 4:
	print("python spearman_rank_corr.py matrix.list ref_num<0,1,5,10,25,50,75,100> out.list")
	exit(0)

fw = open(sys.argv[3],'w')
fw.write('chr\tstart\tend\tspearman_rank_coef\tspearman_rank_pvalue\n')
data_ref = [float(i) for i in sys.argv[2].split(',')]
with open(sys.argv[1]) as fh:
	for lines in fh:
		if lines.startswith('chr'):
			continue
		line = lines.strip().split('\t')
		data_rank = line[3:]
		data_rank_new = [float(i) for i in data_rank]
		coef, p = spearmanr(data_rank_new, data_ref)
		fw.write('\t'.join(line[:3])+'\t'+str(coef)+'\t'+str(p)+'\n')

fw.close()
