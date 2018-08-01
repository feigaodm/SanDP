## 1) read the binary raw_data.
## 2) smooth the raw data ..... 

#!/usr/bin/env python
from ROOT import *
from array import array
import struct
import sys 
import math
import ctypes
import time

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from peakfinder import find_potential_peaks

## Read Raw Data :
## Be noted: 4 is the length of the str. it is always 4 bytes. 
def get_raw(event_number, filename):
    
    #######
    ## parameters here need to be put in config.ini
    nsamps = 20000  ## samples in wavedump setting
    nchs = 4          ## number of channels in total 
    #######
    
    length_unit = 4
    ## Seek the offset: 
    def calculate_seek_number(event_number):
        if event_number == 0:
            return length_unit ## This offset is for the Unix before the header of the first event.
        return length_unit + event_number*length_unit*6 + event_number*nsamps*nchs*length_unit/2
        ##        UnixTime + event_number*Header        + event_number*samples
        ##        (note: samples need to be /2 according to the CAEN manual)

    const_time=2**31 ## 31 bit counter (TRIGGER TIME TAG)
    ss = open(filename) ## name of the raw_data
    
    ## Last event:
    seek_number = calculate_seek_number(event_number - 1) ## -1 means last event
    ss.seek(seek_number + length_unit*5) ## 5*length_unit offset to TRIGGER TIME TAG
    pre_counter=struct.unpack('i',ss.read(4))[0] & 0xffffffff
    
    ## This event:
    seek_number = calculate_seek_number(event_number)
    ss.seek(seek_number + length_unit*5) ## 5*length_unit offset to TRIGGER TIME TAG
    counter=struct.unpack('i',ss.read(4))[0] & 0xffffffff
    
    ## Calculating the Trigger Time difference between LAST and THIS event:
    if counter >= pre_counter:
        delta_counter= counter-pre_counter
    else :
        delta_counter= counter-pre_counter+const_time
    MicroSec =int(delta_counter * 8e-3) ## Convert time to Micro_seconds
    
    ## Filling the data: ---->
    ## ---------------------->
    channel=[]      ## 2D_list: waveform of each channels.
    data=[0]*nsamps ## 1D_list: summed waveform from all channels.
    
    for j in range(nchs):
        data_tmp=[]
        for i in range(nsamps/2):
            tmp=struct.unpack("i",ss.read(4))[0]
            data_tmp.append((tmp >> 16)*2.0/4096)
            data_tmp.append((tmp & 0x0000ffff)*2.0/4096)
            
        channel.append([i for i in data_tmp])
        for i in range(nsamps):
            data[i]+=data_tmp[i]
                    
    ## ---------------------->
    ## Testing:
    print 'Length of the summed-chs WF:    ',len(data)
    print 'Length of the individual-ch WF: ',len(channel[0])
    print 'Number of channels in total:    ',len(channel)
    ## ---------------------->
    
    return data,channel,MicroSec

## summed WF smoothing:
def smooth(origindata,meanNum=100,cover_num=2):
    clib=ctypes.cdll.LoadLibrary("/home/yuehuan/SanDiX/SanDP/sandp/smooth/smooth.so")
    data_smooth=(ctypes.c_double * len(origindata))()
    for i in range(len(origindata)):
        data_smooth[i]=ctypes.c_double(origindata[i])
    clib.smooth(ctypes.byref(data_smooth),ctypes.c_int(meanNum),ctypes.c_int(len(data_smooth)),ctypes.c_int(cover_num))
    for i in range(cover_num):
        data_smooth[i]=0
        data_smooth[i-1]=0
    return data_smooth

## Draw smooth summed-WF:
def printoutsmooth(evt, fname):
    dat_raw,channels,MicroSec = get_raw(evt, fname)
    dat_smooth = smooth(dat_raw)
    samp_len = len(dat_smooth)
    
    sams = np.linspace(0, samp_len, samp_len)
    plt.figure(figsize = (15,6))

    plt.xlim(-10, samp_len + 10)
    #plt.ylim(0, 2.05)

    plt.xlabel('Samples[4ns]', fontsize =15)
    #plt.ylabel('Amp[V]', fontsize =15)

    plt.grid(True)

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.plot(sams, dat_raw,    color='red',  linestyle='-', linewidth=1., label = 'raw data')
    plt.plot(sams, dat_smooth, color='blue', linestyle='-', linewidth=1., label = 'smooth data')
   
    legend = plt.legend(loc='lower left', shadow=True, fontsize = 15)

    plt.show()
