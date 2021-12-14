import argparse
import collections
def getargs():
	examplelog = """EXAMPLES:
	python3 get_std.py matrix.file std.matrix.file
	"""
	parser = argparse.ArgumentParser(description = "Stardard matrix file",
					epilog=examplelog,
					add_help=False)
	parser.add_argument('-i', "--input", help = "the matrix file of all sample")
	parser.add_argument('-o', "--out", help = "output file")
	parser.add_argument('-h', '--help', action="help",help="show the help and exit")
	return parser.parse_args()

def std(file):
	std_samples = collections.OrderedDict()
	with open(file) as fh:
		for lines in fh:
			if lines.startswith('chr'):
				title = lines
			else:
				line = lines.strip().split('\t')
				id = '_'.join(line[:3])
				samples_data = [ float(i) for i in line[3:]]
				min_num = min(samples_data)
				max_num = max(samples_data)
				if min_num == max_num: # no significant
					#std_samples[id] = [0]*len(line[3:])
					continue
				else:
					std_sample = [ (i - min_num)/(max_num - min_num) for i in samples_data]
					std_samples[id] = std_sample
	return title,std_samples

if __name__ == "__main__":
	args = getargs()
	input = args.input
	outfile = args.out
	title,std_data = std(input)
	fw = open(outfile,'w')
	fw.write(title)
	for id in std_data:
		fw.write('\t'.join([str(x) for x in id.split('_')])+'\t'+'\t'.join([str(i) for i in std_data[id]])+'\n')

	fw.close()
