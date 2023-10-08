# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:05:54 2019

@author: Rimi
Task: Check bug closing date based on status. Two Task: Divide the status into two part. resolved and cant resolved
1) Check first occurance and last occurance and its corresponding status
"""
import pandas as pd
import numpy as np
import os
import sys
from collections import defaultdict
import json
import csv


def reading_required_files():
    years = [2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    statusT = open("status_transition_details_wo_same_cdate.csv","w",newline="")
    statusTCSV = csv.writer(statusT)
    statusTCSV.writerow(["Bug Id","Initial status","Initial status date","Last status","Last status date"])
    #years=[2004,2005,2006]
    names = ["warty","hoary","breezy","dapper","edgy","feisty","gutsy","hardy","intrepid","jaunty","karmic","Lucid","maverick","natty","oneiric","precise","quantal","raring","saucy","trusty","utopic","vivid","wily","xenial","yakkety","zesty"]
    overallTaskF = pd.DataFrame()
    overallTaskL = pd.DataFrame()
    for i in range(len(years)-1):        
        start = years[i]
        end = years[i+1]
        task = pd.read_csv(os.path.join("Bugs","All_bug_task_details_"+str(start)+"_"+str(end)+".csv"),usecols = ["Bug Id","date_created","status"])
        overallTaskF = pd.concat([overallTaskF,task])
        overallTaskL = pd.concat([overallTaskL,task])
        
    overallTaskF.drop_duplicates(subset=("Bug Id"),keep = "first",inplace =True)
    overallTaskL.drop_duplicates(subset=("Bug Id"),keep = "last",inplace =True)
    statFlowPos = 0
    statFlowNeg = 0
    statFlowSame = 0
    status = ["New","Incomplete","Opinion","Invalid","Won't Fix","Expired","Confirmed","Triaged","In Progress","Fix Committed","Fix Released","Unknown"]
    temp ={new_list: [] for new_list in status}
    statComb = {new_list: temp for new_list in status} 
    #print(statComb)
    for index,row in overallTaskF.iterrows():
        bug = row[0]
        start_cdate = row[1]
        start_status = row[2]
        anoRow = overallTaskL.loc[overallTaskL["Bug Id"]==bug]
        end_status = list(anoRow["status"])[0]
        end_cdate = list(anoRow["date_created"])[0]
        if ((start_status!=end_status) and (start_cdate!=end_cdate)):
            #print(start_status,end_status)
            statComb[start_status][end_status].append(bug)
            statusTCSV.writerow([bug,start_status,start_cdate,end_status,end_cdate])
            statusT.flush()
        #print(start_status,end_status)
        #Resolved bugs====================================
        if ((start_status!=end_status) and ((end_status=="Fix Committed") or (end_status=="Won't Fix") or (end_status=="Fix Released")) and (start_cdate!=end_cdate)):
            statFlowPos+=1
            #statComb[start_status][end_status].append(bug)
            #print(bug)
            #print(start_status,end_status)
            #print(start_cdate,end_cdate)
        else:
            statFlowSame+=1
            #statComb[start_status][end_status].append(bug)
        #else:
        #    statFlowNeg+=1
            #statComb[start_status][end_status].append(bug)
    print(statFlowPos,statFlowSame)
    
    '''statWiseCount = {new_list:{} for new_list in status} 
    
    for key in statComb.keys():
        for j in (statComb[key]).keys():
            count = len(set(statComb[key][j]))
            statWiseCount[key][j]=count
    
    with open("status_transition_count.json", "w") as write_file:
        json.dump(statWiseCount, write_file,indent=4)
    #print(statComb)
            
        
        
        
    groupedBugs = overallTask.groupby(by="Bug Id")
    groupBugDict = groupedBugs.groups
    print(groupBugDict.keys())
    #sys.exit()
    for key in groupBugDict.keys():
        out = overallTask.loc[overallTask["Bug Id"]==key,["Bug Id","date_created","status"]]
        print(out)
        #sys.exit()'''
        
        
    
#def total_bugs_with_status():
    
reading_required_files()