SanDix Processor (SanDP)
==========================

Created: 07-27-2018

Processor for Analyzing the Data from SanDix Detector.

** Be careful, under developing, maybe not work at current status! **

![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `#f03c15`

Waveform checking:
==========================
sandper --waveform --input /rawdata_path/rawdata.dat --event 100

Rawdata processing:
==========================
sandper --process --input /rawdata_path/rawdata.dat --outpath /processed_path/rawdata.root

note: the processed data have same name as raw data with extension of .root instead of .dat


