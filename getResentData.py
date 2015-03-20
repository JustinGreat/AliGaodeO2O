#!/usr/bin/python

import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import traceback

RIGHT = '0'
ERROR = '1'
MAX_RETRY = 2

def testGetUrlData(url,param = ""):
    code = ERROR
    content = ""
    count = 0
    while count < MAX_RETRY:
        try:
            if param != "":
                connect = urllib2.urlopen(url,param)
            else:
                connect = urllib2.urlopen(url)
            content = connect.read()
            content.close()
            code = RIGHT
        except:
            print url
            sys.stdout.flush()
            traceback.print_exc()
            code = ERROR
        count+=1
        if code == RIGHT:
            break
 
        return code,content

def Start():
    f_p=open('./data/pass_worklist_failed','a')
    f_un=open('./data/unprocess_worklist_failed','a')
    
    urladdr="http://10.16.24.69/ces/api/aligd/vi/getresult?prepare_id=897414&key=A5E13AC7-8055-47D9-912D-39099BADB731&prepare_id=2712249"
    code,datas=testGetUrlData(urladdr)
    if code == ERROR:
        print "alio2o_resend:get url data ERROR"
        return
    datas.split('\n')
    for data in datas:
        data = data[:-1]
        try:
            data_json=json.load(data)
        except:
            print "ERROR when resolving json data\n"
        status=int(data_json.get("process_status"))
        if status == 1:
            f_un.write(data+'\n')
        elif status == 0:
            f_p.write(data+'\n')
    f_un.close()
    f_p.close()
    os.system("python ProcessPassWorklist.py")
    os.system("python ProcessUnprocessWorklist.py")    


if __name__ == "__main__":
    Start()
