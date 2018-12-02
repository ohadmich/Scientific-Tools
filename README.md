# Scientific_Tools
This repository contains some useful scientific functions that I created for my daily research work. 
Here is a short summary of the tools and some examples of the outputs:

## Pulse Shaping
This code simulates the time evolution of a spin under the application of an arbitrary shaped microwave pulse.
Start by defining a pulse shape by setting the pulse amplitude (Omega_t) and frequency (delta_t) functions, make sure that 
the plotted pulse is correct since this is the data that is used later on for the computation.
The Spin evolution is computed for the pulse and a 2D plot of the spin components over time is plotted followed by a
3D plot of the spin trace on the bloch sphere.

Finally, a population (absorption) and dispertion profiles are computed and plotted a function of pulse detuning from 
the spin resonance frequency.

Output example:


## Mechanical Dressed States
This script investigates the mechanical interaction of spin states in an NV center's triplet ground state.
We choose to discuss only the mI=+1 subspace of the nitrogen 14 hyperfine states, and also take into
account additional spin coupling (A) to some spin 1/2 system in the lattice (such as carbon 13).
We compute the energy of dressed states that emerge from a mechanical coupling between the ms=+1 and ms = -1 states (Omega_m),
plot their magnetic field dependance and quantify their protection from magnetic noise.

Output example:

<img src ="https://github.com/ohadmich/Scientific-Tools/blob/master/Mechanical_dressed_states.png" width = "600">

## Beam Waist Calculator
This code takes an image of a laser beam as an input, fits the data to a 2D Gaussian beam,
plots the fit laid over the data and displays the waist value next to a one standard deviation error size.

Example:

<img src ="https://github.com/ohadmich/Scientific-Tools/blob/master/BeamWaistCalc.png" width = "600">
