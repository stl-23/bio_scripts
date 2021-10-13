#!/usr/bin/env python
import os
import sys
import subprocess
from multiprocessing.dummy import Pool as ThreadPool

#def run_shell_cmd(cmd):
#    run = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#    if run.returncode == 0:
#        print("STDOUT:", run.stdout)
#    else:
#        print("STDOUT:", run.stdout)
#        print("STDERR:", run.stderr)
def run_shell_cmd(cmd):
    ## code from https://github.com/XWangLabTHU/cfDNApipe/blob/master/cfDNApipe/cfDNA_utils.py
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
    )
    while True:
        nextline = proc.stdout.readline()
        if (nextline == "") and (proc.poll() is not None):
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    output, error = proc.communicate()
    exitCode = proc.returncode

    if exitCode != 0:
        print(output)
        print(error)

def multi_run(func,cmds,jobs):
    ## split command into sub-commands,
    ## each sub-command has {jobs} tasks
    ## run {jobs} tasks parallelly to save time
    if isinstance(cmds,list):
        for i in range(0, len(cmds), jobs):
            subcmds = cmds[i:i + jobs]
            pool = ThreadPool(jobs)
            pool.map(func, subcmds)
            pool.close()
            pool.join()
    elif isinstance(cmds,str):
        new_cmds = [cmds]
        pool = ThreadPool(jobs)
        pool.map(func, new_cmds)
        pool.close()
        pool.join()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("python download.py command_file job_number")
        exit(0)
    cmds = [i.strip() for i in open(sys.argv[1]).readlines()]
    jobs = int(sys.argv[2])
    #thread_counts = int(sys.argv[3])
    multi_run(run_shell_cmd,cmds,jobs)
