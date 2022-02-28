#!/usr/bin/env python
import os
import sys
import subprocess
import gzip
from multiprocessing import Pool as ThreadPool

def get_matrix(chr_len,file,name):
	dic = {}
	with gzip.open(file,'rt', encoding='utf-8') as fh:
		for lines in fh:
			lst = lines.strip().split('\t')
			dic[int(lst[1])] = lst[2]
	#lst_out = [dic[x] if x in dic else '0' for x in range(1,int(chr_len)+1)]
	fw2 = open(name+'.addpos.sort.list','a')
	fw2.write(name+'\n')
	for x in range(1,int(chr_len)+1):
		if x in dic:
			fw2.write(str(dic[x])+'\n')
		else:
			fw2.write('0'+'\n')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("python search_diff_regions_with_each_site_v4.py all_sample.list chr_length chunk_num")
        exit(0)
    files = [i.strip().split('\t')[-1] for i in open(sys.argv[1]).readlines()[1:]]
    samples = [i.strip().split('\t')[0] for i in open(sys.argv[1]).readlines()[1:]]
    chr_len = sys.argv[2]
    jobs = int(sys.argv[3])
    #fw1 = open('chr.list','a')
    #thread_counts = int(sys.argv[3])
    #for x in range(1,int(chr_len)+1):
    #	fw1.write(str(x)+'\n')
    parameters = [(chr_len,)+(row,sample) for row,sample in zip(files,samples)]
    for i in range(0, len(parameters), jobs):
        subpms = parameters[i:i + jobs]
        pool = ThreadPool(jobs)
        pool.starmap(get_matrix,subpms)
        pool.close()
