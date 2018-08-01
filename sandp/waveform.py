import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import struct
import os
import time

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def drawWF(evt, fname):
    infile = open(fname)
    evtID = evt
    
    #######
    ## parameters here need to be put in config.ini
    nsamples = 20000  ## samples in wavedump setting
    nchs = 4          ## number of channels in total 
    #######
    
    ch0 = []
    ch1 = []
    ch2 = []
    ch3 = []

    
    for i in range(nsamples/2):
        infile.seek(4*i + 4*7 + 6*evtID*4 + (nchs*nsamples/2)*evtID*4)
        tmp=struct.unpack("i",infile.read(4))[0]
        ch0.append((tmp >> 16)*2.0/4096)
        ch0.append((tmp & 0x0000ffff)*2.0/4096)

    for i in range(nsamples/2, nsamples):
        infile.seek(4*i + 4*7 + 6*evtID*4 + (nchs*nsamples/2)*evtID*4)
        tmp=struct.unpack("i",infile.read(4))[0]
        ch1.append((tmp >> 16)*2.0/4096)
        ch1.append((tmp & 0x0000ffff)*2.0/4096)

    for i in range(nsamples, nsamples*3/2):
        infile.seek(4*i + 4*7 + 6*evtID*4 + (nchs*nsamples/2)*evtID*4)
        tmp=struct.unpack("i",infile.read(4))[0]
        ch2.append((tmp >> 16)*2.0/4096)
        ch2.append((tmp & 0x0000ffff)*2.0/4096)

    for i in range(nsamples*3/2, nsamples*2):
        infile.seek(4*i + 4*7 + 6*evtID*4 + (nchs*nsamples/2)*evtID*4)
        tmp=struct.unpack("i",infile.read(4))[0]
        ch3.append((tmp >> 16)*2.0/4096)
        ch3.append((tmp & 0x0000ffff)*2.0/4096)

    ### ------------------------------------------------------------------
    ### ----------------------- draw the Waveform ------------------------>

    samples = np.linspace(0, nsamples, nsamples)
    plt.figure(figsize = (15,6))

    plt.xlim(-10, nsamples + 10)
    plt.ylim(0, 2.05)

    plt.xlabel('Samples[4ns]', fontsize =15)
    plt.ylabel('Amp[V]', fontsize =15)

    plt.grid(True)

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.plot(samples, ch0, color='red',         linestyle='-', linewidth=1., label = 'Ch0')
    plt.plot(samples, ch1, color='blue',        linestyle='-', linewidth=1., label = 'Ch1')
    plt.plot(samples, ch2, color='springgreen', linestyle='-', linewidth=1., label = 'Ch2')
    plt.plot(samples, ch3, color='black',       linestyle='-', linewidth=1., label = 'Ch3')

    legend = plt.legend(loc='lower left', shadow=True, fontsize = 15)

    plt.show()

