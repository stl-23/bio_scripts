import sys
if len(sys.argv) != 4:
	print("python filter.py input output num")
	exit(0)
title = open(sys.argv[1]).readlines()[0].strip().split('\t')
fw = open(sys.argv[2],'w')
num = int(sys.argv[3]) # num=8
fc_index = [i for i,v in enumerate(title) if v.startswith('foldchange')]
mean_index = [ i for i,v in enumerate(title) if v.startswith('mean')]
pvalue_index = [ i for i,v in enumerate(title) if v.startswith('pvalue')]
with open(sys.argv[1]) as fh:
	for lines in fh:
		line = lines.strip().split('\t')
		if lines.startswith('id'):
			fw.write('\t'.join(line)+'\tFC_8_average\tdiff_8_average\tpvalue_8_average\n')
		else:
			forward = [ str(m)+';'+str(n)+';'+str(p) for m,n,p in zip(fc_index,mean_index,pvalue_index) if float(line[m]) >1 and float(line[n]) >0 and float(line[p]) < 0.1 ]
			reverse = [ str(m)+';'+str(n)+';'+str(p) for m,n,p in zip(fc_index,mean_index,pvalue_index) if float(line[m]) <1 and float(line[n]) <0 and float(line[p]) < 0.1 ]
			if len(forward) >= num:
				fc = [ float(line[int(i.split(';')[0])]) for i in forward ]
				diff = [ float(line[int(i.split(';')[1])]) for i in forward ]
				pvalue = [ float(line[int(i.split(';')[2])]) for i in forward ]
				fc_ave = sum(fc)/len(fc)
				diff_ave = sum(diff)/len(diff)
				pvalue_ave = sum(pvalue)/len(pvalue)
				fw.write('\t'.join(line)+'\t'+str(fc_ave)+'\t'+str(diff_ave)+'\t'+str(pvalue_ave)+'\n')
			if len(reverse) >=num:
				fc2 = [ float(line[int(i.split(';')[0])]) for i in reverse ]
				diff2 = [ float(line[int(i.split(';')[1])]) for i in reverse ]
				pvalue2 = [ float(line[int(i.split(';')[2])]) for i in reverse ]
				fc_ave2 = sum(fc2)/len(fc2)
				diff_ave2 = sum(diff2)/len(diff2)
				pvalue_ave2 = sum(pvalue2)/len(pvalue2)
				fw.write('\t'.join(line)+'\t'+str(fc_ave2)+'\t'+str(diff_ave2)+'\t'+str(pvalue_ave2)+'\n')
fw.close()
