# SUPERPARA PACKAGE - EPFL Rocket Team 


This Python package allows sizing a supersonic drogue parachute for the reentry of a payload from space (initial altitude > 100 km).
The user must provide some parameters about the payload (the rocket), the initial conditions for the reentry, and decide whether to iterate the solutions of the dynamics
for different altitudes of deployment of the drogue or to compute the design of a hemisflo drogue given an altitude of deployment.
Please follow the provided instructions to run the code.



## Setup
To run this project, clone the repository:

```
$ git clone https://github.com/Fra-Sala/Supersonic_parachute.git
```

The packages used by the project are the following:
 
 - `numpy`
 - `matplotlib`
 - `customtkinter`
 - `pyatmos`
 
 They need to be installed in order to be able to run the code. 
 
 ## How to use the code
 
 The `main.py` must be run in a Python IDE (PyCharm, Spyder, etc.), or simply in the terminal:
 
 ```
$ python3 main.py
```
 
A GUI pops up. The user must fill in the empty fields regarding the rocket and the initial conditions for reentry.
Then, the user must select between ``Iterate dynamics for different altitude of deployment of the drogue" or  ``Define altitude for drogue deployment and compute design".
The first choice will print to screen 3 new entries, z1,z2 and number of iterations n, that define a vector of altitudes an `numpy.linspace(z2,z1,n)'. In this case, when the code is run, a txt file `OUTPUT_DYNAMICS` is created: for each altitude of deployment, a few relevent values concerning the dynamics are printed, so as to guide the user through the choice of a suitable altitude.

The second choice will instead allow the user to enter a single value for the altitude of deployment of the drogue: the iterative study must be carried out beforehand to define a suitable altitude of deployment. In this case, a txt file `OUTPUT_DESIGN` is created, containing all the information about the design of a hemisflo parachute.
The suggested altitude for the deployment of the main parachute is 500 m, but can be chosen by the user.

Note that, at present, only a hemisflo drogue parachute and a conical ribbon main parachute can be selected. 

Finally, the user must click on the button `RUN` to run the program. If the user opted for the dynamics, a few plots are shown regarding the position, velocity and acceleration of the payload with time. An animation is plotted as well if selected by the user at run time. 
 
 ## Details about code and theoretical background
 
 For details about the logic that was followed for the implementation, or for the theoretical background, please refer to the final report.
 
 
 
_Francesco Sala, June 2023_
