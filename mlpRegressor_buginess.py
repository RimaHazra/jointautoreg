# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 23:35:34 2019

@author: Rimi
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:33:43 2019

@author: Rimi
"""
import scipy as sp
from matplotlib import pyplot as plt
import os,sys
import csv
from collections import defaultdict
import numpy as np
import json
import math
import pandas as pd
from collections import Counter 
from collections import defaultdict
import networkx as nx
from scipy.stats import norm
import seaborn as sns
import random
import scipy.sparse
import itertools
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor



def graph_creation_from_edgelist(filename):
    df = pd.read_csv(filename,header=None,names=('s','d'),dtype={'s':np.int64,'d':np.int64},encoding='ISO-8859-1')
    #print(df)
    outNodes = defaultdict(list)
    Graphtype = nx.DiGraph()
    G = nx.from_pandas_edgelist(df,'s','d',create_using=Graphtype)
    #G=nx.read_edgelist(os.path.join(filename), nodetype=int) 
    #k = 0
    for node in sorted(G.nodes()):
        #print(node)
        outNodes[node]=[]
        neiNodesList = list(G.neighbors(node))
        #print(len(neiNodesList))
        #k=k+1
        for neiNode in neiNodesList:
            #print(neiNode)
            outNodes[node].append(neiNode)
        #if k ==10:
        #    print(outNodes)
        #    sys.exit()
            
        #sys.exit()
    return outNodes 

def sparse_matrix_creation(outLinkDict,noOfPackages):
    N = noOfPackages
    x = sp.sparse.lil_matrix( (N,N) )
    print(N)
    for i in range(N):
        indexI = i
        #print(i)
        for j in range(len(outLinkDict[i])):
            indexJ = outLinkDict[i][j]
            #print(indexJ)
            x[indexI,indexJ]=1
    #print(x)
    return x

def bug_to_package_name_map(bugFile, pNameFile):
    global packageIdList
    packageIdList = {}
    packageList ={}
    totPackages = 0 
    packages = csv.reader(open(os.path.join("ubuntu-version",pNameFile),"r"))
    for row in packages:
        packageList[row[0]]=int(row[1])
        packageIdList[int(row[1])] = row[0]
        totPackages+=1
    #----------------------------------------------------------------------------
    bugs = csv.reader(open(os.path.join("Bugs\PackageNameBugMap",bugFile),"r"))
    next(bugs, None)
    packageWiseBugs = defaultdict(list)
    for row in bugs:
        pname = row[0]
        bugId = row[2]
        pid = packageList[pname]
        packageWiseBugs[pid].append(bugId)
    
    pIdBugCount = {}    
    for key in packageWiseBugs.keys():
        bugC = len(set(packageWiseBugs[key]))
        pIdBugCount[key]=bugC     
    #print(pIdBugCount)
    return pIdBugCount,totPackages


def bugginess_main_function():
    #names = ["warty","hoary","breezy","dapper","edgy","feisty","gutsy","hardy","intrepid","jaunty","karmic","Lucid","maverick","natty","oneiric","precise","quantal","raring","saucy","trusty","utopic","vivid","wily","xenial","yakkety","zesty"]
    names=["trusty"]
    distroName = "Trusty"
    for i in range(len(names)):
        uName = names[i]
        filename="ubuntu_"+uName+"_package_dependency_EdgeList.csv"
        outLinkNodes = graph_creation_from_edgelist(os.path.join("ubuntu-version",filename))
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        bugFileName = "Packages_"+distroName+"_map_with_bugId_prefix.csv"
        pIdNameFile = "ubuntu_"+uName+"_packagesName_Id_Map.csv"
        pIdWithBugs,noOfPackages = bug_to_package_name_map(bugFileName,pIdNameFile)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        X = sparse_matrix_creation(outLinkNodes,noOfPackages)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        keys = np.arange(0,noOfPackages,1)
        data = {key: 0 for key in keys}
        #print(data)
        
        initCoefs = [0.000001 for key in keys]
        initCoefs = np.array(initCoefs,)
        for p in pIdWithBugs.keys():
            try:
                bugC = pIdWithBugs[p]
                data[p]=bugC
            except:
                pass
        #print(data)
        
        Y = np.array(list(data.values()),)
        #print(Y.shape)
        X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y,test_size = 0.25,random_state = 3)#shuffle=True)
        lm = MLPRegressor(hidden_layer_sizes=(1, ), activation='logistic', verbose =True,warm_start=True,early_stopping=True,solver='adam', alpha=0.09, batch_size='auto', learning_rate='invscaling', learning_rate_init=0.0000001, power_t=0.5, shuffle=True, tol=0.00001)
        parameters={'alpha':[0.01]}
        #clf = GridSearchCV(lm, parameters, cv=5)
        lm.fit(X_train,Y_train)#,coef_init = initCoefs)
        
        MSE_train = np.mean((Y_train - lm.predict(X_train)) ** 2)
        MSE_test = np.mean((Y_test - lm.predict(X_test)) ** 2)
        
        #cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
        #cv_results = cross_validate(lm, X,  Y, cv=5)
        #print(clf.cv_results_)
        res = lm.coefs_
        print(np.min(res),np.max(res))
        print("Intercept: ",lm.intercepts_)
        print("Number of iteration solver has run: ",lm.n_iter_)
        print("Loss ",lm.loss_)
        #print(lm.loss_curve_)
        print("Fit a model X_train, and calculate MSE with Y_train: ",MSE_train)
        print("Fit a model X_train, and calculate MSE with X_test, Y_test:",MSE_test)
        print('R sq: ',lm.score(X_test,Y_test))
        #print("Coefficients: ",clf.coef_)
        
        
bugginess_main_function()
        
