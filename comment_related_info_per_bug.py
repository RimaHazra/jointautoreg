# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 20:22:04 2019

@author: Rimi
"""
import os, sys
import numpy as np
import pandas as pd
from collections import defaultdict
import csv
import nltk
from nltk.corpus import stopwords
import string
from datetime import datetime


def calculate_comment_related_information():
    colnames=['bugId', 'contribName', 'contribLink', 'username','name','date','text'] 
    f = open(os.path.join("BugComments","bug_comment_extracted_information.csv"),"w",newline="")
    ferror = open(os.path.join("BugComments","bug_comment_extracted_information_errorFile.txt"),"w")
    fread = csv.writer(f)
    fread.writerow(["Bug Id","Number of Comments","Active comment section (days)","Total length of comments","Average inter arrival time"])
    
    for j in range(1,100):#Re-run it once again
        #bug_comment_1
        filename = "bug_comment_"+str(j)+".csv"
        commentFile = pd.read_csv(os.path.join("BugComments\Comments",filename), names=colnames, usecols=["bugId","date","text"], header=None,encoding='ISO-8859-1')
        #print(commentFile)
        # bug count, number of comments, total text volume of the comments, unique number of users connected to each bug, 
        #duration of commenting (enddate of a comment - start date of the comment for a bug), 
        #average inter-arrival time between comments for the bug.
        #=======================Grouping it by bug id===============================
        grouped = commentFile.groupby("bugId")
        #==========Iterating each group ===========================================
        for name,group in grouped:
            try:
                noOfComments = group.shape[0]
                print("Bug ID: ",name)
                print("Number of Comments: ",noOfComments)
                #========== Calculating date of first comment ==================================
                firstCommentDate = list(group[:1]["date"])[0]
                firstCommentDate = datetime.strptime(firstCommentDate.split("+")[0], '%Y-%m-%d')
                #========== Calculating date of last comment ==================================
                lastCommentDate = list(group[-1:]["date"])[0]
                lastCommentDate = datetime.strptime(lastCommentDate.split("+")[0], '%Y-%m-%d')
                #=================Number of days comment section was active ==========================
                duration = lastCommentDate - firstCommentDate
                daysReq = duration.days
                print("Active comment section (days): ",daysReq)
                #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                #Average inter-arrival time of comments--- variable initialization====================
                intrArrvTime = []
                avgIntrArrvTime = 0
                #============Calculating overall comment length for each bug=====================
                commentLen = 0
                commentFiltered = []
                for i,row in group.iterrows():
                    #=======================text processing ================================================
                    commentText = row[2]
                    stop = set(stopwords.words('english'))
                    commentText = nltk.word_tokenize(commentText)
                    #commentFiltered = []
                    temp = [t for t in commentText if t not in stop and t not in string.punctuation and t.isdigit()==False]
                    commentFiltered.extend(temp) 
                    #=================computation of comment length complete =============================== 
                    #=================Computation of inter arrival time ====================================
                    commentTime = row[1]
                    commentTime = datetime.strptime(commentTime.split("+")[0], '%Y-%m-%d')
                    intrArrvTime.append(commentTime)
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                commentFiltered = len(set(commentFiltered)) 
                print("Total length of comments (unique words): ",commentFiltered)  
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                #==================Computation of interarrival time gap======================================
                for k in range(len(intrArrvTime)-1):
                    t1 = intrArrvTime[k]
                    t2 = intrArrvTime[k+1]
                    diff = t2-t1
                    diff = diff.days
                    avgIntrArrvTime+=diff
                avgIntrArrvTime = float(avgIntrArrvTime/len(intrArrvTime))
                print("Average inter arrival time of comments: ",avgIntrArrvTime)
                #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                #=======================Writing in a CSV file=================================================
                fread.writerow([name,noOfComments,daysReq,commentFiltered,avgIntrArrvTime])
                f.flush()
                #sys.exit()
            except:
                ferror.write(str(name)+"\n")
                pass
    f.close()
                
            
            
            
calculate_comment_related_information()