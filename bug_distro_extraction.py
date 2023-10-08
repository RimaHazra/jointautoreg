# -*- coding: utf-8 -*-
"""
Created on Sat May 11 23:30:10 2019

@author: Rimi
"""
import pandas as pd
import sys
import os
import csv
import re

def bug_distro_phase_one():
    year_start = 2006
    year_end = 2007
    releases = {"Ubuntu 4.10":"Warty","Ubuntu 5.04":"Hoary","Ubuntu 5.10":"Breezy","Ubuntu 6.06.2":"Dapper","Ubuntu 6.10":"Edgy","Ubuntu 7.04":"Feisty","Ubuntu 7.10": "Gutsy","Ubuntu 8.04":"Hardy","Ubuntu 8.10": "Intrepid","Ubuntu 9.04":"Jaunty","Ubuntu 9.10": "Karmic","Ubuntu 10.04":"Lucid","Ubuntu 10.10": "Maverick","Ubuntu 11.04": "Natty","Ubuntu 11.10": "Oneiric","Ubuntu 12.04":"Precise","Ubuntu 12.10":"Quantal","Ubuntu 13.04": "Raring","Ubuntu 13.10":"Saucy","Ubuntu 14.04":"Trusty","Ubuntu 14.10":"Utopic","Ubuntu 15.04": "Vivid","Ubuntu 15.10":"Wily","Ubuntu 16.04":"Xenial","Ubuntu 16.10": "Yakkety","Ubuntu 17.04":"Zesty","Ubuntu 17.10": "Artful","Ubuntu 18.04":"Bionic"}
    fWrite = open(os.path.join("Bugs","bugId_ubuntuVer_"+str(year_start)+"_"+str(year_end)+".csv"),"w",newline="",encoding="utf-8")
    fWriter = csv.writer(fWrite)
    #fWriter.writerow(["BugId","BugDesc","InstallationMedia","DistroRelease","ReleaseName"])
    fWriter.writerow(["BugId","InstallationMedia","DistroRelease"])
    
    f = pd.read_csv(os.path.join("Bugs","All_bug_idwise_description_"+str(year_start)+"_"+str(year_end)+".csv"))
    f.sort_values("Bug Id", inplace = True) 
    #f.drop_duplicates(subset =("Bug Id","Description"), keep = False, inplace = True) 
    print(f)
    c = 0
    d = 0
    for index,row in f.iterrows():
        #print(row)
        flag = False
        temp = []
        bugId = row[0]
        mediaUVer ="-"
        distroRel = "-"
        rel="-"
        try:
            des= str(row[1]).encode('cp1252')
        except:
            des=str(row[1]).encode("utf-8")
            #except:
            #    pass
        description = str(row[1]).split("\n")
        #print(description)
        for i in range(len(description)):
            if "InstallationMedia:" in description[i]:
                media = description[i]
                #print(media)
                media = media.split("InstallationMedia: ")[-1]
                media = re.findall('.+?"',media)
                
                try:
                    mediaUVer = (media[0]).replace('"', "")
                except:
                    pass
                #print(mediaUVer)
                mediaUVer=mediaUVer.lstrip()
                mediaUVer = mediaUVer.rstrip()
                #rel = releases[mediaUVer]
                
                   
            if "DistroRelease:" in description[i]:
                distroRel = description[i].split("DistroRelease:")[-1]
                
                distroRel = distroRel.lstrip()
                #rel=releases[distroRel]
        if((distroRel!="-" and mediaUVer!="-") or (distroRel!="-") or (mediaUVer!="-")):
            c=c+1
            flag = True
            
        #fWriter.writerow([bugId,des,mediaUVer,distroRel,rel])
        if flag ==True:
            fWriter.writerow([bugId,mediaUVer,distroRel])
            fWrite.flush()
    print(c)
    print("total entry:",d)
    fWrite.close()
                
                    
                   
                
    
if __name__ == "__main__":
    bug_distro_phase_one()