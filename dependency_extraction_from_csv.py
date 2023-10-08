# -*- coding: utf-8 -*-
"""
Created on Sun May  5 16:46:00 2019

@author: Rimi
"""
import pandas as pd
import csv
import numpy as np
import csv
import sys
import re

def csvdlist_to_dependencylist():
    f = open(r"ubuntu-version\Ubuntu 5.04 (Hoary)\ubuntu_hoary_package_dependency_List.csv","w",newline="")
    f_csv = csv.writer(f)
    packageDetail = pd.read_csv(r'ubuntu-version\Ubuntu 5.04 (Hoary)\ubuntu_hoary_packages.csv', header=None,names=("Package","Priority","Section","Maintainer" ,"Architecture","Version","Depends","Description","Bugs","Origin","Task"),dtype={"Package": np.unicode_,"Priority": np.unicode_,"Section": np.unicode_,"Maintainer" : np.unicode_,"Architecture": np.unicode_,"Version": np.unicode_,"Depends": np.unicode_,"Description": np.unicode_,"Bugs": np.unicode_,"Origin": np.unicode_,"Task": np.unicode_},encoding='ISO-8859-1')
    #print(packageDetail[["Package","Depends"]])
    for index, row in packageDetail.iterrows():
        packageName = str(row["Package"])
        print(packageName)
        dependencyList = str(row["Depends"]).split(",")
        #print(packageName,"---->",dependencyList)
        for ind in range(len(dependencyList)):
            depPackage =  dependencyList[ind]
            try:
                openningBIndex = [i for i, x in enumerate(depPackage) if x == '('][0]
                closingBIndex = [i for i, x in enumerate(depPackage) if x == ')'][0]
                depVersion = depPackage[openningBIndex:closingBIndex+1]
                depPName = depPackage[0:openningBIndex]
                #print(,"------>",depVersion)
                #sys.exit()
            except:
                depPName = depPackage
                depVersion = "-"
                #print("Not Try: ",packageName,"------>",depPackage)
            f_csv.writerow([packageName,depPName,depVersion])
            f.flush()
    f.close()
                
    #sys.exit()            


csvdlist_to_dependencylist()