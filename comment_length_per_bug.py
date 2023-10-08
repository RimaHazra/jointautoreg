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


def calculate_comment_length():
    colnames=['bugId', 'contribName', 'contribLink', 'username','name','date','text'] 
    for j in range(100):
        filename = "bug_comment_"+str(j)+".csv"
        commentFile = pd.read_csv(os.path.join("BugComments\Comments",filename), names=colnames, usecols=["bugId","text"], header=None,encoding='ISO-8859-1')
        #print(commentFile)
        # bug count, number of comments, total text volume of the comments, unique number of users connected to each bug, 
        #duration of commenting (enddate of a comment - start date of the comment for a bug), 
        #average inter-arrival time between comments for the bug.
        grouped = commentFile.groupby("bugId")
        for name,group in grouped:
            print(name)
            print(group)
            #size = group.shape[0]
            commentLen = 0
            commentFiltered = []
            for i,row in group.iterrows():
                commentText = row[1]
                stop = set(stopwords.words('english'))
                commentText = nltk.word_tokenize(commentText)
                #commentFiltered = []
                temp = [t for t in commentText if t not in stop and t not in string.punctuation and t.isdigit()==False]
                commentFiltered.extend(temp) 
            commentFiltered = len(set(commentFiltered)) 
            print(commentFiltered)     
            sys.exit()
            
calculate_comment_length()