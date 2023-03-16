from rocket import Rocket
import numpy as np
from drogue import Drogue
from dynamics import DynamicsReentry
from plotanimate import PlotAnimate
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)




"""This is the main to run the simulation. See documentation for details.
    By Francesco Sala"""


new_rocket = Rocket(0.55, 80.0, 0.02)               # cd0 rocket, mass of rocket, cross-section
new_drogue = Drogue(0.35, 5e3, 0.2, 25)            # cd0 drogue, altitude of deployment, surface of chute, total porosity
dynamics_obj = DynamicsReentry(160, 0, 100e3, 200, 0, new_drogue, new_rocket)  # final_time, x0, z0, vx0, vz0, objects)

dynamics_obj.solve_dynamics()

plot_animate_obj = PlotAnimate(dynamics_obj)
plot_animate_obj.plot_coord()
plot_animate_obj.plot_dynamics()

speed_animation = 30
if speed_animation < 1:
    print("Please enter a speed for the animation >= 1 (e.g. 20)\n")
plot_animate_obj.animate_reentry(speed_animation)

print(new_drogue.t_infl)

