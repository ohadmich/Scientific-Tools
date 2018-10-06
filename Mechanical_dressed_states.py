# -*- coding: utf-8 -*-
"""
Created on Thu Oct 04 10:31:06 2018

This script investigates the mechanical interaction of spin states in an NV center's triplet ground state.
We choose to discuss only the mI=+1 subspace of the nitrogen 14 hyperfine states, and also take into
account additional spin coupling (A) to some spin 1/2 systrm in the lattice (such as carbon 13).
We compute the energy of dressed states that emerge from a mechanical coupling between the ms=+1 and ms = -1 states (Omega_m),
plot their magnetic field dependance and quantify their protection from magnetic noise.

@author: Ohad Michel
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigvalsh
from numpy import pi, exp, sinc, cos, sin, sqrt, log, linspace, arange

# Define parameters
D = 2876 # Zero field splitting [MHz]
gamma = 2.8 # Gyromagnetic ratio [MHz/Gauss]
Omega_m = 2 # Mechanical Rabi [MHz]
B = np.array([0, 0, 0.9425]) # Magnetic field [Gauss]
A = [0, 0, .150] # Hyperfine coupling [MHz]

Delta = 5.278 - 2*gamma*B[2] # Mechanical drive detuning [MHz]

# Define matrices
Sz = np.matrix([[1, 0, 0],\
                [0, 0, 0],\
                [0, 0, -1]])
                
Sx = 1.0/sqrt(2) * np.matrix([[0, 1, 0],\
                              [1, 0, 1],\
                              [0, 1, -1]])

Sy = 1.0/sqrt(2) * np.matrix([[0, -1j, 0],\
                              [1j, 0, -1j],\
                              [0, 1j, 0]])

Sz2 = np.matrix([[1, 0, 0],\
                 [0, 0, 0],\
                 [0, 0, 1]])
                 
Iz = 0.5*np.matrix([[1, 0],\
                   [0, -1]])
               
Ix = 0.5*np.matrix([[0, 1],\
                   [1, 0]])
                   
Iy = 0.5*np.matrix([[0, -1j],\
                   [1j, 0]])

Ieye = np.matrix([[1, 0],\
                  [0, 1]])                   
                   
Mc = 0.5*np.matrix([[0, 0, 1],\
                            [0, 0, 0],\
                            [1, 0, 0]]) # Mechanical coupling matrix
                   
H = lambda Del, Om: D*Sz2 + gamma*(B[0]*Sx + B[1]*Sy) -0.5*Del*Sz + Om*Mc # NV Spin Hamiltonian

H_hf = A[0]*np.kron(Sx, Ix) + A[1]*np.kron(Sy, Iy) + A[2]*np.kron(Sz, Iz) # Hyperfine interaction with some spin 1/2 in the lattice

H_tot = lambda Del, Om: np.kron(H(Del, Om),Ieye) + H_hf # Total NV hamiltonian + HF coupling

E = eigvalsh(H_tot(Delta, Omega_m)) # Diagonalize the Hamiltonian and find eigenenergies

#print E

def plotvsB(Om, ST):
    ''' Computes and plots mechanical dressed states energy and their slopes vs. magnetic field
    
    Parameters
    ----------
    Om: a scalar 
        Mechanical Rabi frequency [MHz]
        
    ST: a scalar
        Slope threshold for marking the desired domain [MHz/Gauss]
    
    '''
    ### Computing ###    
    B_range = np.linspace(-2,2, 1000) # Magnetic field magnitude range [Gauss] relative to the mechanical resonance
    Delta_range = gamma*B_range # Detuning range based on magnetic field values [MHz]
    Eup = np.zeros(len(Delta_range)) # Energy vector for the up plus state
    Eum = np.zeros(len(Delta_range)) # Energy vector for the up minus state
    Edp = np.zeros(len(Delta_range)) # Energy vector for the down plus state
    Edm = np.zeros(len(Delta_range)) # Energy vector for the down minus state
    
    for i in range(len(Delta_range)):
        E = eigvalsh(H_tot(Delta_range[i], Om)) # Find eigenvalues 
        # Save energy values and take into account the energy crossing at Delta = 0
        if(Delta_range[i]>0):
            Edp[i] = E[5] - E[0]
            Eup[i] = E[4] - E[0]
            Eum[i] = E[3] - E[0]
            Edm[i] = E[2] - E[0]
        else:
            Eup[i] = E[5] - E[0]
            Edp[i] = E[4] - E[0]
            Edm[i] = E[3] - E[0]
            Eum[i] = E[2] - E[0]
    
    # Compute slopes for one of the ups and one of the downs
    slope_Eup = np.diff(Eup)/np.diff(B_range)
    slope_Edp = np.diff(Edp)/np.diff(B_range)
    
    ### plotting ###
    plt.figure(figsize = (8,8))
    plt.subplot(2,1,1)
    plt.plot(B_range, Eup, color = 'blue')
    plt.plot(B_range, Edp, color = 'red')
    plt.plot(B_range, Eum, color = 'blue')
    plt.plot(B_range, Edm, color = 'red')
    plt.xlabel('Magnetic field [Gauss]')
    plt.ylabel('State frequency [MHz]')
    plt.title('State Frequency vs. Magnetic Field')
    plt.legend(['Up', 'Down'], loc=0)
    
    plt.subplot(2,1,2)   
    plt.plot(B_range[:-1], slope_Eup, color = 'blue')
    plt.plot(B_range[:-1], slope_Edp, color = 'red')
    plt. plot(B_range[:-1], np.zeros(len(slope_Eup)), 'k--')
    plt.fill_between(B_range[:-1], -ST, ST, where =  np.abs(slope_Eup)<ST , color = 'blue', alpha = 0.25)
    plt.fill_between(B_range[:-1], -ST, ST, where =  np.abs(slope_Edp)<ST , color = 'red', alpha = 0.25)
    plt.xlabel('Magnetic field [Gauss]')
    plt.ylabel('slope [MHz/Gauss]')
    plt.title('Slope vs. Magnetic Field')
    plt.legend(['Up Plus', 'Down Plus'], loc=0)
    plt.tight_layout()

plotvsB(2, 0.5)
