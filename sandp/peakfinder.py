## FUNCTIONs for finding the peaks:

#!/usr/bin/env python
from ROOT import *
from array import array
import struct
import sys 
import math
import ctypes
import time
import numpy as np


## Find any potenrial peaks with required width:
def find_potential_peaks(data_smooth, left_width, right_width, threshold):
    
    ## 2) function the refine the boundary searching:
    ## S is 2D list contains the [left, right] edge of each Peaks.
    def accurate_S_boundary(S, data_smooth, threshold_left, threshold_right): 
        for i in range(len(S)): ## len(S) is number of Peaks.
            boundary=S[i]
            num=boundary[0] ## Left edge.
            while  (num > 0) and (data_smooth[num] > threshold_left) :
                num-=1
            S[i][0]=num
            num=boundary[1] ## Right edge.
            while (num<len(data_smooth)) and (data_smooth[num] > threshold_right):
                num+=1
            S[i][1]=num
        return S  
    
    ## 1) roughly find the edge for each peak.
    S=[]
    clib=ctypes.cdll.LoadLibrary("/home/yuehuan/SanDiX/SanDP/sandp/findPoWa/findPoWa.so")
    data_c=(ctypes.c_double * len(data_smooth))()
    for i in range(len(data_smooth)):
        data_c[i]=ctypes.c_double(data_smooth[i])
    func=clib.findPotentialWave
    func.restype=ctypes.c_char_p;
    S1=func(ctypes.byref(data_c), 
            ctypes.c_int(len(data_c)),
            ctypes.c_int(left_width), 
            ctypes.c_int(right_width), 
            ctypes.c_double(threshold))
    s_tmp=S1.split(";")
    if len(s_tmp) > 20: ## if more than 20 peaks find, means the event is very noisy!
        return []
    del s_tmp[-1]
    for i in s_tmp:
        tmp=i.split(",")
        tmp[0]=int(tmp[0])
        tmp[1]=int(tmp[1])
        S.append(tmp) ## S is 2D list contains the [left, right] edge of each Peaks. 
    
    ## First:  using 1) to roughly fiind all peaks.
    ## Second: call the func to re-fine the left/right edge.
    return accurate_S_boundary(S,data_smooth,threshold/2., threshold*2)
