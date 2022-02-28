#!/sxyf_keyan/04.private.person/03.fangjian/01.software/anaconda3/bin/python
# -*- coding: UTF-8 -*-

# * Author        : fangjian
# * Email         : jian.fang@genetronhealth.com
# * version       : v1.0

###### Import Module ######
import sys
import os
import argparse
import glob
import time
import math

###### Description ######
Description = '''
Description :
    Find no exist files and empty files!'''

#####CLASS#####
class HelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

def fmt_time(spend_time):
    spend_time = int(spend_time)
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if spend_time < 60:
        return "%ds" % math.ceil(spend_time)
    elif spend_time > day:
        days = divmod(spend_time,day)
        return "%dd%s" %(int(days[0]),fmt_time(days[1]))
    elif spend_time > hour:
        hours = divmod(spend_time,hour)
        return "%dh%s" %(int(hours[0]),fmt_time(hours[1]))
    else:
        mins = divmod(spend_time, min)
        return "%dm%s" %(int(mins[0]),math.ceil(mins[1]))

def checkEmpty(existfileList,prefix):
    with open("%s.emptyFile.txt"%(prefix),'w') as emptyFile:
        for filePath in existfileList:
            size = os.path.getsize(filePath)
            if size:
                continue
            else:
                emptyFile.write("%s\n"%(filePath))

def fileExist(infile,colNum,prefix):
    existfileList = []
    with open(infile,'r') as inFile,\
    open("%s.realFile.txt"%(prefix),'w') as realFile,\
    open("%s.noFile.txt"%(prefix),'w') as noFile,\
    open("%s.moreFile.txt"%(prefix),'w') as moreFile:
        for line in inFile:
            line = line.strip()
            lineList = line.split("\t")
            filePath = lineList[int(colNum)-1]
            #print(filePath)
            infoList = lineList[0:int(colNum)-1]    ## add info  前面信息；
            otherList = lineList[int(colNum):]      ## add info  后面信息；
            filePathList = glob.glob(filePath)
            #print(filePathList)
            if len(filePathList) == 0:
                noFile.write("%s\n"%(line))
            elif len(filePathList) == 1:
                #print(len(otherList))
                if len(otherList ) > 0:
                    realFile.write("%s\t%s\t%s\n"%("\t".join(infoList),filePathList[0],"\t".join(otherList)))
                else:
                    realFile.write("%s\t%s\n"%("\t".join(infoList),filePathList[0]))
                existfileList.append(filePathList[0])
            else:
                moreFile.write("%s\n"%(line))
    return existfileList


#####FUNC#####
def options():
    parser = argparse.ArgumentParser(formatter_class=HelpFormatter,description=Description)
    parser.add_argument('-in', help='input path file ', dest='infile', type=str, action='store', required=True)
    parser.add_argument('-p', help='prefix of output file', dest='prefix', type=str, action='store', default="test")
    parser.add_argument('-col', help='Number of columns in the file', dest='colNum', type=int, action='store', default=1)
    args = parser.parse_args()
    return args

def main():
    args = options()
    filePathList = fileExist(args.infile,args.colNum,args.prefix)
    checkEmpty(filePathList,args.prefix)

if __name__ == '__main__':
    try:
        sta = time.time()
        main()
        end = time.time()
        print('spend time:%s'%fmt_time(end-sta))
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
