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
            connect.close()
            code = RIGHT
        except:
            print url
            sys.stdout.flush()
            traceback.print_exc()
            code = ERROR
        count+=1
        if code == RIGHT:
            break
    print "Datas:%s"%content
    return code,content

def Start():
    f_p=open('./data/pass_worklist_failed','a')
    f_un=open('./data/unprocess_worklist_failed','a')
    datas=""
    urladdr="http://10.16.24.69/ces/api/aligd/v1/getresult?prepare_id=897414&key=A5E13AC7-8055-47D9-912D-39099BADB731&prepare_id=2712249,2724955,2726780,2726270,2725840,2725040,2732319"
    code,datas=testGetUrlData(urladdr)
    datas=datas[17:-2]
    if code == ERROR:
        print "alio2o_resend:get url data ERROR"
        return
    for c in range(len(datas)):
        if (datas[c]== ',') and (datas[c-1]=='}'):
            datas=datas[:c]+'\n'+datas[c+1:] 
    datas_list=datas.split('\n')
    print "Processed Datas:\n"
    print datas_list
    for data in datas_list:
        print "Data 2 be delt:\n"
        print data
        #data = data[:-1]
        try:
            data_json=json.loads(data)
        except:
            print "ERROR when resolving json data\n"
        print data_json.get("process_status")
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
