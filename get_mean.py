import argparse
import numpy as np
#Mann-Whitney for unequal number of two groups
#Wilcoxon for equal number of two groups
def getargs():
        examplelog = """EXAMPLES:
        python3 get_fc_wilcoxon_test.py -i matrix.file -a case_num -b con_num -o matrix.cal.out
        """
        parser = argparse.ArgumentParser(description = "calculate mean",
                                        epilog=examplelog,
                                        add_help=False)
        parser.add_argument('-i', "--matrix", help = "matrix file")
        parser.add_argument('-a', "--case",type=int, help = "case sample number")
        parser.add_argument('-b', "--control",type=int, help = "control sample number")
        #parser.add_argument('-df2', "--diff2",type=float, default=0.1, help = "the threshold of case_mean - control_mean")
        parser.add_argument('-o', "--out", help = "output all vaule file")
        #parser.add_argument('-o2', "--out2", help = "output signatue vaule file")
        parser.add_argument('-h', '--help', action="help",help="show the help and exit")
        return parser.parse_args()
def cal(file,a,b):
	all = []
	#sig = []
	with open(file) as fh:
		for lines in fh:
			if lines.startswith('chr'):continue
			line = lines.strip().split('\t')
			id = '\t'.join(line[:3])
			case = [ float(i) for i in line[3:3+a] ]
			con = [ float(i) for i in line[3+a:3+a+b] ]
			#if sum(case+con) !=0: |FC| > 1
			#if sum(case+con) != 0:  # FC >1
				#case_ave = np.mean(case)
				#con_ave = np.mean(con)
				#case_std = np.std(case)
				#con_std = np.std(con)
			case_mean = np.mean(case)
			con_mean = np.mean(con)
				#if sum(con) == 0:
				#	fc = 'inf'
				#elif sum(case) == 0:
				#	fc = '-inf'
				#else:
					#fc = list(np.log2(np.array([case_ave])/np.array([con_ave])))[0]
				#	fc = case_ave/con_ave
				#u,p = stats.mannwhitneyu(case,con,alternative='two-sided')
			diff2 = case_mean - con_mean
			all.append([id,case_mean,con_mean, diff2])
				#if float(p) < 0.05 and abs(float(fc)) >1 :
				#if float(p) < t_pvalue and (float(fc) > t_fc or fc == 'inf') and diff2 > t_diff2:
				#	sig.append([id,case_ave,con_ave,case_std,con_std,fc,p,diff2])
			#elif sum(case+con) == 0:
			#	all.append([id,'0','0','0','0','NA','NA','NA'])

	return all

if __name__ == "__main__":
	args = getargs()
	input = args.matrix
	outfile_all = args.out
	case_num = args.case
	con_num = args.control
	fw1 = open(outfile_all,'w')
	#fw2 = open(outfile_sig,'w')
	fw1.write('chr\tstart\tend\tcancer_mean\thealth_mean\tmean_diff\n')
	#fw2.write('chr\tstart\tend\tcase_average\tcon_average\tcase_sd\tcon_sd\tFoldChange\tpvalue\tmean_diff\n')
	all_val= cal(input,case_num,con_num)
	for lst in all_val:
		lst_new = [str(i) for i in lst]
		fw1.write('\t'.join(lst_new)+'\n')
fw1.close()
