"""Processor for analyzing SanDiX
Provides a framework for calling plugins that manipulate data.
"""
import os

# -*- coding: utf-8 -*-

__author__ = 'Yuehuan Wei, Jingqiang Ye'
__email__ = 'ywei@physics.ucsd.edu, yejingqiang1992@gmail.com'
__version__ = '1.1'

THISDIR = os.path.dirname(os.path.realpath(__file__))

def full_path(local_path):
    return os.path.join(THISDIR, local_path)