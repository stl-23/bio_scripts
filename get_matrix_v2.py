#/usr/bin/env python
import argparse
import pandas as pd
def getargs():
	examplelog = """EXAMPLES:
	python3 get_matrix.py sample.list out.matrix.file
	"""
	parser = argparse.ArgumentParser(description = "Generate matrix file",
					epilog=examplelog,
					add_help=False)
	parser.add_argument('-i', "--sample", help = "the std file list of samples")
	parser.add_argument('-o1', "--out1", help = "output all file")
	parser.add_argument('-o2', "--out2", help = "output filterd file")
	parser.add_argument('-d', "--depth", type=int,help = "filter loc that 0.20 quantile of sample < depth")
	parser.add_argument('-h', '--help', action="help",help="show the help and exit")
	return parser.parse_args()
def getmatrix(file,depth):
	units = pd.read_table(file, dtype=str).set_index(["sample","type","file"], drop=False)
	counts = [pd.read_table(i.file,index_col=[0,1,2], usecols=[0,1,2,5],header=None) for i in units.itertuples()]
	freqs = [pd.read_table(i.file,index_col=[0,1,2], usecols=[0,1,2,6],header=None) for i in units.itertuples()]
	for t, (sample, unit, file) in zip(counts, units.index):
		t.index.names = ['chr','start','end']
		t.columns = ["%s_%s"%(sample,unit)]
	for m, (sample, unit, file) in zip(freqs, units.index):
		m.index.names = ['chr','start','end']
		m.columns = ["%s_%s"%(sample,unit)]
	count_matrix = pd.concat(counts, axis=1)
	freq_matrix = pd.concat(freqs, axis=1)
	#freq_matrix['id'] = freq_matrix['chr'].map(str)+'_'+freq_matrix['start'].map(str)+'_'+freq_matrix['end'].map(str)
	#freq_matrix = freq_matrix.drop(columns=['chr','start','end'])
	count_matrix_na = count_matrix.fillna(-1).astype(float)
	freq_matrix_na = freq_matrix.fillna(-1).astype(float)
	#print(count_matrix_na)
	#matrix_final = matrix_na2[(matrix_na2zero.T != -1).all() & (matrix_na2zero.T != 0).all()]
	count_matrix_na_percent = count_matrix_na.quantile([0.2,0.25,0.5,0.75], axis = 1)
	cols = count_matrix_na_percent.loc[:,count_matrix_na_percent.loc[0.2,:] > depth].columns
	matrix_final = freq_matrix_na.loc[cols,:]
	matrix_final.columns = freq_matrix_na.columns
	matrix_final = matrix_final[(matrix_final.T != -1).all()]
	return freq_matrix_na,matrix_final


if __name__ == "__main__":
	args = getargs()
	samples = args.sample
	outfile1 = args.out1
	outfile2 = args.out2
	depth = int(args.depth)
	matrix,matrix_final = getmatrix(samples,depth)
	matrix.to_csv(outfile1,sep="\t")
	matrix_final.to_csv(outfile2,sep="\t")
