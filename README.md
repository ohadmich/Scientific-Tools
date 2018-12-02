# Scientific_Tools
This repository contains some useful scientific functions that I created for my daily research work. 
Below you can find a short summary of the tools and some output examples.

## Bfield Estimator
Computes the magnitude of the magnetic field (B0) and the angle relative to the NV axis (theta)
based on the measured frequencies of the ms=0-->ms=1 and ms=0-->ms=-1 transitions (f = [f0,f1])

In the following example BfieldEstimator was used to estimate the magnetic field magnitude and direction based on the transition frequencies between the spin states in the NV centers's ground state which were extracted from a fit to the data:

<img src ="https://github.com/ohadmich/Scientific-Tools/blob/master/Images/BfieldEstimator.png" width = "600">

## Beam Waist Calculator
This code takes an image of a laser beam as an input, fits the data to a 2D Gaussian beam,
plots the fit laid over the data and displays the waist value next to a one standard deviation error size.

Here is an example for a 2D Gaussian fit (white contours) to a beam image (color scale) and the extracted waist value:

<img src ="https://github.com/ohadmich/Scientific-Tools/blob/master/Images/BeamWaistCalc.png" width = "600">

## Pulse Shaping
This code simulates the time evolution of a spin under the application of an arbitrary shaped microwave pulse.
Start by defining a pulse shape by setting the pulse amplitude (Omega_t) and frequency (delta_t) functions, make sure that 
the plotted pulse is correct since this is the data that is used later on for the computation.
The Spin evolution is computed for the pulse and a 2D plot of the spin components over time is plotted followed by a
3D plot of the spin trace on the bloch sphere.

Finally, a population (absorption) and dispertion profiles are computed and plotted a function of pulse detuning from 
the spin resonance frequency.

Output example:

<img src ="https://github.com/ohadmich/Scientific-Tools/blob/master/Images/Pulse_shaping1.png" width = "400"><img src ="https://github.com/ohadmich/Scientific-Tools/blob/master/Images/Pulse_shaping2.png" width = "400">

<img src ="https://github.com/ohadmich/Scientific-Tools/blob/master/Images/Pulse_shaping3.png" width = "400"><img src ="https://github.com/ohadmich/Scientific-Tools/blob/master/Images/Pulse_shaping4.png" width = "400">

## Mechanical Dressed States
This script investigates the mechanical interaction of spin states in an NV center's triplet ground state.
We choose to discuss only the mI=+1 subspace of the nitrogen 14 hyperfine states, and also take into
account additional spin coupling (A) to some spin 1/2 system in the lattice (such as carbon 13).
We compute the energy of dressed states that emerge from a mechanical coupling between the ms=+1 and ms = -1 states (Omega_m),
plot their magnetic field dependance and quantify their protection from magnetic noise.

Output example:

<img src ="https://github.com/ohadmich/Scientific-Tools/blob/master/Images/Mechanical_dressed_states.png" width = "600">
