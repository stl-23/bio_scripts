import os
import sys
import argparse
import time
import subprocess
def getargs():
        examplelog = """EXAMPLES:
        python3 auto_k8s_job.py -i shell.sh -l 30 -k stl -t 1.2;0;0
        """
        parser = argparse.ArgumentParser(description = "auto submit jobs",
                                        epilog=examplelog,
                                        add_help=False)
        parser.add_argument('-i', "--input", help = "the input job file")
        parser.add_argument('-l', "--line", type=int,default=1,help = "the number of jobs to run at each time")
        parser.add_argument('-k', "--keyword", help = "keyword for search your k8s jobs")
        parser.add_argument('-t', "--wtime",help = "xx hour:xx minute:xx second. For example: 0:30:0 ,means waiting for 30 minutes for a chunk of jobs")
        parser.add_argument('-h', '--help', action="help",help="show the help and exit")
        return parser.parse_args()

def sleeptime(hour,min,sec):
	return hour*3600+min*60+sec

def runjobs(chunk_job):
	for i in chunk_job:
		#os.system("{}".format(i))
		subprocess.Popen(i,stdout=subprocess.PIPE,shell=True)

def checkjobs(keyword,chun_job,wait2):
	cmd = "/bionfsdate/Software/bin/ags --kubeconfig /bionfsdate/ctDNA/experiment/lishaobo/K8S/ali_info/.sxyf-21node.config -n sxyf list |grep {} | grep Running| wc -l".format(keyword)
	res = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
	for line in res.stdout.readlines():
    		remain_jobs = int(line.decode("utf-8").strip())
		#return remain_jobs
	print(remain_jobs)
	if remain_jobs  >= len(chun_job)*0.3:
		time.sleep(wait2)
		checkjobs(keyword,chun_job,wait2)
		#return remain_jobs_new
	#else:
#		time.sleep(wait3)
		#return remain_jobs
if __name__ == "__main__":
	args = getargs()
	input_jobs = args.input
	line = args.line
	keyword = args.keyword
	wtime = args.wtime
	h,m,s = wtime.strip().split(":")
	wait1 = sleeptime(float(h),float(m),float(s))
	wait2 = sleeptime(0,5,0)
	#wait3 = sleeptime(0,0,2)
	jobs = [ i.strip() for i in open(input_jobs).readlines()]
	for i in range(0,len(jobs),line):
		if i+line >= len(jobs):
			chunk_job = jobs[i:len(jobs)]
		else:
			chunk_job = jobs[i:i + line]
		runjobs(chunk_job)
		time.sleep(wait1)
		checkjobs(keyword,chunk_job,wait2)
