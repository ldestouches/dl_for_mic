# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:35:46 2022

@author: ldestouches
"""

def get_metadata_zeiss_SIMpsize(image):
    metaSIM = image.imagej_metadata
    psizestr = metaSIM['LsmTag #3'][0:23]
    psizenm = float(psizestr[-7:-1])
    psizemicrom = psizenm * 10**(-3)
    return psizemicrom