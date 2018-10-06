# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 17:32:47 2018

This code simulates the time evolution of a spin under the application of an arbitrary shaped microwave pulse.
Start by defining a pulse shape by setting the pulse amplitude (Omega_t) and frequency (delta_t) functions, make sure that 
the plotted pulse is correct since this is the data that is used later on for the computation.
The Spin evolution is computed for the pulse and a 2D plot of the spin components over time is plotted followed by a
3D plot of the spin trace on the bloch sphere.

Finally, a population (absorption) and dispertion profiles are computed and plotted a function of pulse detuning from 
the spin resonance frequency. 
 

@author: Ohad Michel
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, exp, sinc, cos, sin, sqrt, log, linspace, arange

def Blochplot(initial_state):
    ''' Computes and plots the spin evolution on the Bloch sphere
    
    Parameters
    ----------
    initial_state: a numpy 2x2 matrix 
                   represents the initial state of the spin
    
    '''
    from mpl_toolkits.mplot3d import Axes3D # a toolkit for 3D plotting
    sigma = initial_state # Initialize our spin state to the input initial state
    x = np.zeros(np.size(t)) # Spin x component
    y = np.zeros(np.size(t)) # Spin y component
    z = np.zeros(np.size(t)) # Spin z component
    # compute spin state in each time step
    for tstep in range(len(t)):
        sigma = dR(tstep).H * sigma * dR(tstep) # Time step evolution
        x[tstep] = float(np.real((sigma_x * sigma).trace())) # Compute expectation value for x
        y[tstep] = float(np.real((sigma_y * sigma).trace())) # Compute expectation value for y
        z[tstep] = float(np.real((sigma_z * sigma).trace())) # Compute expectation value for z

    ### Plotting ###
    # 2D plot of each component vs. time   
    plt.figure()
    plt.plot(x)
    plt.plot(y)
    plt.plot(z)
    plt.legend(['x','y', 'z']) 
    plt.xlabel('time step')
    plt.title('Spin components vs time')
    
    # 3D plot on the Bloch sphere
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect("equal")
    # Compute x,y,z components of a sphere
    theta, phi = np.mgrid[0:pi:10j, 0:2*pi:20j]
    a = sin(theta)*cos(phi)
    b = sin(theta)*sin(phi)
    c = cos(theta)
    # Plot a sphere and spin evolution on top
    ax.plot_wireframe(a, b, c, color="r")
    ax.plot(xs = x, ys = y, zs = z)
    plt.title('Bloch sphere trace')
    

# Define parameters   
Omega_0 = 2*pi*0.32*1e-3 # maximal Rabi frequency of the pulse [GHz]
Lambda = 2*pi*0.5*1e-3 # frequency sweep amplitude [GHz]
beta = 0.2*1e-3 # sweep rate [ns-1]
tmax = 5/beta; # maximal time for calculation [ns]
dt = 100 # time step for evolution calculation [ns]
t = arange(-tmax, tmax, dt) # a time vector [ns]

Omega_t = Omega_0/np.cosh(beta*t) # Pulse amplitude as afunction of time
delta_t = Lambda*np.tanh(beta*t) # Pulse phase as a function of time 

# Plot pulse amplitude and frequency detuning vs. time
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

# Define Pauli matrices and states
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


# Compute the magnitude of the effective Rabi frequency vector which acts as the torque for the spin rotation
# The x component is the Rabi frequency created by the field on resonance, the z component is detuning from resonance            
Omega_eff_t = lambda tstep: sqrt(Omega_t[tstep]**2 + delta_t[tstep]**2)

# Compute the time step rotation matrix on the bloch sphere : exp(i*dt*Omega_eff/2 * sigma_vec*(omega_eff_direction) )
dR = lambda tstep: eye*cos(Omega_eff_t(tstep)*dt/2) -1j*sin(Omega_eff_t(tstep)*dt/2)*\
                (Omega_t[tstep]*sigma_x/Omega_eff_t(tstep) + delta_t[tstep]*sigma_z/Omega_eff_t(tstep)) # rotation step
                
# plot spin components on the bloch sphere
Blochplot(sigma0)

### Compute z (population/absorption) and x (dispertion) components after the pulse vs. pulse detuning from resonance ###
dmax = 4*2*pi*1e-3 # detuning span [GHz]
delta_t0 = delta_t # keep original frequency sweep
detuning = linspace(-dmax/2,dmax/2,40+1) # detuning vector [GHz]
population = np.zeros((len(detuning), 1)) # population vector
dispersion = np.zeros((len(detuning), 1)) # dispersion vector

# Compute evolution per detuning
for i in range(len(detuning)):
    sigma = sigma0 # Define the initial state
    delta_t = delta_t0 + detuning[i] # detuned delta_t
    # compute state for each time step
    for tstep in range(len(t)):
        sigma = dR(tstep).H * sigma * dR(tstep) # Time step evolution

    population[i] = float(np.real((sigma_z * sigma).trace())) # Store population for detuning i
    dispersion[i] = float(np.real((sigma_x * sigma).trace())) # Store dispersion for detuning i

# Plot population and dispersion vs. detuning
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