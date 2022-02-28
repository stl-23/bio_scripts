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
	parser.add_argument('-p', "--percent",type=float,default=1.0,help = "percentage threshold,of Nan or -1")
	parser.add_argument('-h', '--help', action="help",help="show the help and exit")
	return parser.parse_args()
def getmatrix(file,percent):
	units = pd.read_table(file, dtype=str).set_index(["sample","type","file"], drop=False)
	counts = [pd.read_table(i.file,index_col=[0,1,2], usecols=[0,1,2,6],header=None) for i in units.itertuples()]
	for t, (sample, unit, file) in zip(counts, units.index):
		t.index.names = ['chr','start','end']
		t.columns = ["%s_%s"%(sample,unit)]
	matrix = pd.concat(counts, axis=1)
	matrix_na2zero = matrix.fillna(-1)
	cl_num_t = matrix_na2zero.shape[1]*percent
	matrix_final = matrix_na2zero[((matrix_na2zero == -1).sum(axis=1) <= cl_num_t)]

	return matrix,matrix_final


if __name__ == "__main__":
	args = getargs()
	samples = args.sample
	outfile1 = args.out1
	outfile2 = args.out2
	percent = args.percent
	matrix,matrix_final = getmatrix(samples,percent)
	matrix.to_csv(outfile1,sep="\t")
	matrix_final.to_csv(outfile2,sep="\t")
