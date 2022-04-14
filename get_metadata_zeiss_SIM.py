# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:35:46 2022

@author: ldestouches
"""

def get_psize_zeiss_SIM(image):
    metaSIM = image.imagej_metadata
    psizestr = 