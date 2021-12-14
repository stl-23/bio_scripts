import sys
if len(sys.argv) != 4:
	print("python union.py new.list old.list out.list")
	exit(0)

fw = open(sys.argv[3],'w')
fw.write('\t'.join(['chr','start','end','case_average','con_average','case_sd','con_sd','FC','pvalue','median_diff','case_average','con_average','case_sd','con_sd','FC','pvalue','median_diff'])+'\n')
with open(sys.argv[1]) as fh1,open(sys.argv[2]) as fh2:
	dic1 = {}
	dic2 = {}
	for lines in fh1:
		line = lines.strip().split("\t")
		info1 = '_'.join(line[:3])
		dic1[info1] = '\t'.join(line[3:])
	for rows in fh2:
		row = rows.strip().split("\t")
		info2 = '_'.join(row[:3])
		dic2[info2] = '\t'.join(row[3:])
	unionset = set(dic1.keys()).union(set(dic2.keys()))
	for i in unionset:
		if i in dic1 and i in dic2:
			fw.write('\t'.join(i.split('_'))+'\t'+dic1[i]+'\t'+dic2[i]+'\n')
		elif i in dic1 and i not in dic2:
			fw.write('\t'.join(i.split('_'))+'\t'+dic1[i]+'\t'+'-\t'*7+'\n')
		elif i in dic2 and i not in dic1:
			fw.write('\t'.join(i.split('_'))+'\t'+'-\t'*7+ dic2[i]+'\n')
fw.close()
