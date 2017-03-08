#J750DatalogBinSummary.py
#Creator: Dennis Lin
#Notice:
#It's just a handy small tool for personal use on datalog convert
#It might occupy huge memory due to its "not so good" algorithm
#Just keep it in mind and be careful with it...
#How to execute this code:
#See the options -> c:\folder_name>python J750DatalogBinSummary.py -h
#Combine each site's result -> c:\folder_name>python J750DatalogBinSummary.py -c
#Separate by site -> c:\folder_name>python J750DatalogBinSummary.py -s

import re
from glob import glob
import pandas
import numpy
import fileinput
import sys, getopt

def main_function(BySite):
    GetEnable=False
    ResultString=[]
    ResutlDict={'Site':[],
                'Soft Bin':[],
                'Hard Bin':[]}

    #This block is for reading all the files' name from current folder
    #Then read all files' content to a string variable "Content" except Python related files
    Content=""
    fnames=glob("*")
    for s in fnames:
        if re.search("\.*py",s)==None:
            try:
                Source=open(s,"r")
            except PermissionError as err:
                print(err)
                print("Don't worry about this error.\n")
                continue
            Content=Content+Source.read()
            Source.close()
    DataSplit=[]
    DataSplit=Content.split("\n")

    #Do some compare to append the string it needs from the files
    for TempStr in DataSplit:
        if (TempStr==" Site    Sort     Bin"):
            GetEnable=True
        if (GetEnable==True) and \
           (TempStr!=" Site    Sort     Bin") and \
           (TempStr!="=========================================================================") and \
           (TempStr!="------------------------------------"):
            ResultString.append(TempStr)
        if (TempStr=="========================================================================="):
            GetEnable=False

    #Append the information we got into dictionary variable "ResultDict"
    for Temp in ResultString:
        temp2=Temp.split()
        ResutlDict['Site'].append(int(temp2[0]))
        ResutlDict['Soft Bin'].append(int(temp2[1]))
        ResutlDict['Hard Bin'].append(int(temp2[2]))

    #Convert "ResultDict" to DataFrame
    #Then calculate PV table and convert them into csv file
    ResultData=pandas.DataFrame(ResutlDict)
    ResultData.to_csv('RawData.csv')
    if BySite:
        ResultDataPV=pandas.pivot_table(ResultData,index='Soft Bin',columns='Site',aggfunc='count',fill_value=0,margins=True)
    else:
        ResultDataPV=pandas.pivot_table(ResultData,index='Soft Bin',aggfunc='count',fill_value=0,margins=True)
    print(ResultDataPV)
    ResultDataPV.to_csv('PV.csv')

if __name__=='__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hcs")
    except getopt.GetoptError:
        print("Please enter parameter:")
        print("\t-c: Combine each site's result")
        print("\t-s: Separate by site")
        sys.exit(2)
    for opt, arg in opts:
        if opt=='-h':
            print("Please enter parameter:")
            print("\t-c: Combine each site's result")
            print("\t-s: Separate by site")
            sys.exit()
        elif opt=='-c':
            main_function(False)
        elif opt=='-s':
            main_function(True)
