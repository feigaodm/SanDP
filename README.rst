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

Installing Anaconda Libraries
---------------------------------------------
SanDP is currently written by Python. We recommend `Anaconda <https://store.continuum.io/cshop/anaconda/>`_ for the python distribution and environment management. If you already have Anaconda installed, skip this step. To install this in Linux do:  

.. code-block::
  :linenothreshold:2
  
  wget http://repo.continuum.io/archive/Anaconda3-2.4.0-Linux-x86_64.sh  # Linux
  bash Anaconda3-2.4.0-Linux-x86_64.sh  # Say 'yes' to appending to .bashrc and specify the installation directory
  conda install -q conda=4.1.1

Usually the steps above automatically create ``.bashrc`` file. Check the file by

.. code::

  cat ~/.bashrc
  
It should contains the following line:

.. code::

  export PATH=/home/<username>/anaconda3/bin:$PATH 
  
If not, add the line above to ``.bashrc`` file and source it by ``source ~/.bashrc``

Install the environment
-----------------------------
After Anaconda is installed, we can install our environment. Be noted that SanDP is written by **Python 2**.

.. code::

  conda create -n <your_environment> python=2.7 root numpy scipy matplotlib pandas 
  
Then activate your environment by

.. code::

  source activate <your_environment>
  
Solution to common issues can be found in FAQ (to be added) .

Install SanDP
------------------

.. code::
  
  git clone https://github.com/darkmatter-ucsd/SanDP.git
  
Enter your user name and password for GitHub as `SanDP` is a private repository. We recommend you to _`add your SSH to GitHub <https://help.github.com/en/enterprise/2.15/user/articles/adding-a-new-ssh-key-to-your-github-account>`_ to access your private repository without password.

Then install the package by:

.. code::

  cd SanDP
  python setup.py develop
  
The installation is done! To test if it's installed properly, check SanDP version by:

.. code::

  sandper version
  
If it prompts the right version, then congratulate and enjoy the package!
