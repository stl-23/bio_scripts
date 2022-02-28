import sys
import random

if len(sys.argv) != 4:
	print("python random_select.py input percent_of_each_group out_prefix")
	exit(0)
percent = float(sys.argv[2])
out_prefix = sys.argv[3]
dic = {}
fw = open(out_prefix+'.select.list','w')
fw2 = open(out_prefix+'.remain.list','w')

with open(sys.argv[1]) as fh1:
	for lines in fh1:
		line = lines.strip().split('\t')
		if lines.startswith('sample'):
			continue
		else:
			group = line[0]
			dic[group] = lines.strip()
			#if group in dic:
			#	dic[group].append(lines.strip())
			#else:
			#	dic[group] = [lines.strip()]
	rand_sample = []
	remain_sample = []
	lst = list(dic.keys())
	if percent <=1:
		rand_index = random.sample(range(0,len(lst)),round(len(lst)*percent))
	else:
		rand_index = random.sample(range(0,len(lst)),round(percent))
	remain_index = set(range(0,len(lst))) - set(rand_index)
	remain_index = list(remain_index)
	rand_sample += [ dic[lst[m]] for m in rand_index ]
	remain_sample += [ dic[lst[n]] for n in remain_index ]

fw.write('\n'.join(rand_sample)+'\n')
fw2.write('\n'.join(remain_sample)+'\n')

fw.close()
fw2.close()
