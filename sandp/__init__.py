"""Processor for analyzing XENON1T
Provides a framework for calling plugins that manipulate data.
"""
import os

# -*- coding: utf-8 -*-

__author__ = 'Yuehuan Wei'
__email__ = 'ywei@physics.ucsd.edu'
__version__ = '1.0'

THISDIR = os.path.dirname(os.path.realpath(__file__))

def full_path(local_path):
    return os.path.join(THISDIR, local_path)