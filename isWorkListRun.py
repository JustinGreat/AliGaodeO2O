#!/usr/bin/python

import os
import sys

def WorklistRun():
    if os.path.exist("processPassWorklist_pid"):
        os.system("rm processPassWorklist_pid")
    if os.path.exist("processUnprocessWorklist_pid"):
        os.system("rm processUnprocessWorklist_pid")
    os.system('ps -ef | grep processPassWorklist.py > processPassWorklist_pid')
    os.system('ps -ef | grep processUnprocessWorklist.py > processUnprocessWorklist_pid')
    lines=[line for line in file('processPassWorklist_pid')]
    for line in lines:
        if line.find('python processPassWorklist.py')!=-1:
            return True


    lines=[line for line in file('processUnprocessWorklist_pid')]
    for line in lines:
        if line.find('python processUnprocessWorklist.py')!=-1:
            return True
    return False

if WorklistRun():
    sys.exit(1)
os.system('./getResentData.py')
