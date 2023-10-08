# -*- coding: utf-8 -*-
"""
Created on Sat May 11 11:53:56 2019

@author: Rimi
"""

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


def line_plot(feature_val_x, feature_val_y,fname,objects):
    fig_size = plt.rcParams["figure.figsize"]
    # Prints: [8.0, 6.0]
    print("Current size:", fig_size)
    # Set figure width to 12 and height to 9
    fig_size[0] = 9
    fig_size[1] = 4
    plt.rcParams["figure.figsize"] = fig_size
    #styles = ["ro","r--","k","g+","p-","r-","b-"] 
    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 5)])
    #call_plot_func(feature_val_x,feature_val_y,"average degree")
    for i in range(len(feature_val_x)):
        #s = random.choice(styles)
        sing_f_x = feature_val_x[i]
        print(sing_f_x)
        sing_f_y = feature_val_y[i]
        print(sing_f_y)
        call_plot_func(sing_f_x,sing_f_y,names[i])
        plt.xlabel('Degree k')
        plt.ylabel("Average Degree value")
        plt.legend()
        plt.tight_layout()
        plt.savefig(fname+'_'+names[i]+'_.png')
        plt.show()
    #plt.plot(feature_val_x,feature_value_y,"ro")
    
    
def call_plot_func(f_x,f_y,l):
    plt.scatter(f_x,f_y,marker = "o",label = l)
    #plt.show()
    #sys.exit()


def pdf_plot():
    
    tname = "Ubuntu 4.10 (Warty)"
    pname = "warty"
    #f = pd.read_csv(os.path.join("Graph_Properties","ubuntu_trusty_packages_indeg_outdeg.csv"))
    f1 = pd.read_csv(os.path.join("Graph_Properties","ubuntu_"+pname+"_In_degree_count.csv"),header=None,names=("package","InDegree"),dtype={"package":np.int64,"InDegree":np.int64},encoding='ISO-8859-1')
    f2 = f = pd.read_csv(os.path.join("Graph_Properties","ubuntu_"+pname+"_Out_degree_count.csv"),header=None,names=("package","OutDegree"),dtype={"package":np.int64,"OutDegree":np.int64},encoding='ISO-8859-1')
    
    f = pd.merge(f1, f2, on='package')
    #print(f)
    print(f.groupby('OutDegree').size())
    sys.exit()
    
    flist = list(f["InDegree"])
    foutlist = list(f["OutDegree"])
    flist = list(filter(lambda a: a != 0, flist))
    foutlist = list(filter(lambda a: a != 0, foutlist))
    #flist = np.log10(flist)
    #foutlist = np.log10(foutlist)
    sns.distplot(flist,hist=False, kde=True,bins=20, color = 'blue', hist_kws={'edgecolor':'black'},kde_kws={'shade': False,'linewidth': 1},label="In Degree")
    sns.distplot(foutlist,hist=False, kde=True,bins=20, color = 'red', hist_kws={'edgecolor':'black'},kde_kws={'shade': False,'linewidth': 1},label= "out Degree")
    plt.legend(loc = 1)
    plt.xlabel("Log of Degree")
    plt.ylabel("PDF")
    plt.title(tname)
    plt.tight_layout()
    plt.savefig((pname+"_PDF.png"))
    plt.show()


#pdf_plot()


def graph_creation_from_edgelist(filename):
    df = pd.read_csv(filename,header=None,names=('s','d'),dtype={'s':np.int64,'d':np.int64},encoding='ISO-8859-1')
    #print(df)
    Graphtype = nx.DiGraph()
    G = nx.from_pandas_edgelist(df,'s','d',create_using=Graphtype)
    #G=nx.read_edgelist(os.path.join(filename), nodetype=int) 
    return G    

def cycle_of_the_network(filename,G):
    #=======================================================================
    #G = nx.DiGraph([(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)])
    G = (sorted(nx.weakly_connected_component_subgraphs(G),key =(len),reverse=True))[0]
    sizeOfComp = len(G.nodes()) 
    print(sizeOfComp)
    print(list(nx.simple_cycles(G)))
    #cycles = len(list(nx.simple_cycles(G)))
    #print(filename,"-- cycles : ",cycles)
    #listOfCycles.append(cycles)
    #print(listOfCycles)
    #print("Depth is ",depth)
    
def calculate_reciprocity(filename,G):
    #=======================================================================
    recipro = nx.reciprocity(G) 
    print("Reciprocity",recipro)
    listOfRecipro.append(recipro)
    
def calculate_diameter(filename,G):
    G = (sorted(nx.weakly_connected_component_subgraphs(G),key =(len),reverse=True))[0]
    G.remove_edges_from(nx.selfloop_edges(G))
    sizeOfComp = len(G.nodes()) 
    print(sizeOfComp)
    diameter = nx.diameter(G)
    print(filename,"--diameter : ",diameter)
    listOfDia.append(diameter)

def average_shortest_path_length (filename,G):
    #can only computed for connected network..so taking largest component
     G = (sorted(nx.weakly_connected_component_subgraphs(G),key =(len),reverse=True))[0]
     G.remove_edges_from(nx.selfloop_edges(G))
     sizeOfComp = len(G.nodes()) 
     print(sizeOfComp)
     avgSh = nx.average_shortest_path_length(G)
     print(filename,"--average shortest path length : ",avgSh)
     listOfAvgSh.append(avgSh)
    
def largest_component_fraction(filename,G):
    n = len(G.nodes())
    G = (sorted(nx.weakly_connected_component_subgraphs(G),key =(len),reverse=True))[0]
    fracSize = float(len(G.nodes()))/float(n)
    print("Filename: ",filename,"  Fraction: ",fracSize)
    listOfFracCC.append(fracSize)

