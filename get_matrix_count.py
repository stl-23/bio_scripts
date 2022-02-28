import argparse
import pandas as pd
def getargs():
	examplelog = """EXAMPLES:
	python3 get_matrix.py -i sample.list -o1 all.count.matrix.file -o2 methy.count.matrix.file
	"""
	parser = argparse.ArgumentParser(description = "Generate matrix file",
					epilog=examplelog,
					add_help=False)
	parser.add_argument('-i', "--sample", help = "the std file list of samples")
	parser.add_argument('-o1', "--out1", help = "output all file")
	parser.add_argument('-o2', "--out2", help = "output methy file")
	#parser.add_argument('-d', "--depth", type=int,help = "filter loc that 0.25 quantile of sample < depth")
	parser.add_argument('-h', '--help', action="help",help="show the help and exit")
	return parser.parse_args()
def getmatrix(file):
	units = pd.read_table(file, dtype=str).set_index(["sample","type","file"], drop=False)
	counts = [pd.read_table(i.file, index_col=[0,1,2],usecols=[0,1,2,5],header=None) for i in units.itertuples()]
	methy = [pd.read_table(i.file, index_col=[0,1,2],usecols=[0,1,2,4],header=None) for i in units.itertuples()]
	for t, (sample, unit, file) in zip(counts, units.index):
		t.index.names = ['chr','start','end']
		t.columns = ["%s_%s"%(sample,unit)]
	for m, (sample, unit, file) in zip(methy, units.index):
		m.index.names = ['chr','start','end']
		m.columns = ["%s_%s"%(sample,unit)]
	count_matrix = pd.concat(counts, axis=1)
	methy_matrix = pd.concat(methy, axis=1)
	#count_matrix['id2'] = count_matrix['chr'].str.cat([count_matrix['start'],count_matrix['end']],sep="_")
	#methy_matrix['id2'] = methy_matrix['chr'].str.cat([methy_matrix['start'],methy_matrix['end']],sep="_")
	count_matrix_na = count_matrix.fillna(-1)
	methy_matrix_na = methy_matrix.fillna(-1)
	#print(count_matrix_na)
	#count_matrix_final = count_matrix_na[(count_matrix_na.T != -1).all() & (count_matrix_na.T != 0).any()]
	#methy_matrix_final = methy_matrix_na[(methy_matrix_na.T != -1).all() & (methy_matrix_na.T != 0).any()]
	#count_matrix_na_percent = count_matrix_na.quantile([0.2,0.25,0.5,0.75], axis = 1)
	#cols = count_matrix_na_percent.loc[:,count_matrix_na_percent.loc[0.2,:] > depth].columns
	#matrix_final = methy_matrix_na.loc[cols,:]
	#matrix_final.columns = methy_matrix_na.columns
	return count_matrix_na,methy_matrix_na


if __name__ == "__main__":
	args = getargs()
	samples = args.sample
	outfile1 = args.out1
	outfile2 = args.out2
	#depth = int(args.depth)
	count,methy = getmatrix(samples)
	count.to_csv(outfile1,sep="\t")
	methy.to_csv(outfile2,sep="\t")
