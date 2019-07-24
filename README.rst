.. image:: bin/sandix_logo.png

SanDix Processor (SanDP) is used for Analyzing the Data from SanDix Detector.

Instructions:
=========================================

Waveform checking:
----------------------
sandper --waveform --input /rawdata_path/rawdata.dat --event 100

Rawdata processing:
-----------------------
sandper --process --input /rawdata_path/rawdata.dat --outpath /processed_path/

note: the processed data have same name as raw data with extension of .root instead of .dat

Installation:
===============
If you wish to develop SanDP, install it either on your machine or your account on Nilab server, please follow the instructions below.

Installing Python 2 and Anaconda Libraries
---------------------------------------------
SanDP is currently written by **Python 2**. We recommend Anaconda for the python distribution and environment management. To install this in Linux do:  

.. code-block::
  :linenothreshold:2
  
  wget http://repo.continuum.io/archive/Anaconda3-2.4.0-Linux-x86_64.sh  # Linux
  bash Anaconda3-2.4.0-Linux-x86_64.sh  # Say 'yes' to appending to .bashrc and specify the installation directory
  conda install -q conda=4.1.1
