# Finite/Zero Temperature String Method (F/ZTSM)

## Overview
The Finite Temperature String Method (FTSM) is a computational approach designed to study rare events in complex systems. These events often occur on rugged energy landscapes where standard methods fail to identify the optimal reaction pathways. FTSM extends the zero-temperature string method to finite temperatures, accounting for thermal fluctuations and entropy effects.

This repository provides an implementation of FTSM for analyzing potential energy surfaces (PES), allowing users to load custom PES data files and calculate transition pathways interactively.

## How It Works
FTSM constructs a "string," a smooth curve connecting two metastable states on a PES. The method iteratively updates the string to converge to the most probable transition pathway, considering:
- **Thermal forces**: The influence of finite temperature on dynamics.
- **Equilibrium probabilities**: Averaging over isoprobability (committer) surfaces.
- **Reparameterization**: Ensuring uniform distribution of images (nodes) along the string.

The output is a transition tube that captures the high-probability regions of the PES, enabling free energy calculations and insight into transition dynamics.

## Features
- Load and visualize PES data interactively.
- Compute gradients and evolve the string using a finite-temperature framework.
- Generate plots of the PES and string evolution.

## References
This code is derived from the original MATLAB implementation of the finite temperature string method developed by Eric Vanden-Eijnden ([CIMS NYU](https://cims.nyu.edu/~eve2/string.htm)).

For more details on the methodology, refer to:
- E, Weinan, Ren, Weiqing, and Vanden-Eijnden, Eric. "Finite temperature string method for the study of rare events." *The Journal of Physical Chemistry B* 109, no. 14 (2005): 6688-6693. DOI: [10.1021/jp0455430](https://pubs.acs.org/doi/10.1021/jp0455430).