def calculate_average_degree(filename,uName,G):
    temp_deg = []
    temp_val = []
    avgDeg = nx.average_degree_connectivity(G, source='in+out', target='in+out')
    for key in sorted(avgDeg.keys()):
        val = avgDeg[key]
        temp_deg.append(float(key))
        temp_val.append(float(val))
    #print(temp_val)
    listOfListAvgDeg.append(temp_deg)
    listOfListAvgDegVal.append(temp_val)
    #print(avgDeg.keys(),avgDeg.values())
    
    #sys.exit()
    #listOfAvgDeg.append(avgDeg)
    
    
    
    

def basic_network_measure(filename,G):
    #===============================Whether it is connected=======================================
    print(uName,"\n")
    conCheck = nx.is_weakly_connected(G)
    print(conCheck)
    #==========================Number of Nodes============================================
    '''print("total nodes:",len(G.nodes()))
    n = len(G.nodes())
    listOfNodes.append(n)
    #============================Density of the network==========================================
    dens = nx.density(G)#Computing density of the whole network
    print("Density of whole network: ",dens)
    listOfOverAllDens.append(dens)
    #===============================Number of Edges========================================
    e = len(G.edges())
    print("No of Edges: ",e)
    listOfEdges.append(e)'''
    
    #===============================Number of connected components=========================================
    count=0
    if conCheck==True:
        listOfNoComp.append(1)
    if conCheck == False:
        noOfComp = nx.number_weakly_connected_components(G)#
        print("Number of Connected Components: ",noOfComp)
        listOfNoComp.append(noOfComp)
    #============================================================================================
    lOfN = []
    lOfE = []    
    for G in (sorted(nx.weakly_connected_component_subgraphs(G),key =(len),reverse=True)):
        e = len(G.edges())
        n = len(G.nodes())
        lOfN.append(n)
        lOfE.append(e)
        #sizeOfComp = len(G.nodes())         
        #print("size of component",sizeOfComp)
        #print("Density of each component: ",nx.density(G))
        #listOfD.append(nx.density(G))
        #listOfSize.append(sizeOfComp)
    listOfListNodes.append(lOfN)
    listOfListEdges.append(lOfE)

                
def bar_plots(feature_val,fname,objects):
    fig_size = plt.rcParams["figure.figsize"]
    # Prints: [8.0, 6.0]
    print("Current size:", fig_size)
    # Set figure width to 12 and height to 9
    fig_size[0] = 9
    fig_size[1] = 4
    plt.rcParams["figure.figsize"] = fig_size
    bar_width = 0.4
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, feature_val,bar_width, alpha=0.8,color='red',hatch="o")
    plt.xticks(y_pos, objects,rotation=68)
    plt.ylabel(fname+"_Value")
    plt.xlabel('Ubuntu versions')
    plt.tight_layout()
    plt.savefig(fname+'.png')
    #plt.title('Programming language usage')
    plt.show()
    


if __name__ == "__main__":
    #names = ["warty","hoary","breezy","dapper","edgy","feisty","gutsy","hardy","intrepid","jaunty","karmic","Lucid","maverick","natty","oneiric","precise","quantal","raring","saucy","trusty","utopic","vivid","wily","xenial","yakkety","zesty"]
    names=["trusty"]
    listOfD = []
    listOfSize = []
    listOfNoComp =[]
    listOfOverAllDens=[]
    listOfNodes =[]
    listOfEdges = []
    listOfRecipro = []
    listOfCycles =[]
    listOfDia =[]
    listOfAvgSh =[]
    listOfFracCC=[]
    listOfListNodes =[]
    listOfListEdges =[]
    listOfListAvgDeg = []
    listOfListAvgDegVal = []
    for i in range(len(names)):
        uName = names[i]
        filename="ubuntu_"+uName+"_package_dependency_EdgeList.csv"
        G = graph_creation_from_edgelist(os.path.join("ubuntu-version",filename))
        #basic_network_measure(filename,G)
        #calculate_average_degree(filename,uName,G)
        cycle_of_the_network(filename,G)
        #calculate_diameter(filename,G)
        #average_shortest_path_length(filename, G)
        #calculate_reciprocity(filename,G)
        #largest_component_fraction(filename,G)
    #bar_plots(listOfRecipro,"Reciprocity",names)
    #bar_plots(listOfD,"density",names)
    #bar_plots(listOfSize,"Component Size",names)
    #bar_plots(listOfNoComp,"Number of Nodes",names)
    #bar_plots(listOfOverAllDens,"Number of Edges",names)
    #bar_plots(listOfDia,"Diameter",names)
    #bar_plots(listOfCycles,"Number of Cycles in largest component",names)
    #bar_plots(listOfAvgSh,"Average shortest path length",names)
    #bar_plots(listOfFracCC,"Fraction Of nodes in largest component",names)
    #line_plot(listOfListNodes,listOfListEdges,"Node vs. Edges",names)
    #line_plot(listOfD,listOfListEdges,"Node vs. Edges",names)
    #line_plot(listOfListAvgDeg,listOfListAvgDegVal,"Average Degree",names)
    #======================================================================================
    #result =[]
    #l = [0,0,2,295,755,4271,6321,7732,1033,6271,7154,5916,1905,5430,6251,2162]
    #totBug = [312,709,2026,4818,12512,23510,28565,29044,32514,25696,34287,29283,11190,24912,23279,9181]
    #obs = ["2004","2005 ","2006 ","2007 ","2008 ","2009 ","2010","2011 ","2012 ","2013","2014 ","2015 ","2016","2017","2018","2019"]
    #for i in range(len(l)):
    #    result.append(float(l[i])/float(totBug[i]))
    #result
    #print(result)
    #bar_plots(result,"Percentage of Bugs having distro",obs)'''