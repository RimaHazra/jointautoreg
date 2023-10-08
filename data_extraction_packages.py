# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:36:27 2019

@author: Rimi
"""
import sys,os
import csv
from bs4 import BeautifulSoup

def data_extraction(filename,common_path,path):
    fWr = open(os.path.join(common_path,"ubuntu_hoary_packages.csv"),"a",newline="",encoding='ISO-8859-1')
    csvFile = csv.writer(fWr)
    packageDict = dict()
    f = open(os.path.join(path,filename),"r",encoding="ISO-8859-1")
    placeholder = f.readlines()
    #print(placeholder)
    placeholder=placeholder[:-2]
    indices = indices = [i for i, x in enumerate(placeholder) if x == '\n']
    #print(indices)
    indices = [-1]+indices+[len(placeholder)]
    #print(indices)
    print(len(indices))
    low=0
    entityDict={}
    c = 0
    for i in range(len(indices)-2):
        entity=[]
        entityDict[c]={'Package':[],'Priority':[],'Section':[],'Maintainer':[] ,'Architecture':[],'Version':[],'Depends':[],'Description':[],'Bugs':[],'Origin':[],'Task':[]}
        low = indices[i]+1
        up = indices[i+1]
        #print("Low:: ",low,"Upper:: ",up)
        entity = placeholder[low:up]
        print(entity)
        desIndex = [i for i, x in enumerate(entity) if x.startswith('Description:')][0]
        #print(desIndex)
        bugIndex = [i for i, x in enumerate(entity) if x.startswith('Bugs:')][0]
        #print("Description Index",desIndex,"Bug Index",bugIndex)
        des_string = "".join(entity[desIndex:(bugIndex)])
        #print(des_string)
        for j in range(0,desIndex):
            #print(j)
            entry = entity[j]
            if entry.startswith('Package: ') or entry.startswith('Priority:') or entry.startswith('Section: ') or entry.startswith('Maintainer: ') or entry.startswith('Architecture: ') or entry.startswith('Version: ') or entry.startswith('Depends:'):
                entry = entry.rstrip().split(":")
                #print(entry)
                tag = entry[0]
                data = entry[1:]
                #print(tag,data)
                entityDict[c][tag]=data
        desTag = des_string.split(":")
        #print(desTag[0])
        #sys.exit()
        entityDict[c][desTag[0]]=desTag[1:]
        bugTag= entity[bugIndex].rstrip().split(":")[0]
        entry = entity[bugIndex].rstrip().split(":")
        entityDict[c][bugTag]=[":".join(entry[1:])]
        #print(":".join(entry[1:]))
        #sys.exit()
        for j in range(bugIndex+1,len(entity)):
            #print(up)
            #print(j)
            entry = entity[j]
            if entry.startswith('Origin:') or entry.startswith('Task:'):
                entry = entry.rstrip().split(":")
                #print(entry)
                tag = entry[0]
                data = entry[1:]
                entityDict[c][tag]=data
        c=c+1
    #Writing Files   
    #csvFile.writerow(["Package","Priority","Section","Maintainer" ,"Architecture","Version","Depends","Description","Bugs","Origin","Task"])
    for key in entityDict.keys():
        temp=[]
        #temp =[key]
        entryDict = entityDict[key]
        for tag in entryDict.keys():
            if(len(entryDict[tag])!=0):
                d = " ".join(entryDict[tag])
            if(len(entryDict[tag])==0):
                d = "None"
            temp.append(d)
        #sys.exit()
        csvFile.writerow(temp[0:])
        fWr.flush()
    fWr.close()
    #sys.exit()
common_path =r"ubuntu-version\Ubuntu 5.04 (Hoary)"        
path1 = r"ubuntu-version\Ubuntu 5.04 (Hoary)\main"
path2=r"ubuntu-version\Ubuntu 5.04 (Hoary)\multiverse"
path3=r"ubuntu-version\Ubuntu 5.04 (Hoary)\restricted"
path4=r"ubuntu-version\Ubuntu 5.04 (Hoary)\universe"

filename = "Packages_2"
data_extraction(filename,common_path,path3)
    