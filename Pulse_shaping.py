"""
Created on Fri Sep 14 17:32:47 2018

This code simulates the time evolution of a spin under the application of
a carefully shaped microwave pulse.

@author: Ohad Michel
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, exp, sinc, cos, sin, sqrt, log, linspace, arange

def blochplot(initial_state):
    from mpl_toolkits.mplot3d import Axes3D
    sigma = initial_state # Define the initial state
    x = np.zeros(np.size(t))
    y = np.zeros(np.size(t))
    z = np.zeros(np.size(t))
    # compute state for each time step
    for tstep in range(len(t)):
        sigma = dR(tstep).H * sigma * dR(tstep)
        x[tstep] = float(np.real((sigma_x * sigma).trace()))
        y[tstep] = float(np.real((sigma_y * sigma).trace()))
        z[tstep] = float(np.real((sigma_z * sigma).trace()))

    plt.figure()
    plt.plot(x)
    plt.plot(y)
    plt.plot(z)
    plt.legend(['x','y', 'z']) 
    plt.xlabel('time step')
    plt.title('Spin components vs time')
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect("equal")
    theta, phi = np.mgrid[0:pi:10j, 0:2*pi:20j]
    a = sin(theta)*cos(phi)
    b = sin(theta)*sin(phi)
    c = cos(theta)
    ax.plot_wireframe(a, b, c, color="r")
    ax.plot(xs = x, ys = y, zs = z)
    plt.title('Bloch sphere trace')
    
    
Omega_0 = 2*pi*0.32*1e-3 # maximal Rabi frequency of the pulse [GHz]
Lambda = 2*pi*0.5*1e-3 # frequency sweep amplitude [GHz]
beta = 0.2*1e-3 # sweep rate [ns-1]
tmax = 5/beta; # maximal time for calculation [ns]
dt = 100 # time step for evolution calculation [ns]
t = arange(-tmax, tmax, dt) # a time vector [ns]

Omega_t = Omega_0/np.cosh(beta*t) # Pulse amplitude as afunction of time
delta_t = Lambda*np.tanh(beta*t) # Pulse phase as a function of time 

plt.figure()
plt.subplot(2,1,1)
plt.plot(t, Omega_t/(2*pi)*1e3)
plt.xlabel('time [ns]')
plt.ylabel('Rabi frequency [MHz]')
plt.title('Pulse shape and frequency modulation')
plt.subplot(2,1,2)
plt.plot(t, delta_t/(2*pi)*1e3)
plt.xlabel('time [ns]')
plt.ylabel('detuning [MHz]')
plt.tight_layout()

# Pauli matrices
sigma0 = np.matrix([[1, 0],\
                   [0, 0]])
                   
sigma1 = np.matrix([[0, 0],\
                   [0, 1]])

sigma_x = np.matrix([[0, 1],\
                    [1, 0]])

sigma_y = np.matrix([[0, -1j],\
                    [1j, 0]])
                    
sigma_z = np.matrix([[1, 0],\
                   [0, -1]])
                   
eye = np.matrix([[1, 0],\
               [0, 1]])
               
Omega_eff_t = lambda tstep: sqrt(Omega_t[tstep]**2 + delta_t[tstep]**2) # Effective Rabi frequency vector

dR = lambda tstep: eye*cos(Omega_eff_t(tstep)*dt/2) -1j*sin(Omega_eff_t(tstep)*dt/2)*\
                (Omega_t[tstep]*sigma_x/Omega_eff_t(tstep) + delta_t[tstep]*sigma_z/Omega_eff_t(tstep)) # rotation step
                
blochplot(sigma0) # plot spin components on the bloch sphere

################ Evolution computation ################
delta_t0 = delta_t # keep original frequency sweep
detuning = linspace(-2,2,40+1)*2*pi*1e-3 # detuning vector [MHz]
population = np.zeros((len(detuning), 1)) # population vector
dispersion = np.zeros((len(detuning), 1)) # population vector
for i in range(len(detuning)):
    sigma = sigma0 # Define the initial state
    delta_t = delta_t0 + detuning[i] # detuned delta_t
    # compute state for each time step
    for tstep in range(len(t)):
        sigma = dR(tstep).H * sigma * dR(tstep)

    population[i] = float(np.real((sigma_z * sigma).trace()))
    dispersion[i] = float(np.real((sigma_x * sigma).trace()))

plt.figure()
plt.subplot(2,1,1)
plt.plot(detuning*1e3/(2*pi), population,'.-')
plt.xlabel('detuning [MHz]')
plt.ylabel('population')
plt.title('Population and dispersion vs detuning')
plt.subplot(2,1,2)
plt.plot(detuning*1e3/(2*pi), dispersion,'.-')
plt.xlabel('detuning [MHz]')
plt.ylabel('dispertion')
plt.tight_layout()
