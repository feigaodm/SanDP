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

nsamp_base = int (cfg['peaks']['nsamp_base'])
s1_thre_base = int (cfg['peaks']['s1_thre_base'])
s2_thre_base = int (cfg['peaks']['s2_thre_base'])
trigger_position = int (cfg['peaks']['trigger_position'])

## processing the data:
def processing(evt, fname):
    
    dat_raw,channels,MicroSec = get_raw(evt, fname)
    dat_smooth = smooth(dat_raw)
    
    ## Baseline:
    BaseLineSumSigma=array('f',[0.0]) 
    BaseLineSumSigma[0]=np.std(dat_smooth[:nsamp_base]) ## shall we use raw_data instead of smoothed one here?
    ##=== find potential S1 S2 =====
    S1_potential = find_potential_peaks(dat_smooth[:], #number of 10000 is half number of samples, need to be changed here.
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