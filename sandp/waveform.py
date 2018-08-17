import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import struct
import os
import time
from array import array

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from rawdata import get_raw
from rawdata import smooth
from peakfinder import find_potential_peaks
from peakrefine import split_S2
from peakrefine import peak_width
from peakrefine import accurate_peaks
from peakrefine import accurate_S1

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('/home/yuehuan/SanDiX/SanDP/sandp/config/sandix.ini')

s1width_lower_limit = int (cfg['peaks']['s1width_lower_limit'])
s1width_upper_limit = int (cfg['peaks']['s1width_upper_limit'])
s2width_lower_limit = int (cfg['peaks']['s2width_lower_limit'])
s2width_upper_limit = int (cfg['peaks']['s2width_upper_limit'])

nsamps = int (cfg['peaks']['nsamps'])
nsamp_base = int (cfg['peaks']['nsamp_base'])
s1_thre_base = int (cfg['peaks']['s1_thre_base'])
s2_thre_base = int (cfg['peaks']['s2_thre_base'])
trigger_position = int (cfg['peaks']['trigger_position'])

def drawWF(evt, fname):
    dat_raw,channels,MicroSec = get_raw(evt, fname)
    dat_smooth = smooth(dat_raw)
    
    #----------->
    rawbaseline = np.mean(dat_raw[0:nsamp_base])
    dat_raw_temp = []
    for i in range(len(dat_raw)):
        dat_raw_temp.append(rawbaseline - dat_raw[i])
    #----------->
    
    ## Baseline:
    BaseLineSumSigma=array('f',[0.0]) 
    BaseLineSumSigma[0]=np.std(dat_raw_temp[:nsamp_base])
    ##=== find potential S1 S2 =====
    S1_potential = find_potential_peaks(dat_smooth[:],
                                        s1width_lower_limit,
                                        s1width_upper_limit,
                                        max(0.001,s1_thre_base*BaseLineSumSigma[0]))

    S2_potential = find_potential_peaks(dat_smooth,
                                        s2width_lower_limit,
                                        s2width_upper_limit,
                                        max(0.001,s2_thre_base*BaseLineSumSigma[0])) 
    print 'S1 edges: ',S1_potential
    print 'S2 edges: ',S2_potential
    print len(S1_potential)
    print len(S2_potential)
    print '\n'
    
    S2_split=split_S2(dat_smooth,S2_potential,0.1,1./5)
    S1_temp,S2=accurate_peaks(dat_smooth,S1_potential,S2_split,trigger_position)
    S1 = accurate_S1(dat_smooth,S1_temp,S2,s1width_upper_limit)
    
    print 'S1 edges: ',S1
    print 'S2 edges: ',S2
    print len(S1)
    print len(S2)

    ######################################################################################################:
    samp_len = nsamps ## from sample to micro-second
    sams = np.linspace(0, samp_len, samp_len)
    
    miny = min(min(channels[0]), min(channels[1]), min(channels[2]), min(channels[3]))
    maxy = max(max(channels[0]), max(channels[1]), max(channels[2]), max(channels[3]))
    ## individul WF:
    fig_individual = plt.figure(figsize = (8, 7))
    plt.subplot(411)
    
    plt.xlim(-10, samp_len + 10)
    plt.ylim(miny, maxy)
    
    plt.xlabel('', fontsize =0)
    plt.ylabel('ch0 [V]', fontsize =10)
    plt.grid(True)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.plot(sams, channels[0], color='black', linestyle='-', linewidth=1., label = '')
    plt.axvline(6500, color='magenta', linestyle='--', linewidth = 1)
    #------------------------------------------------------------------------------------>
    plt.subplot(412)
    
    plt.xlim(-10, samp_len + 10)
    plt.ylim(miny, maxy)
    
    plt.xlabel('Samples [4ns]', fontsize =10)
    plt.ylabel('ch1 [V]', fontsize =10)
    plt.grid(True)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.plot(sams, channels[1], color='black', linestyle='-', linewidth=1., label = '')
    plt.axvline(6500, color='magenta', linestyle='--', linewidth = 1)
    #------------------------------------------------------------------------------------>
    
    plt.subplot(413)
    
    plt.xlim(-10, samp_len + 10)
    plt.ylim(miny, maxy)
    
    plt.xlabel('Samples [4ns]', fontsize =10)
    plt.ylabel('ch2 [V]', fontsize =10)
    plt.grid(True)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.plot(sams, channels[2], color='black', linestyle='-', linewidth=1., label = '')
    plt.axvline(6500, color='magenta', linestyle='--', linewidth = 1)
    #------------------------------------------------------------------------------------>
    plt.subplot(414)
    
    plt.xlim(-10, samp_len + 10)
    plt.ylim(miny, maxy)
    
    plt.xlabel('Samples [4ns]', fontsize =10)
    plt.ylabel('ch3 [V]', fontsize =10)
    plt.grid(True)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.plot(sams, channels[3], color='black', linestyle='-', linewidth=1., label = '')
    plt.axvline(6500, color='magenta', linestyle='--', linewidth = 1)
    #------------------------------------------------------------------------------------>
    ######################################################################################################:
    ## Summed WF:
    fig, ax = plt.subplots(figsize = (10, 7))
    plt.xlim(0, samp_len*4/1000.)
    ## plt.xlim(25,  30)
    ## plt.ylim(0,  0.5)
    plt.xlabel('Time [$\mu s$]', fontsize =15)
    plt.ylabel('Amp [V]', fontsize =15)
    plt.grid(True)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.plot(sams*4/1000., dat_raw_temp, color='black', linestyle='-', linewidth=1., label = 'Summed Waveform')
    plt.plot(sams*4/1000., dat_smooth, color='springgreen', linestyle='-', linewidth=4, alpha = 0.5, label = 'Smoothed Waveform')
    
    ## plot baseline:
    plt.axhline(s1_thre_base*BaseLineSumSigma[0], color='magenta', linestyle='--', linewidth = 1., label = 'S1 Threshold')
    plt.axhline(s2_thre_base*BaseLineSumSigma[0], color='yellow', linestyle='--', linewidth = 1., label = 'S2 Threshold')
    ## S1:
    if len(S1) > 0:
        for p1 in range(len(S1)):
            ax.axvspan(S1[p1][0]*4/1000., S1[p1][1]*4/1000., alpha=0.4, color='magenta', label = 'S1') 
    ## S2:
    if len(S2) > 0:
        for p2 in range(len(S2)):
            ax.axvspan(S2[p2][0]*4/1000., S2[p2][1]*4/1000., alpha=0.4, color='yellow', label = 'S2')
    
    legend = plt.legend(loc='best', shadow=True, fontsize = 10)
    plt.show(block=False)
    raw_input("Hit Enter To Close")
    plt.close()
