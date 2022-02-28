import sys
import random

if len(sys.argv) != 3:
	print("python random_select.py input percent_of_each_group")
	exit(0)
percent = float(sys.argv[2])
dic = {}
fw = open('train.list','w')
fw2 = open('test.list','w')

with open(sys.argv[1]) as fh1:
	for lines in fh1:
		line = lines.strip().split('\t')
		if lines.startswith('sample'):
			title = line
			#title[0] = ''
			title = '\t'.join(title)
		else:
			group = line[0]
			if group in dic:
				dic[group].append(lines.strip())
			else:
				dic[group] = [lines.strip()]
	rand_sample = []
	remain_sample = []
	for i in dic:
		lst = dic[i]
		rand_index = random.sample(range(0,len(lst)),round(len(lst)*percent))
		remain_index = set(range(0,len(lst))) - set(rand_index)
		remain_index = list(remain_index)
		rand_sample += [ lst[m] for m in rand_index ]
		remain_sample += [ lst[n] for n in remain_index ]

fw.write(title+'\n'+'\n'.join(rand_sample))
fw2.write(title+'\n'+'\n'.join(remain_sample))

fw.close()
fw2.close()
