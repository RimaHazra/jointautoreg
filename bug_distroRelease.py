# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 23:34:16 2019

@author: Rimi
"""
import json
import ijson
import os,sys
import pandas as pd
import subprocess

path1="E:\1MyWork\SoftwareDependencyProject\Bugs"
path="Bugs"
filename = "All_bug_task_details_2014_2016.json"

#with open(os.path.join(path,filename)) as f:
#    data = json.load(f)

#pprint(data)



with open(os.path.join(path,filename)) as f:
    p = subprocess.Popen(['jq', '-c', '.'], stdin=f, stdout=subprocess.PIPE,shell=True)
    print(p.stdout)
    for line in p.stdout:
        print(line)
        content = json.loads(line)
        print(content)
    print("efg")
print("abc")