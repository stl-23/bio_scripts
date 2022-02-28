import sys
if len(sys.argv) != 4:
	print("python filter.py input output num")
	exit(0)
title = open(sys.argv[1]).readlines()[0].strip().split('\t')
fw = open(sys.argv[2],'w')
num = int(sys.argv[3]) # num=8
mean_fc_index = [i for i,v in enumerate(title) if v.startswith('mean_foldchange')]
mean_diff_index = [ i for i,v in enumerate(title) if v.startswith('mean_diff')]
pvalue_index = [ i for i,v in enumerate(title) if v.startswith('pvalue')]
median_fc_index = [ i for i,v in enumerate(title) if v.startswith('median_foldchange')]
median_diff_index = [ i for i,v in enumerate(title) if v.startswith('median_diff')]
cancer_median_index = [ i for i,v in enumerate(title) if v.startswith('cancer_median')]
normal_median_index = [ i for i,v in enumerate(title) if v.startswith('normal_median')]
cancer_mean_index = [ i for i,v in enumerate(title) if v.startswith('cancer_mean')]
normal_mean_index = [ i for i,v in enumerate(title) if v.startswith('normal_mean')]
with open(sys.argv[1]) as fh:
	for lines in fh:
		line = lines.strip().split('\t')
		if lines.startswith('id'):
			fw.write('\t'.join(line)+'\tmean_FC_average\tmean_diff_average\tpvalue_average\tmedian_FC_average\tmedian_diff_average\tcancer_median_average\tnormal_median_average\tcancer_mean_average\tnormal_mean_average\n')
		else:
			forward = [ str(m)+';'+str(n)+';'+str(p)+';'+str(q)+';'+str(r)+';'+str(s)+';'+str(t)+';'+str(u)+';'+str(v) for m,n,p,q,r,s,t,u,v in zip(mean_fc_index,mean_diff_index,pvalue_index,median_fc_index,median_diff_index,cancer_median_index,normal_median_index,cancer_mean_index,normal_mean_index) if float(line[m]) >1 and float(line[n]) >0 and float(line[p]) < 0.1]
			reverse = [ str(m)+';'+str(n)+';'+str(p)+';'+str(q)+';'+str(r)+';'+str(s)+';'+str(t)+';'+str(u)+';'+str(v) for m,n,p,q,r,s,t,u,v in zip(mean_fc_index,mean_diff_index,pvalue_index,median_fc_index,median_diff_index,cancer_median_index,normal_median_index,cancer_mean_index,normal_mean_index) if float(line[m]) <1 and float(line[n]) <0 and float(line[p]) < 0.1]
			if len(forward) >= num:
				mean_fc = [ float(line[int(i.split(';')[0])]) for i in forward ]
				mean_diff = [ float(line[int(i.split(';')[1])]) for i in forward ]
				pvalue = [ float(line[int(i.split(';')[2])]) for i in forward ]
				median_fc = [ float(line[int(i.split(';')[3])]) for i in forward ]
				median_diff = [ float(line[int(i.split(';')[4])]) for i in forward ]
				cancer_median = [ float(line[int(i.split(';')[5])]) for i in forward ]
				normal_median = [ float(line[int(i.split(';')[6])]) for i in forward ]
				cancer_mean = [ float(line[int(i.split(';')[7])]) for i in forward ]
				normal_mean = [ float(line[int(i.split(';')[8])]) for i in forward ]
				mean_fc_ave = sum(mean_fc)/len(mean_fc) 
				mean_diff_ave = sum(mean_diff)/len(mean_diff)
				pvalue_ave = sum(pvalue)/len(pvalue)
				median_fc_ave = sum(median_fc)/len(median_fc)
				median_diff_ave = sum(median_diff)/len(median_diff)
				cancer_median_ave = sum(cancer_median)/len(cancer_median)
				normal_median_ave = sum(normal_median)/len(normal_median)
				cancer_mean_ave = sum(cancer_mean)/len(cancer_mean)
				normal_mean_ave = sum(normal_mean)/len(normal_mean)
				fw.write('\t'.join(line)+'\t'+str(mean_fc_ave)+'\t'+str(mean_diff_ave)+'\t'+str(pvalue_ave)+'\t'+str(median_fc_ave)+'\t'+str(median_diff_ave)+'\t'+str(cancer_median_ave)+'\t'+str(normal_median_ave)+'\t'+str(cancer_mean_ave)+'\t'+str(normal_mean_ave)+'\n')
			if len(reverse) >=num:
				fc2 = [ float(line[int(i.split(';')[0])]) for i in reverse ]
				diff2 = [ float(line[int(i.split(';')[1])]) for i in reverse ]
				pvalue2 = [ float(line[int(i.split(';')[2])]) for i in reverse ]
				md_fc2 = [ float(line[int(i.split(';')[3])]) for i in reverse ]
				md_diff2 = [ float(line[int(i.split(';')[4])]) for i in reverse ]
				c_md2 = [ float(line[int(i.split(';')[5])]) for i in reverse ]
				n_md2 = [ float(line[int(i.split(';')[6])]) for i in reverse ]
				c_mn2 = [ float(line[int(i.split(';')[7])]) for i in reverse ]
				n_md2 = [ float(line[int(i.split(';')[8])]) for i in reverse ]
				fc_ave2 = sum(fc2)/len(fc2)
				diff_ave2 = sum(diff2)/len(diff2)
				pvalue_ave2 = sum(pvalue2)/len(pvalue2)
				md_fc_ave2 = sum(md_fc2)/len(md_fc2)
				md_diff_ave2 = sum(md_diff2)/len(md_diff2)
				c_md_ave2 = sum(c_md2)/len(c_md2)
				n_md_ave2 = sum(n_md2)/len(n_md2)
				c_mn_ave2 = sum(c_mn2)/len(c_mn2)
				n_md_ave2 = sum(n_md2)/len(n_md2)
				fw.write('\t'.join(line)+'\t'+str(fc_ave2)+'\t'+str(diff_ave2)+'\t'+str(pvalue_ave2)+'\t'+str(md_fc_ave2)+'\t'+str(md_diff_ave2)+'\t'+str(c_md_ave2)+'\t'+str(n_md_ave2)+'\t'+str(c_mn_ave2)+'\t'+str(n_md_ave2)+'\n')
fw.close()
