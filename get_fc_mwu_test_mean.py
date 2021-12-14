import argparse
import scipy.stats as stats
import numpy as np
#Mann-Whitney for unequal number of two groups
#Wilcoxon for equal number of two groups
def getargs():
        examplelog = """EXAMPLES:
        python3 get_fc_wilcoxon_test.py -i matrix.file -a case_num -b con_num -fc 1 -p 0.05 -df1 0.2 -df2 0.1 -o1 matrix.cal.out        -o2 matrix.cal.out.sig
        """
        parser = argparse.ArgumentParser(description = "calculate average,std,FC..",
                                        epilog=examplelog,
                                        add_help=False)
        parser.add_argument('-i', "--matrix", help = "matrix file")
        parser.add_argument('-a', "--case",type=int, help = "case sample number")
        parser.add_argument('-b', "--control",type=int, help = "control sample number")
        parser.add_argument('-fc', "--fc",type=float, default=1.0, help = "the threshold of Fold change")
        parser.add_argument('-p', "--pvalue",type=float, default=0.05,help = "the threshold of pvalue")
        parser.add_argument('-df2', "--diff2",type=float, default=0.1, help = "the threshold of case_mean - control_mean")
        parser.add_argument('-o1', "--out1", help = "output all vaule file")
        parser.add_argument('-o2', "--out2", help = "output signatue vaule file")
        parser.add_argument('-h', '--help', action="help",help="show the help and exit")
        return parser.parse_args()
def cal(file,a,b,t_fc,t_pvalue,t_diff2):
	all = []
	sig = []
	with open(file) as fh:
		for lines in fh:
			if lines.startswith('chr'):continue
			line = lines.strip().split('\t')
			id = '\t'.join(line[:3])
			case = [ float(i) for i in line[3:3+a] ]
			con = [ float(i) for i in line[3+a:3+a+b] ]
			#if sum(case+con) !=0: |FC| > 1
			if sum(case+con) != 0:  # FC >1
				case_ave = np.mean(case)
				con_ave = np.mean(con)
				case_std = np.std(case)
				con_std = np.std(con)
				case_mean = np.mean(case)
				con_mean = np.mean(con)
				if sum(con) == 0:
					fc = 'inf'
				#elif sum(case) == 0:
				#	fc = 'inf'
				else:
					#fc = list(np.log2(np.array([case_ave])/np.array([con_ave])))[0]
					fc = case_ave/con_ave
				u,p = stats.mannwhitneyu(case,con,alternative='two-sided')
				diff2 = case_mean - con_mean
				all.append([id,case_ave,con_ave,case_std,con_std,fc,p,diff2])
				#if float(p) < 0.05 and abs(float(fc)) >1 :
				if float(p) < t_pvalue and (float(fc) > t_fc or fc == 'inf') and diff2 > t_diff2:
					sig.append([id,case_ave,con_ave,case_std,con_std,fc,p,diff2])
			elif sum(case+con) == 0:
				all.append([id,'0','0','0','0','NA','NA','NA'])

	return all,sig

if __name__ == "__main__":
	args = getargs()
	input = args.matrix
	outfile_all = args.out1
	outfile_sig = args.out2
	case_num = args.case
	con_num = args.control
	t_fc = args.fc
	t_pvalue = args.pvalue
	t_diff2 = args.diff2  #mean
	fw1 = open(outfile_all,'w')
	fw2 = open(outfile_sig,'w')
	fw1.write('chr\tstart\tend\tcase_average\tcon_average\tcase_sd\tcon_sd\tFoldChange\tpvalue\tmean_diff\n')
	fw2.write('chr\tstart\tend\tcase_average\tcon_average\tcase_sd\tcon_sd\tFoldChange\tpvalue\tmean_diff\n')
	all_val,sig_val = cal(input,case_num,con_num,t_fc,t_pvalue,t_diff2)
	for lst in all_val:
		lst_new = [str(i) for i in lst]
		fw1.write('\t'.join(lst_new)+'\n')
	for lst2 in sig_val:
		lst2_new = [str(i) for i in lst2]
		fw2.write('\t'.join(lst2_new)+'\n')
fw1.close()
fw2.close()
