# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 07:02:08 2019

@author: Rimi
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 18:58:59 2019

@author: Rimi
"""
from matplotlib import pyplot as plt
import os,sys,csv,json,math
from collections import defaultdict
import numpy as np
import pandas as pd
from collections import Counter 
from collections import defaultdict
#import networkx as nx
from scipy.stats import norm
from itertools import combinations
#from sklearn import cross_validation
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn import model_selection
from sklearn.metrics import mean_squared_error
from scipy import stats as st 
from sklearn import linear_model
from sklearn.linear_model import Ridge,RidgeCV
from sklearn.model_selection import GridSearchCV



def bug_to_package_name_map(bugFile, pNameFile):
    global packageIdList
    packageIdList = {}
    packageList ={}
    packages = csv.reader(open(os.path.join("ubuntu-version",pNameFile),"r"))
    for row in packages:
        packageList[row[0]]=int(row[1])
        packageIdList[int(row[1])] = row[0]
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
    return pIdBugCount

def read_indeg_outdeg(pInDeg, pOutDeg):
    pIdInDeg = {}
    pIdOutDeg = {}
    fIn = csv.reader(open(os.path.join("Graph_Properties",pInDeg),"r"))
    fOut = csv.reader(open(os.path.join("Graph_Properties",pOutDeg),"r"))
    for row in fIn:
        pIdInDeg[int(row[0])]=int(row[1])    
    for row in fOut:
        pIdOutDeg[int(row[0])] = int(row[1])
    return pIdInDeg,pIdOutDeg

def regularized_linear_reg_bugginess():
    distroName = "Trusty"
    bugFileName = "Packages_"+distroName+"_map_with_bugId_prefix.csv"
    pIdNameFile = "ubuntu_"+distroName.lower()+"_packagesName_Id_Map.csv"
    pInDeg = "ubuntu_"+distroName.lower()+"_In_degree_count.csv"
    pOutDeg = "ubuntu_"+distroName.lower()+"_Out_degree_count.csv"
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    pIdWithBugs = bug_to_package_name_map(bugFileName,pIdNameFile)
    pIdInDeg,pIdOutDeg = read_indeg_outdeg(pInDeg,pOutDeg)
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #+++++++++++++++++++++Here we use outdegree only+++++++++++++++++++++++++++
    data = {"PName":[],"OutDegree":[],"BugCount":[]}
    
    for p in pIdOutDeg.keys():
        outDeg = pIdOutDeg[p]
        data["PName"].append(p)
        data["OutDegree"].append(outDeg)
        try:
            bugC = pIdWithBugs[p]
            data["BugCount"].append(bugC)
        except:
            data["BugCount"].append(0)
            pass
    #print(data)
    #+++++++++++++creating dataframe++++++++++++++++
    df = pd.DataFrame(data) 
    #print(df)
    X = df.drop(['PName','BugCount'],axis=1)
    #++++++++++++++++Train, Test and Cross Validate+++++++++++++++++++++
    
    X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, df.BugCount,test_size = 0.25,random_state = 3)#shuffle=True)
    lm = RidgeCV(alphas=(0.1, 1.0, 10.0),cv=5)
    
    #parameters = {'alpha':np.arange(0,1,0.01)}
    #lm = linear_model.Lasso(fit_intercept = True,tol= 0.00001)
    #lm = GridSearchCV(l, parameters, cv=5)
    #print(X_train.shape,X_test.shape, Y_train.shape, Y_test.shape)
    lm.fit(X_train,Y_train)
    
    pred_train = lm.predict(X_train)
    pred_test = lm.predict(X_test)
    
    MSE_train = np.mean((Y_train - lm.predict(X_train)) ** 2)
    MSE_test = np.mean((Y_test - lm.predict(X_test)) ** 2)
    
    print("Alpha:",lm.alpha_)
    print("Fit a model X_train, and calculate MSE with Y_train: ",MSE_train)
    print("Fit a model X_train, and calculate MSE with X_test, Y_test:",MSE_test)
    print("Coefficients: ",lm.coef_)#for slope
    print("Intercept Coefficient",lm.intercept_)
    # Have a look at R sq to give an idea of the fit 
    #print(sorted(lm.get_params(deep=True)))
    print('R sq: ',lm.score(X_test,Y_test))
    # and so the correlation is..
    print('Correlation: ', math.sqrt(lm.score(X_train,Y_train)))
    print ("Standard Error: ",st.sem(X_train))
    
regularized_linear_reg_bugginess()
