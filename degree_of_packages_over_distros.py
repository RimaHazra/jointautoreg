# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 00:32:22 2019

@author: Rimi
"""
import pandas as pd
import csv
import networkx as nx
import os
import sys
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt


def get_package_id_name_map(distroName):
    pIDNameDict = {}
    pnameIDMapFile = csv.reader(open(os.path.join("ubuntu-version","ubuntu_"+distroName+"_packagesName_Id_Map.csv"),"r"))
    for line in pnameIDMapFile:
        pname = (line[0]).strip()
        pid = int(line[1])
        pIDNameDict[pid]=pname
    return pIDNameDict
    
def union_of_packages():
    print("Process: Union of Packages:: Started")
    packages_union_set = []
    names = ["warty","hoary","breezy","dapper","edgy","feisty","gutsy","hardy","intrepid","jaunty","karmic","Lucid","maverick","natty","oneiric","precise","quantal","raring","saucy","trusty","utopic","vivid","wily","xenial","yakkety","zesty"]
    for i in range(len(names)):
        uName = names[i]
        print(uName)
        pIDNameDict = get_package_id_name_map(uName)
        packages_union_set.extend(pIDNameDict.values())
    packages_union_set = set(packages_union_set)
    print("Overall Packages: ",len(packages_union_set))
    print("Process: Union of Packages :: End")
    return packages_union_set

def packages_degree_storage_creation(overall_packages):
    cols = ["warty","hoary","breezy","dapper","edgy","feisty","gutsy","hardy","intrepid","jaunty","karmic","Lucid","maverick","natty","oneiric","precise","quantal","raring","saucy","trusty","utopic","vivid","wily","xenial","yakkety","zesty"]
    packageCores = {}
    overall_packages = list(overall_packages)
    for j in range(len(overall_packages)):
        package = overall_packages[j]
        packageCores[package]={}
        for k in range(len(cols)):
            distro = cols[k]
            packageCores[package][distro]=-1
    return packageCores
    
def read_degrees(distro,packageDict):
    propFile = "ubuntu_"+distro+"_In_degree_count"
    indegWithId = pd.read_csv(os.path.join("Graph_Properties",propFile+".csv"))
    #inDegProp = {}
    pnameIndeg = {}
    for index,row in indegWithId.iterrows():
        pid = int(row[0])
        indeg = int(row[1])
        #Preparing package name and its corresponding in-degree
        pname = packageDict[pid]
        pnameIndeg[pname] = indeg
        
    propFile = "ubuntu_"+distro+"_Out_degree_count"
    outdegWithId = pd.read_csv(os.path.join("Graph_Properties",propFile+".csv"))
    pnameOutdeg = {}
    for index,row in outdegWithId.iterrows():
        pid = int(row[0])
        outdeg = int(row[1])
        #Preparing package name and its corresponding out-degree
        pname = packageDict[pid]
        pnameOutdeg[pname] = outdeg
           
    return pnameIndeg,pnameOutdeg

    
if __name__ == "__main__":
    names = ["warty","hoary","breezy","dapper","edgy","feisty","gutsy","hardy","intrepid","jaunty","karmic","Lucid","maverick","natty","oneiric","precise","quantal","raring","saucy","trusty","utopic","vivid","wily","xenial","yakkety","zesty"]
    overall_packages = union_of_packages()
    packageInDegree = packages_degree_storage_creation(overall_packages)
    packageOutDegree = packages_degree_storage_creation(overall_packages)
    
    for i in range(len(names)):
        uName = names[i]
        print("Started: ",uName)
        pIDNameDict = get_package_id_name_map(uName)
        packageInDegreeLabel,packageOutDegreeLabel = read_degrees(uName,pIDNameDict)
        for package in packageInDegreeLabel.keys():
            
            inDegLabel = packageInDegreeLabel[package]
            outDegLabel = packageOutDegreeLabel[package]
            packageInDegree[package][uName]=inDegLabel
            packageOutDegree[package][uName]=outDegLabel
        
        print("End of Computation For: ",uName)
    print("Storing")
    df = pd.DataFrame.from_dict(packageInDegree,orient='index')
    df.to_csv('indegree_transition_6_labels.csv', index=True)
    
    df2 = pd.DataFrame.from_dict(packageOutDegree,orient='index')
    df2.to_csv('outdegree_transition_6_labels.csv', index=True)
        
    
    
        
            
            
        
    
        
                

