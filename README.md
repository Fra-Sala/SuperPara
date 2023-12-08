# SUPERPARA PACKAGE - EPFL Rocket Team

Welcome to the SuperPara Python package, developed by Francesco Sala for the EPFL Rocket Team. This package is designed to assist in sizing a supersonic drogue parachute for reentry of a payload from space, where the initial altitude exceeds 100 km. Users can input various parameters about the rocket, initial reentry conditions, and choose between iterating solutions for different deployment altitudes or computing the design of a hemisflo drogue for a specific altitude.

## Setup

To get started, clone the repository:

$ git clone https://github.com/Fra-Sala/SuperPara.git

Ensure that the following packages are installed to run the code:

- numpy
- matplotlib
- customtkinter
- pyatmos

You can install these packages using the following command:

$ pip install numpy matplotlib customtkinter pyatmos

## How to Use the Code

Navigate to the Code_parachute/trees folder and locate the main.py file. The code can be run in a Python IDE (PyCharm, Spyder, etc.) or in the terminal:

$ python3 main.py

A GUI will appear, prompting users to fill in information about the rocket and initial reentry conditions. Users can then choose between Iterate dynamics for different altitude of deployment of the drogue or Define altitude for drogue deployment and compute design.

- The first choice prints three new entries (z1, z2, and the number of iterations, n) that define a vector of altitudes using numpy.linspace(z2, z1, n). Running the code generates an OUTPUT_DYNAMICS txt file containing relevant values for each altitude, guiding users in choosing a suitable deployment altitude.

- The second choice allows users to enter a single value for the drogue's deployment altitude, based on the results of the iterative study. This generates an OUTPUT_DESIGN txt file containing all the information about the design of a hemisflo parachute. The suggested altitude for the deployment of the main parachute is 500 m, but users can choose their preferred altitude.

Note that, currently, only a hemisflo drogue parachute and a conical ribbon main parachute can be selected. Click the RUN button to execute the program. If dynamics are selected, plots regarding the position, velocity, and acceleration of the payload over time will be displayed, along with an optional animation.

## Details about Code and Theoretical Background

For details about the logic used in the implementation or the theoretical background, refer to the final report. The code documentation, generated with sphinx, can be found in the docs/_build/html folder.

_Francesco Sala, June 2023_
