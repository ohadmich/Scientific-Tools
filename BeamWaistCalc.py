# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:08:17 2017

This code takes an image of a laser beam as an input, fits the data to a 2D Gaussian beam,
plots the fit laid over the data and displays the waist value next to a one standard deviation error size.  
**Please make sure that the pixel size value is updated and correct for your camera**

@author: Ohad Michel
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from numpy import pi, exp, cos, linspace, fft, sqrt
from PIL import Image

# A 2D Gaussian fit function
def Gaussian((x,y), A, B, x0, y0, W):

    G = A*exp( -2*((x-x0)**2 + (y-y0)**2)/W**2 ) + B    
    
    return G.ravel()

# Image files names and location
datafolder = """C:\Users\lab\Documents\Data\\"""
year = "2018_"
monthday = "Nov_30\\"
datafiles = ["Green_beam_output_0.tif", "Green_beam_output_1.tif",\
             "Green_beam_after_lens-f-125mm_before_AOM.tif"]
folder = year+monthday
datafolder = datafolder + folder

pixel_size = 5.2 # Pixel side length [um] (assuming square pixels)

for i in range(len(datafiles)):
    
    im = Image.open(datafolder + datafiles[i]) # load image file
    beam_data = np.array(im)[:,:,0] # Convert to an np.array and take first channel 
    x = np.arange(beam_data.shape[0])*pixel_size # x axis vector [um]
    y = np.arange(beam_data.shape[1])*pixel_size # y axis vecor [um]
    X, Y = np.meshgrid(y,x) # x,y grids [um]
    
    # Find index of max value in a tuple form - used for estimation of Gaussian's center
    indmax = np.unravel_index(np.argmax(beam_data, axis=None), beam_data.shape)
    
    # initial parameters
    A = 255
    B = 0
    x0 = x[indmax[0]]
    y0 = y[indmax[1]]
    W = 200
    
    # fit
    guess = [A,B,x0,y0,W] # Initial guess list
    beam_fit, beam_cov = curve_fit(Gaussian, (X,Y), beam_data.ravel(), p0=guess, maxfev = 100000 )
    [A,B,x0,y0,W] = beam_fit
    fit_err = sqrt(np.diag(beam_cov))
    
    # Show beam profile and fit
    plt.figure()
    plt.pcolormesh(X,Y, beam_data) # Plot beam
    plt.colorbar(label = "Intensity") # Add colorbar
    plt.contour(X,Y, Gaussian((X,Y),A,B,x0,y0,W).reshape(X.shape),10, colors = 'w') # plot fit on top
    W_acc = int(-np.floor(np.log10(fit_err[4]))) # compute accuracy based on fit error
    plt.title("Waist = " + str(round(W,W_acc)) + r"$\pm$" + str(round(fit_err[4], W_acc)) + r"$\mu m$")
    plt.xlabel(r"$x \, (\mu m)$", fontsize = 16)
    plt.ylabel(r"$y \, (\mu m)$", fontsize = 16)
