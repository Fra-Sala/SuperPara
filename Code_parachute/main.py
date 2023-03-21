from rocket import Rocket
import numpy as np
from drogue import Drogue
from dynamics import DynamicsReentry
from mainpara import Mainpara
from plotanimate import PlotAnimate
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
from scipy.optimize import minimize, LinearConstraint
from optimal_reentry import *



"""This is the main to run the simulation. See documentation for details.
    By Francesco Sala"""

# As a main parachute, we hypothesize a conical ribbon one
x0 = np.array([15e3, 5e2])
final_v = 20   # let impose a landing velocity of 20 m/s
force_main = 50e3
force_drogue = 10e3

linear_constraint = LinearConstraint([[-1, 1], [1, 0], [0,1]], [-np.inf, 1e3, 2e2], [0, 20e3, 2e3])
res = minimize(optimal_reentry, x0, method='SLSQP', args = (20.0, 50e3, 10e3), constraints=linear_constraint,
               options={'disp': True})


new_mainpara = Mainpara(0.5, 5e2, 3.0, 20)          # conical ribbon parachute
new_rocket = Rocket(0.55, 80.0, 0.02)               # cd0 rocket, mass of rocket, cross-section
new_drogue = Drogue(0.35, 4e3, 0.3, 25)            # cd0 drogue, altitude of deployment, surface of chute, total porosity
dynamics_obj = DynamicsReentry(500, 0, 100e3, 300, 0, new_mainpara, new_drogue, new_rocket)  # final_time, x0, z0, vx0, vz0, objects)


dynamics_obj.solve_dynamics()

plot_animate_obj = PlotAnimate(dynamics_obj)
plot_animate_obj.plot_coord()
plot_animate_obj.plot_dynamics()


speed_animation = 20
if speed_animation < 1:
    print("Please enter a speed for the animation >= 1 (e.g. 20)\n")
plot_animate_obj.animate_reentry(speed_animation)



