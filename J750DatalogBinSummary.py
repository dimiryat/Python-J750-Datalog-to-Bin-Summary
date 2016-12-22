#J750DatalogBinSummary.py
#Creator: Dennis Lin

import pandas
import numpy

GetEnable=False
ResultString=[]
ResutlDict={'Site':[],
            'Soft Bin':[],
            'Hard Bin':[]}

SourceFile="C:\\Users\dlin\Downloads\J750-59_FT1RT1_V2A0_82E1_E4.9.0_PIXEL_110416_N0BY16.00B_N0BY16.00_Nov29_2300_16.data"
Source=open(SourceFile,"r")
data=Source.read()
Source.close()
DataSplit=[]
DataSplit=data.split("\n")

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

for Temp in ResultString:
    temp2=Temp.split()
    ResutlDict['Site'].append(int(temp2[0]))
    ResutlDict['Soft Bin'].append(int(temp2[1]))
    ResutlDict['Hard Bin'].append(int(temp2[2]))

ResultData=pandas.DataFrame(ResutlDict)
ResultData.to_csv('RawData.csv')
ResultDataPV=pandas.pivot_table(ResultData,index='Soft Bin',columns='Site',aggfunc='count',fill_value=0,margins=True)
print(ResultDataPV)
ResultDataPV.to_csv('PV.csv')

del ResultString
del data
del Temp
del temp2
del ResultData
del DataSplit
del TempStr
del GetEnable
del pandas
del numpy
