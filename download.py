#!/usr/bin/env python
import os
import sys
import subprocess
from multiprocessing.dummy import Pool as ThreadPool

def run_shell_cmd(cmd):
    run = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if run.returncode == 0:
        print("STDOUT:", run.stdout)
    else:
        print("STDOUT:", run.stdout)
        print("STDERR:", run.stderr)

def multi_run(func,cmds,jobs,maxc):
    ## split command into sub-commands,
    ## each sub-command has {jobs} tasks
    ## run {jobs} tasks parallelly to save time
    if isinstance(cmds,list):
        for i in range(0, len(cmds), jobs):
            subcmds = cmds[i:i + jobs]
            pool = ThreadPool(maxc)
            pool.map(func, subcmds)
            pool.close()
            pool.join()
    elif isinstance(cmds,str):
        new_cmds = [cmds]
        pool = ThreadPool(maxc)
        pool.map(func, new_cmds)
        pool.close()
        pool.join()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("python download.py command_file job_number thread_counts")
        exit(0)
    cmds = [i.strip() for i in open(sys.argv[1]).readlines()]
    jobs = int(sys.argv[2])
    thread_counts = int(sys.argv[3])
    multi_run(run_shell_cmd,cmds,jobs,thread_counts)
