import argparse
#import scipy.stats as stats
import numpy as np
#Mann-Whitney for unequal number of two groups
#Wilcoxon for equal number of two groups
def getargs():
        examplelog = """EXAMPLES:
        python3 get_fc_wilcoxon_test.py matrix.file matrix.cal.out
        """
        parser = argparse.ArgumentParser(description = "calculate average,std,FC..",
                                        epilog=examplelog,
                                        add_help=False)
        parser.add_argument('-i', "--matrix", help = "matrix file")
        #parser.add_argument('-a', "--case",type=int, help = "case sample number")
        #parser.add_argument('-b', "--control",type=int, help = "control sample number")
        parser.add_argument('-t1', "--thres1",type=float, default=0.25,help = "the threshold of sd/mean")
        parser.add_argument('-t2', "--thres2",type=float, default=0.2,help = "the threshold of max-min")
        parser.add_argument('-o', "--out", help = "output all vaule file")
        #parser.add_argument('-o2', "--out2", help = "output signatue vaule file")
        parser.add_argument('-h', '--help', action="help",help="show the help and exit")
        return parser.parse_args()
def cal(file,thres1,thres2):
	all = []
	#sig = []
	with open(file) as fh:
		for lines in fh:
			if lines.startswith('chr'):continue
			line = lines.strip().split('\t')
			id = '\t'.join(line[:3])
			case = [ float(i) for i in line[3:] ]
			#con = [ float(i) for i in line[3+a:3+a+b] ]
			#if sum(case+con) !=0: |FC| > 1
			if sum(case) != 0 and case.count(0.0) < len(case)*0.5:  # FC >1
				case_ave = np.mean(case)
				case_std = np.std(case)
				case_max = max(case)
				case_min = min(case)
				t_sd_mean = case_std/case_ave
				#if case_min != 0:
				diff = case_max - case_min
				#else:
				#	diff = 'inf'
				#if t_sd_mean >= thres1 and diff >= case_min*thres2:
				#	continue
				#else:
				#	all.append([id,case_ave,case_std,t_sd_mean,case_max,case_min,diff])
				all.append([id,case_ave,case_std,t_sd_mean,case_max,case_min,diff])
			#elif sum(case+con) == 0:
			#	all.append([id,'0','0','0','0','NA','NA'])

	return all

if __name__ == "__main__":
	args = getargs()
	input = args.matrix
	outfile_all = args.out
	#outfile_sig = args.out2
	#case_num = args.case
	#con_num = args.control
	thres1 = float(args.thres1)
	thres2 = float(args.thres2)
	#t_pvalue = args.pvalue
	fw1 = open(outfile_all,'a')
	#fw2 = open(outfile_sig,'a')
	fw1.write('chr\tstart\tend\tcase_average\tcase_sd\tsd/mean\tcase_max\tcase_min\tdiff\n')
	#fw2.write('chr_start_end\tcase_average\tcon_average\tcase_sd\tcon_sd\tFoldChange\tpvalue\n')
	all_val = cal(input,thres1,thres2)
	for lst in all_val:
		lst_new = [str(i) for i in lst]
		fw1.write('\t'.join(lst_new)+'\n')
fw1.close()
