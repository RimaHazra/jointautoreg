# -*- coding: utf-8 -*-
"""
Created on Wed May 15 01:28:13 2019

@author: Rimi
"""

import pandas as pd
import csv
import os
import sys
import numpy as np
import datetime

def closed_and_assigned_bugs():
    months = [10,4,10,6,10,4,10,4,10,4,10,4,10,4,10,4,10,4,10,4,10,4,10,4,10,4,10,4]
    years = [2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    releases = {"Ubuntu 4.10":"Warty","Ubuntu 5.04":"Hoary","Ubuntu 5.10":"Breezy","Ubuntu 6.06.2":"Dapper","Ubuntu 6.10":"Edgy","Ubuntu 7.04":"Feisty","Ubuntu 7.10": "Gutsy","Ubuntu 8.04.4 LTS":"Hardy","Ubuntu 8.10": "Intrepid","Ubuntu 9.04":"Jaunty","Ubuntu 9.10": "Karmic","Ubuntu 10.04.4 LTS":"Lucid","Ubuntu 10.10": "Maverick","Ubuntu 11.04": "Natty","Ubuntu 11.10": "Oneiric","Ubuntu 12.04.4 LTS":"Precise","Ubuntu 12.10":"Quantal","Ubuntu 13.04": "Raring","Ubuntu 13.10":"Saucy","Ubuntu 14.04.5 LTS":"Trusty","Ubuntu 14.10":"Utopic","Ubuntu 15.04": "Vivid","Ubuntu 15.10":"Wily","Ubuntu 16.04.5 LTS":"Xenial","Ubuntu 16.10": "Yakkety","Ubuntu 17.04":"Zesty","Ubuntu 17.10": "Artful","Ubuntu 18.04":"Bionic"}
    table = pd.DataFrame(columns = ["Bugs Id","Date Assigned","Date Closed","Create Date"])
    for i in range(len(years)-1):
        start = years[i]
        end = years[i+1]
        print(start,end)
        taskf = pd.read_csv(os.path.join("Bugs","All_bug_task_details_"+str(start)+"_"+str(end)+".csv"), usecols = ["Bug Id","date_assigned","date_closed","date_created"])
        #print(taskf["date_closed"])
        taskf = taskf.dropna()
        for index,row in taskf.iterrows():
            bug = row[0]
            assDate = str(row[1]).split(" ")[0]
            closedt = str(row[2]).split(" ")[0]
            createdate = str(row[3]).split(" ")[0]
            if closedt!="NaN" or len(closedt)!=0: 
                print(bug,assDate,closedt,createdate)
                #table=table.append({"Bug Id":bug,"Date Assigned":assDate,"Date Closed":closedt,"Create Date":createdate},ignore_index=True)
    #table.drop_duplicates(subset=('Bug Id'),keep="first",inplace=True)    
    #print(table)
    
    

closed_and_assigned_bugs()    