import sys

if len(sys.argv) != 4:
	print("python overlap.py all.pos check.pos out")
	exit(0)
fw = open(sys.argv[3],'w')
with open(sys.argv[1]) as fh1,open(sys.argv[2]) as fh2:
	dic = {}
	for rows in fh2:
		if rows.startswith('chr'):continue
		row = rows.strip().split('\t')
		chr2,start2,end2 = row[:3]
		anno = row[-1]
		if chr2 in dic:
			dic[chr2].append(start2+'_'+end2+'_'+anno)
		else:
			dic[chr2] = [start2+'_'+end2+'_'+anno]
	for lines in fh1:
		if lines.startswith('chr'):continue
		line = lines.strip().split('\t')
		chr,start,end = line[:3]
		set1 = set(range(int(start),int(end)+1))
		tmps = []
		if chr in dic:
			lst = dic[chr]
			for i in lst:
				start2,end2,anno = i.split('_')
				set2 = set(range(int(start2),int(end2)+1))
				#lst_tmp = list(set1.intersection(set2))
				lst_tmp = set1.intersection(set2)
				if lst_tmp:
					tmps = [start2,end2]
			if len(tmps) > 0:
				s2,e2 = tmps[0],tmps[1]
				fw.write(chr+'\t'+start+'\t'+end+'\t'+'1'+'\t'+str(s2)+'\t'+str(e2)+'\t'+anno+'\n')
			else:
				fw.write(chr+'\t'+start+'\t'+end+'\t'+'0'+'\t'+'-'+'\t'+'-'+'\t'+'-'+'\n')
			
		else:
			fw.write(chr+'\t'+start+'\t'+end+'\t'+'0'+'\t'+'-'+'\t'+'-'+'\t'+'-'+'\n')
fw.close()
