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
	parser.add_argument('-o', "--out", help = "output file")
	parser.add_argument('-h', '--help', action="help",help="show the help and exit")
	return parser.parse_args()
def getmatrix(file):
	units = pd.read_table(file, dtype=str).set_index(["sample","type","file"], drop=False)
	counts = [pd.read_table(i.file,index_col=[0,1,2], usecols=[0,1,2,8]) for i in units.itertuples()]
	for t, (sample, unit, file) in zip(counts, units.index):
		t.columns = ["%s_%s" % (sample,unit)] 
	matrix = pd.concat(counts, axis=1)
	matrix.index.name = "position"
	matrix_na2zero = matrix.fillna(0)
	#matrix_final = matrix_na2zero[(matrix_na2zero.T != 0).any()]
	#print(matrix_na2zero[matrix_na2zero.columns[0:2]].mean(axis=1))

	#matrix_na2zero.to_csv('out', sep="\t")
	return matrix_na2zero


if __name__ == "__main__":
	args = getargs()
	samples = args.sample
	outfile = args.out
	matrix = getmatrix(samples)
	matrix.to_csv(outfile,sep="\t")
