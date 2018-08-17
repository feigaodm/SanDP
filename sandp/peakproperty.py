import math
from array import array
import numpy as np
import matplotlib


## 1) 
## calculate Entropy for each peak, the entropy quantifies the uniformity of the siganl in time: 
## --------------------------------------------------------------------------------------------->
def Entropy(nchannels,data_channel,BASE_line,boundary,threshold):
    Entropy=0
    for ich in range(nchannels):
        Area=sum([abs(BASE_line[ich]-data_channel[ich][i]) for i in range(boundary[0],boundary[1])])
        for i in range(boundary[0],boundary[1]):
            if (abs(BASE_line[ich]-data_channel[ich][i])>threshold[ich]) and (Area>0):
                prob = abs(BASE_line[ich]-data_channel[ich][i])/Area            
                Entropy -= prob * math.log(prob)
    return Entropy             

## 2)
## the uniformity quantifies the uniformity of the signal distributed in all PMTs:
## --------------------------------------------------------------------------------------------->
def Uniformity(nchannels,PMTgain,data_channel,BASE_line,boundary,threshold=0.3):
    Uniformity=0
    TotalArea=0
    Area=array("f",nchannels*[0.0])
    for ich in range(nchannels):
        Area[ich]=4.9932e8/PMTgain[ich]*sum([abs(BASE_line[ich]-data_channel[ich][i]) for i in range(boundary[0],boundary[1])])
        TotalArea+=Area[ich]
        if (TotalArea>threshold) and (Area[ich]!=0):
            Prob = abs (Area[ich] / TotalArea)
            Uniformity-= Prob * math.log(Prob)
    return Uniformity

## 3)
## Integral for peak area calculation:
## --------------------------------------------------------------------------------------------->
def integral(S,data,BASE_line,PMTgain):
    data_tmp=[]
    for boundary in S:
        data_tmp.append(4.9932e8/PMTgain*sum([BASE_line-data[i] for i in range(boundary[0],boundary[1]+1)]))
    return data_tmp

## 4)
## Sorting peaks by area, returning the sort index :
## --------------------------------------------------------------------------------------------->
def sort_area(S_trap):
    argsort=[]
    for i in range(len(S_trap)):
        maxIndex=-1
        maxValue=-9999
        for j in range(len(S_trap)):
            if (S_trap[j] > maxValue) and (j not in argsort):
                maxIndex=j
                maxValue=S_trap[j] 
        argsort.append(maxIndex)
    return argsort


