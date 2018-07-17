"""
Created on Wed Apr 11 10:20:04 2018

Computes the magnitude of the magnetic field (B0) and the angle relative to the NV axis (theta)
based on the measured frequencies of the 0-->1 and 0-->-1 transitions (f = [f1,f2])

@author: Ohad Michel
"""

import numpy as np
from scipy.optimize import fmin
from scipy.linalg import eigvalsh
from numpy import pi, sin, cos, sqrt

def EstimateB(f):
    
    """ Computes the magnetic field magnitude and the angle relative to the NV axis based on measured 0-->1 and 0-->-1 transitions.
    
    Parameters:
    ----------
    f: a list of floats, [f1, f2]
       Two measured frequencies for the 0-->1 and 0-->-1 transitions, order is not important.
       Units:f1 and f2 should be given in MHz
       
    Returns:
    -------
    s: a list of floats, [B0, theta]
       Magnetic field magnitude (B0) and angle relative to the NV axis (theta)
       Units: B0 is given in Gauss and theta in degrees
       
    """
    
    def costfunc(Bparams,f1,f2):
        # B0 should be given in Gauss
        # theta should be given in degrees
    
        Deg = pi/180 # degrees to radians conversion factor
        D = 2870 # MHz
        gamma = 2.8 # MHz
        phi = 0 # Aangle in the xy plane in degrees
        B0 = np.abs(Bparams[0])
        theta = np.abs(Bparams[1])*Deg
            
        B = B0*np.array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)])
        L = gamma/sqrt(2)*(B[0]-1j*B[1])
    
        H = np.array([[D+gamma*B[2], L, 0],
                  [np.conjugate(L), 0, L],
                  [0, np.conjugate(L), D-gamma*B[2]]])
    
        E = eigvalsh(H,lower=False)
    
        freq1 = E[2]-E[0]    # 0-->+1 transition frequency
        freqm1 = E[1]-E[0]   # 0-->-1 transition frequency
        
        return (freq1-np.max([f1,f2]))**2 + (freqm1-np.min([f1,f2]))**2
    
    Bparams0 = [0,0] # Initialze parameters
    s = fmin(costfunc,Bparams0,args=(f[0],f[1])) # Find Bfield parameters that minimize the cost function
    print 'B0 = ' + str(np.abs(s[0])) + ' & ' 'theta = ' + str(np.abs(s[1]))
    return s