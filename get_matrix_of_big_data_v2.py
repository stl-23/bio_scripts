import os
import argparse
#import pandas as pd
def getargs():
	examplelog = """EXAMPLES:
	python3 get_matrix.py sample.list out.matrix.file
	"""
	parser = argparse.ArgumentParser(description = "Generate matrix file",
					epilog=examplelog,
					add_help=False)
	parser.add_argument('-i', "--sample", help = "the std file list of samples")
	parser.add_argument('-o1', "--out1", help = "output reads file")
	parser.add_argument('-o2', "--out2", help = "output freq file")
	#parser.add_argument('-d', "--depth", type=int,help = "filter loc that 0.25 quantile of sample < depth")
	parser.add_argument('-h', '--help', action="help",help="show the help and exit")
	return parser.parse_args()
def getmatrix(file,outfile1,outfile2):
	samples = []
	types = []
	files = []
	with open(file) as fh_list:
		for lines in fh_list:
			if lines.startswith('sample'):continue
			line = lines.strip().split('\t')
			sample,type,file = line[:]
			samples.append(sample)
			types.append(type)
			files.append(file)
			titles = ['id']+ [sample+'_'+type for sample,type in zip(samples,types)]
		fw = open('titles','w').write('\t'.join(titles)+'\n')
		os.system("""awk 'BEGIN{FS=OFS="\t"}''NR==FNR{b[$1"_"$2"_"$3]=$5}NR>FNR{if($1"_"$2"_"$3 in b){print $1"_"$2"_"$3,b[$1"_"$2"_"$3],$5}}' {} {} > {}""".format(files[0],files[1],'outreads1'))
		os.system("""awk 'BEGIN{FS=OFS="\t"}''NR==FNR{b[$1"_"$2"_"$3]=$5}NR>FNR{if($1"_"$2"_"$3 in b){print $1"_"$2"_"$3,b[$1"_"$2"_"$3],$5}}' {} {} > {}""".format(files[0],files[1],'outfreq1'))
		for i in range(2,len(files)-1):
			os.system("""awk 'BEGIN{FS=OFS="\t"}''NR==FNR{b[$1"_"$2"_"$3]=$0}NR>FNR{if($1"_"$2"_"$3 in b){print b[$1"_"$2"_"$3],$5}}' {} {} > {}""".format('outreads'+str(i-1),files[i],'outreads'+str(i)))
			os.system("""awk 'BEGIN{FS=OFS="\t"}''NR==FNR{b[$1"_"$2"_"$3]=$0}NR>FNR{if($1"_"$2"_"$3 in b){print b[$1"_"$2"_"$3],$5}}' {} {} > {}""".format('outfreq'+str(i-1),files[i],'outfreq'+str(i)))
		os.system("""cat titles {} > {}""".format('outfreq'+str(len(files)-1),outfile1))
		os.system("""rm outreads* outfreq*""")
if __name__ == "__main__":
	args = getargs()
	samples = args.sample
	outfile1 = args.out1
	outfile2 = args.out2
	#depth = int(args.depth)
	getmatrix(samples,outfile1,outfile2)
	#matrix.to_csv(outfile1,sep="\t")
	#matrix_final.to_csv(outfile2,sep="\t")
