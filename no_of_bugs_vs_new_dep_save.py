# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 01:07:44 2019

@author: Rimi
"""

'''#=====================================Work with in degree=====================================
        inDegList = []
        bugCountList = []
        pnameIndeg = read_indegree(names[i])
        for pname in pnameIndeg.keys():
            
            try:
                
                indeg = int(pnameIndeg[pname])
                if indeg<100: 
                    bugC = int(packageBugCount[pname])
                    inDegList.append(indeg)
                    bugCountList.append(bugC)
            except:
                #bugC = 0
                pass
            
            continue
        #print(max(inDegList))
        print(len(inDegList),len(bugCountList))
        dataIn = sorted(zip(inDegList,bugCountList))
        plt.scatter(*zip(*dataIn))#,*zip(*ALL))
        #======================================Work with out degree=====================================
        outDegList = []
        bugCountList = []
        pnameOutdeg = read_outdegree(names[i])
        for pname in pnameOutdeg.keys():
            
            try:
                outdeg = int(pnameOutdeg[pname])
                bugC = int(packageBugCount[pname])
                outDegList.append(outdeg)
                bugCountList.append(bugC)
            except:
                #bugC = 0
                pass  
            continue
        print(max(outDegList))
        print(len(outDegList),len(bugCountList))
        dataOut = sorted(zip(outDegList,bugCountList))
        plt.scatter(*zip(*dataOut))#,*zip(*ALL))
        
    plt.xlabel("In Degree")
    plt.ylabel("Number of Bugs")
    plt.legend(names,prop=fontP)#,"overall"))
    plt.title("In Degree vs Bug Count")
    plt.savefig('indegree_vs_bugcount_lessthan_100.png')
    plt.show()'''
