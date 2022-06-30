# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 13:23:50 2022

@author: ldestouches
"""


import numpy as np
import matplotlib.pyplot as plt

from skimage.morphology import medial_axis
from skimage.graph import shortest_path
from skimage.measure import find_contours

from scipy import interpolate
from scipy.ndimage import median_filter, gaussian_filter, zoom, convolve
from tifffile import imread
from scipy.stats import linregress

from skimage.draw import polygon, line

from skimage.graph import route_through_array

import os
import cv2

import pandas as pd

def extract_roi(mask, margin=8):
    xx,yy=np.where(mask==1)
    xmin = xx.min()
    xmax = xx.max()
    ymin = yy.min()
    ymax = yy.max()
    
    out = np.zeros((xmax-xmin+2*margin, ymax-ymin+2*margin))
    out[margin:-margin,margin:-margin ] = mask[xmin:xmax,ymin:ymax]
    return (xmin,ymin,xmax,ymax), out

def get_skel_extrema(skel):
    """Given a skeletonized image, finds the position of its extremities
    (hopefully only 2)
    Parameters:
        skel (ndarray): skeletonized image
    Returns:
        ndarray: coordinates of extremities of the skeleton"""
    if skel.dtype==bool:
        skel = skel.astype(int)
    connectivity = convolve(skel.astype(int),np.ones((3,3)))*skel.astype(int)
    return np.array(np.where(connectivity==2))

def sort_list_fromref(to_sort, ref):
    return [x for _, x in sorted(zip(ref,to_sort))]

def get_neighbouring_points(xs, ys, xy_ref, dist = 30):
    """Finds all the points within a list of coordinates that are in the vicinity
    of another point
    Parameters:
        xs (list): x coordinates
        ys (list): y coordinates
        xy_ref (list): (x,y) coordinates of the centre 
        dist (float): distance within which points are considered to be in the 
            vicinity of the ref
    Returns:
        list: xs,ys: list of coordinates of points in the neighbourhood of the ref"""
    xs = np.asarray(xs)
    ys = np.asarray(ys)
    dists = np.sqrt((xs-xy_ref[0])**2 + (ys - xy_ref[1])**2)
    
    msk1 = dists<dist
    xs = xs[msk1]
    ys = ys[msk1]
    dists = dists[msk1]
    
    xs = np.array(sort_list_fromref(xs,dists))
    ys = np.array(sort_list_fromref(ys,dists))
    return xs,ys



def prolongate_skel(skel, xy_ref, t_ext = -2, neighbour_dist = 30):
    """Prolongates a skeleton at one of its extremities using linear interpolation.
    Parameters:
        skel (ndarray): the skeletton in int format
        xy_ref (list): x, y values of the extremum from which we want to prolongate
        t_ext (int): has to be negative, how far we want to prolongate
        beighbour_dist (float): distance to the ref point within which we look
            for neighbours
    Returns:
        ndarray: the prolongated skeleton"""
    xs, ys = (skel>0).nonzero()
    xn, yn = get_neighbouring_points(xs,ys,xy_ref, dist = neighbour_dist)
    txn = np.linspace(0,1,xn.size)
    outlinx = linregress(txn,xn)
    outliny = linregress(txn,yn)
    
    r1 = outlinx.slope*t_ext + outlinx.intercept
    c1 = outliny.slope*t_ext + outliny.intercept
    
    rr,cc = line(xy_ref[1], xy_ref[0], int(c1), int(r1))
    msk1 = np.logical_and(rr>=0,rr<skel.shape[1])
    msk2 = np.logical_and(cc>=0,cc<skel.shape[0])
    msk = np.logical_and(msk1, msk2)
    skel=skel.astype(int)
    skel[cc[msk],rr[msk]] = 2
    return skel

def unzoom_skel(skel_zoomed,factor):
    skel_unzoomed = skel_zoomed.reshape(-1,factor,
                         skel_zoomed.shape[1]//factor,factor).sum(axis=(-1,-3))
    return (skel_unzoomed>0)

def cell_dimensions_skel(mask, upsampling_factor = 5,
                         plot_in_context = True, plot_single=False):
    """Measures dimensions of a rod-shaped mask using skeletonization.
    Parameters:
        mask (ndarray): binary mask, represents a rod-shaped bacteria which dimensions
            we are looking for
        upsampling_factor (int): Masks are upsampled by this factor to increase
            method precision. Higher coefficient yields slower but more accurate
            results.
        plot_in_context (bool): if Ture, plots the resulting skeleton
        plot_single (bool): if True, plots the upsampled image of the mask
            along its skeleton. Useful for debuging purpose
    Returns:
        list: [cell_width, cell_length]"""

    margin = 2*upsampling_factor
    submask_coords, submask = extract_roi(mask, margin = margin)
    
    new_img = zoom(gaussian_filter(submask.astype(float),
                                   sigma=upsampling_factor*4/5),upsampling_factor)
    poly = find_contours(new_img,level=0.5)[0]
    rr, cc = polygon(poly[:, 0], poly[:, 1], new_img.shape)
    out = np.zeros_like(new_img)
    out[rr, cc] = 1
    
    skel, dist = medial_axis(out, return_distance = True)
    # factor 2 because measures distance to an edge
    cell_widths = 2*dist[skel]/upsampling_factor
    cell_width = np.median(cell_widths)
    
    x_refs, y_refs = get_skel_extrema(skel)
    
    skel = prolongate_skel(skel, [x_refs[0],y_refs[0]], 
                           neighbour_dist=6*upsampling_factor)
    skel = prolongate_skel(skel, [x_refs[1],y_refs[1]],
                           neighbour_dist=6*upsampling_factor)
    
    submask_zoomed = zoom(submask.astype(int),upsampling_factor)
    
    
    skel = np.logical_and(submask_zoomed==1,skel).astype(int)
    
    if plot_single:
        plt.figure()
        plt.imshow(submask_zoomed)
        xskel, yskel = np.where(skel>0)
        plt.plot(yskel,xskel,"o",color="k")
    skel_unzoomed = unzoom_skel(skel, upsampling_factor)
    skelf =  medial_axis(skel_unzoomed, return_distance = False)

        
    if plot_in_context:
        xskel, yskel = np.where(skelf>0)
        plt.plot(yskel-margin+submask_coords[1],xskel-margin+submask_coords[0],
                 "o",markersize=0.5,color="k")
        
    x_0, y_0 = get_skel_extrema(skelf)
    start = x_0[0], y_0[0]
    end = x_0[1], y_0[1]
    skelf[skelf==0] = 100
    path, cell_length = route_through_array(skelf.astype(float), start, end ,
                                     geometric=True)

    return cell_width, cell_length

if __name__=='__main__':
    plt.close('all')
    path = "C:/Users/ldestouches/Documents/PAPER 2/Test Advanced width/Test seq/FOSFO1_LABEL_rem.tif"
    #path="/home/aurelienb/Documents/Projects/2022_02_Louise/resized_testim_labels.tif"
    img = imread(path)
    # img[img==43] = 0
    img = img[-1]
    nce = 78
    nce = 89
    widths = []
    lengths = []
    img_dsp = img.copy().astype(float)
    img_dsp[img_dsp==0]=np.nan
    plt.figure()
    plt.imshow(img_dsp, cmap="Set2")
    
    labels = np.unique(img).tolist()
    labels.pop(0)
    for nce in labels:
        mask = img==nce
        width, length = cell_dimensions_skel(mask,upsampling_factor=5)
        widths.append(width)
        lengths.append(length)
    
    lab = np.random.choice(labels)
    # lab=699
    width, length = cell_dimensions_skel(img==lab,upsampling_factor=5,plot_in_context=False,
                                         plot_single = True)
    
    # we get the widths list for each tp in widths

    '''    
    plt.figure()
    plt.subplot(121)
    plt.hist(widths,bins=10)
    plt.xlabel("width [pixels]")
    plt.subplot(122)
    plt.hist(lengths,bins=10)
    plt.xlabel("length [pixels]")
    """plt.figure()
     plt.imshow(mask)"""
    '''

#_______________________________________________________________________________________________________

TL_directory = ["C:/Users/ldestouches/Documents/PAPER 2/POST-PROCESSED SEQUENCES/FOSFO1_LABEL_rem"]

path_csv = 'C:/Users/ldestouches/Documents/PAPER 2/Test Advanced width/Test csv/test_FOSFO.csv' # give new name for your csv file here before the .csv

pixel_size = 0.100

time_between_frames = 30 # in minutes # this means every frame of the timelapse used is x minutes apart

def nlabels_and_widths_from_directory(directory, pixel_size):
    
    # number of files in directory
    nfiles = len(os.listdir(directory))
    print("the number of files in the directory is: ", nfiles)
    
    # list for storing all the widths of all the images
    all_filewidths = [[] for i in range(nfiles)]
    
    for file in os.listdir(directory):
        
        # read and show image
        im_path = os.path.join(directory,file)
        img = imread(im_path)
        
        nce = 78
        nce = 89
   
        widths = []
        lengths = []
        img_dsp = img.copy().astype(float)
        img_dsp[img_dsp==0]=np.nan
        plt.figure()
        plt.imshow(img_dsp, cmap="Set2")
        
        labels = np.unique(img).tolist()
        labels.pop(0)
        for nce in labels:
            mask = img==nce
            width, length = cell_dimensions_skel(mask,upsampling_factor=5)
            widths.append(width)
            lengths.append(length)
        
        lab = np.random.choice(labels)
        # lab=699
        width, length = cell_dimensions_skel(img==lab,upsampling_factor=5,plot_in_context=False,
                                             plot_single = True)
        
        all_filewidths.append(widths)
    
    return all_filewidths




# Number of bacteria and big list of widths for timelapses

combined_widths = [[] for i in range(len(os.listdir(TL_directory[0])))]

for i in range(len(TL_directory)):

    widths_tl = nlabels_and_widths_from_directory(TL_directory[i], pixel_size)
    
    for j in range(len(widths_tl)):
        combined_widths[j].extend(widths_tl[j]) 
    
    # PROBLEM ABOUT ADDING WIDTHS FROM SEVERAL TIMELAPSES !!!

# create csv file

D = {}

for count,i in enumerate(range(len(combined_widths))):
    
    keys = str(count*time_between_frames)
    values = combined_widths[i]
    D[keys] = values

df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in D.items() ]))
df.to_csv(path_csv)

        
        
        
        
        
        
#____________________________________________________________________________________________
"""
        
        '''
        plt.figure()
        plt.imshow(im, cmap = 'gray')
        plt.title(file)
        '''
        # find number of bacteria in image
        label_values = np.unique(im)
        nlabel = np.unique(im).size - 1
        all_nlabels.append(nlabel) # add to all files list
        
        # Empty lists where we put the widths for the image
        widths = []
        
        #print("processing file: ", file, "of index", ind)
        
        for i in range(1,nlabel):
            onebac = im==label_values[i]
            # plot_patch(onebac)
            widthbac = get_widthlength_rect(onebac) * pixel_size # multiply by pixel size
            #print('bacteria with label {} has measured width of {:.2f}'.format(i+1, widthbac))
            widths.append(widthbac)
              
        # need to make a loop to iterate over nfiles
        for i in range(0,nfiles):
            if ind == i:
                all_filewidths[i] = widths # here I append a list within a list
    
        ind = ind + 1
    
    return all_filewidths


# Number of bacteria and big list of widths for timelapses

combined_widths = [[] for i in range(len(os.listdir(TL_directory[0])))]

for i in range(len(TL_directory)):

    widths_tl = nlabels_and_widths_from_directory(TL_directory[i], pixel_size)
    
    for j in range(len(widths_tl)):
        combined_widths[j].extend(widths_tl[j])
    

# create csv file

D = {}

for count,i in enumerate(range(len(combined_widths))):
    
    keys = str(count*time_between_frames)
    values = combined_widths[i]
    D[keys] = values

df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in D.items() ]))
df.to_csv(path_csv)

"""

